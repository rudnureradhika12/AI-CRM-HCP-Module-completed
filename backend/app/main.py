from dotenv import load_dotenv
load_dotenv()

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import interactions
from app.db import init_db

app = FastAPI(title="AI-First CRM HCP Module")
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(interactions.router, prefix="/api/interactions")

@app.on_event('startup')
async def startup_event():
    # initialize DB (create tables)
    await init_db()

@app.get('/')
async def root():
    return {"status":"AI-CRM-HCP backend running"}

from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str


@app.post("/api/chat")
async def chat_ai(req: ChatRequest):
    user_msg = req.message.lower()

    # simple demo AI logic (replace with OpenAI/Groq later)
    if "visit" in user_msg:
        reply = "It sounds like a visit interaction. Make sure to note doctor feedback."
    elif "call" in user_msg:
        reply = "Calls are great for follow-ups. Did the doctor request anything?"
    elif "product" in user_msg:
        reply = "Product discussions should include objections and acceptance."
    else:
        reply = "Tell me more about the interaction and I will analyze it."

    return {"reply": reply}


from app.api import chat

app.include_router(chat.router, prefix="/api")


from app.ai_engine import get_ai_reply

@app.post("/api/chat")
def chat_with_ai(data: dict):
    user_msg = data.get("message")
    reply = get_ai_reply(user_msg)
    return {"reply": reply}



chat_history = []

@app.post("/api/chat")
def chat_api(req: ChatRequest):
    chat_history.append({"role": "user", "msg": req.message})

    reply = ai_response_logic(req.message)   # pyright: ignore[reportUndefinedVariable] # your AI function

    chat_history.append({"role": "agent", "msg": reply})

    return {"reply": reply, "history": chat_history}
