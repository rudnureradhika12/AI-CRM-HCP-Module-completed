from fastapi import APIRouter
from pydantic import BaseModel
from app.agents.ai_engine import run_ai

router = APIRouter()

class ChatInput(BaseModel):
    message: str

@router.post("/chat")
def ai_reply(data: ChatInput):
    prompt = f"""
    You are a CRM assistant.
    Analyze and assist this interaction:
    {data.message}

    Give summary, intent, tags, next actions.
    """
    reply = run_ai(prompt)
    return {"reply": reply}
