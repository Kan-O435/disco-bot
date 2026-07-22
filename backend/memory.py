from openai import AsyncOpenAI
from sqlalchemy import select

from db import async_session
from models import Memory

EMBEDDING_MODEL = "text-embedding-3-small"

client = AsyncOpenAI()


async def _embed(text: str) -> list[float]:
    response = await client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    return response.data[0].embedding


async def save_memory(conversation_id: str, fact: str) -> str:
    embedding = await _embed(fact)
    async with async_session() as session:
        session.add(
            Memory(conversation_id=conversation_id, content=fact, embedding=embedding)
        )
        await session.commit()
    return f"覚えました: {fact}"


async def recall_memory(conversation_id: str, query: str, limit: int = 3) -> str:
    embedding = await _embed(query)
    async with async_session() as session:
        result = await session.execute(
            select(Memory)
            .where(Memory.conversation_id == conversation_id)
            .order_by(Memory.embedding.cosine_distance(embedding))
            .limit(limit)
        )
        memories = result.scalars().all()

    if not memories:
        return "関連する記憶は見つかりませんでした。"
    return "\n".join(f"- {m.content}" for m in memories)
