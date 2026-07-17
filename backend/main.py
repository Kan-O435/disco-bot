import os
from collections import defaultdict, deque

from fastapi import FastAPI
from openai import AsyncOpenAI
from pydantic import BaseModel

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
HISTORY_LIMIT = int(os.getenv("CHAT_HISTORY_LIMIT", "20"))

app = FastAPI()
client = AsyncOpenAI()
histories: dict[str, deque[dict]] = defaultdict(lambda: deque(maxlen=HISTORY_LIMIT))


class ChatRequest(BaseModel):
    conversation_id: str
    message: str


class ChatResponse(BaseModel):
    reply: str


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    history = histories[request.conversation_id]
    history.append({"role": "user", "content": request.message})

    response = await client.chat.completions.create(
        model=MODEL,
        messages=list(history),
    )
    reply = response.choices[0].message.content
    history.append({"role": "assistant", "content": reply})

    return ChatResponse(reply=reply)
