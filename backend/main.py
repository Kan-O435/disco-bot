import json
import os

from fastapi import FastAPI
from openai import AsyncOpenAI
from pydantic import BaseModel

from db import check_connection
from history import get_history, save_message
from reminders import get_due_reminders
from tools import TOOL_FUNCTIONS, TOOLS

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


@app.get("/reminders/due")
async def reminders_due():
    return await get_due_reminders()


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    await save_message(request.conversation_id, "user", request.message)
    history = await get_history(request.conversation_id, HISTORY_LIMIT)

    response = await client.chat.completions.create(
        model=MODEL,
        messages=history,
        tools=TOOLS,
    )
    message = response.choices[0].message

    if message.tool_calls:
        history.append(message.model_dump(exclude_none=True))
        for tool_call in message.tool_calls:
            func = TOOL_FUNCTIONS[tool_call.function.name]
            args = json.loads(tool_call.function.arguments)
            result = await func(conversation_id=request.conversation_id, **args)
            history.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result),
                }
            )

        response = await client.chat.completions.create(
            model=MODEL,
            messages=history,
        )
        message = response.choices[0].message

    reply = message.content
    await save_message(request.conversation_id, "assistant", reply)

    return ChatResponse(reply=reply)
