import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from openai import AsyncOpenAI
from pydantic import BaseModel

from db import check_connection, create_tables
from history import get_history, save_message
from models import Message  # noqa: F401 (registers table with Base.metadata)

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
HISTORY_LIMIT = int(os.getenv("CHAT_HISTORY_LIMIT", "20"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)
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
