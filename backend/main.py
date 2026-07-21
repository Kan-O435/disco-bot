import os

from fastapi import FastAPI
from openai import AsyncOpenAI
from pydantic import BaseModel

from db import check_connection
from history import get_history, save_message

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
HISTORY_LIMIT = int(os.getenv("CHAT_HISTORY_LIMIT", "20"))

app = FastAPI()
client = AsyncOpenAI()


class ChatRequest(BaseModel):
    conversation_id: str
    message: str


class ChatResponse(BaseModel):
    reply: str


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/health/db")
async def health_db():
    await check_connection()
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    await save_message(request.conversation_id, "user", request.message)
    history = await get_history(request.conversation_id, HISTORY_LIMIT)

    response = await client.chat.completions.create(
        model=MODEL,
        messages=history,
    )
    reply = response.choices[0].message.content
    await save_message(request.conversation_id, "assistant", reply)

    return ChatResponse(reply=reply)
