from sqlalchemy import select

from db import async_session
from embeddings import embed
from models import Memory


async def save_memory(conversation_id: str, fact: str) -> str:
    embedding = await embed(fact)
    async with async_session() as session:
        session.add(
            Memory(conversation_id=conversation_id, content=fact, embedding=embedding)
        )
        await session.commit()
    return f"覚えました: {fact}"


async def recall_memory(conversation_id: str, query: str, limit: int = 3) -> str:
    embedding = await embed(query)
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
