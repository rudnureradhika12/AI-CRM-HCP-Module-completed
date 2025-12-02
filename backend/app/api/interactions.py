from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Any
from app.agents.hcp_agent import HCPAgent
from app.db import get_db, Interaction
from sqlalchemy.orm import Session
import json

router = APIRouter()
agent = HCPAgent()

class InteractionIn(BaseModel):
    hcp_id: str
    rep_id: str
    interaction_type: str
    notes: Optional[str] = None
    metadata: Optional[dict] = None

@router.post('/', status_code=201)
async def log_interaction(payload: InteractionIn, db: Session = Depends(lambda: next(get_db()))):
    try:
        # create DB record (raw)
        rec = Interaction(
            hcp_id=payload.hcp_id,
            rep_id=payload.rep_id,
            interaction_type=payload.interaction_type,
            notes=payload.notes or '',
            metadata=json.dumps(payload.metadata or {})
        )
        db.add(rec)
        db.commit()
        db.refresh(rec)
        # run agent tool to summarize & extract entities
        result = await agent.tools.log_interaction_tool({
            'interaction_id': rec.id,
            'hcp_id': rec.hcp_id,
            'rep_id': rec.rep_id,
            'notes': rec.notes,
            'metadata': payload.metadata or {}
        })
        # update record with summary/entities
        rec.summary = result.get('summary')
        rec.entities = json.dumps(result.get('entities', []))
        db.add(rec)
        db.commit()
        db.refresh(rec)
        return {
            'id': rec.id,
            'hcp_id': rec.hcp_id,
            'rep_id': rec.rep_id,
            'interaction_type': rec.interaction_type,
            'notes': rec.notes,
            'summary': rec.summary,
            'entities': result.get('entities', [])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put('/{interaction_id}')
async def edit_interaction(interaction_id: int, payload: InteractionIn, db: Session = Depends(lambda: next(get_db()))):
    try:
        rec = db.query(Interaction).filter(Interaction.id == interaction_id).first()
        if not rec:
            raise HTTPException(status_code=404, detail='Interaction not found')
        rec.hcp_id = payload.hcp_id
        rec.rep_id = payload.rep_id
        rec.interaction_type = payload.interaction_type
        rec.notes = payload.notes or rec.notes
        rec.extra_data = json.dumps(payload.metadata or {})
        db.add(rec)
        db.commit()
        db.refresh(rec)
        # optionally re-run summarizer if notes changed
        result = await agent.tools.edit_interaction_tool(interaction_id, {
            'notes': rec.notes
        })
        rec.summary = result.get('summary') or rec.summary
        rec.entities = json.dumps(result.get('entities', [])) if result.get('entities') else rec.entities
        db.add(rec)
        db.commit()
        db.refresh(rec)
        return {'status':'ok', 'id': rec.id, 'summary': rec.summary, 'entities': json.loads(rec.entities) if rec.entities else []}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


