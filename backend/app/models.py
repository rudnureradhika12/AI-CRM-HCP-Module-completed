# Pydantic models
from pydantic import BaseModel
from typing import Optional, List, Any

class InteractionOut(BaseModel):
    id: int
    hcp_id: str
    rep_id: str
    interaction_type: str
    notes: Optional[str]
    summary: Optional[str]
    entities: Optional[List[Any]]
