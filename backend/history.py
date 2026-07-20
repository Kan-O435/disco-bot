from sqlalchemy import select

from db import async_session
from models import Message


async def get_history(conversation_id: str, limit: int) -> list[dict]:
    async with async_session() as session:
        result = await session.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
        )
        rows = result.scalars().all()

    rows.reverse()
    return [{"role": row.role, "content": row.content} for row in rows]


async def save_message(conversation_id: str, role: str, content: str) -> None:
    async with async_session() as session:
        session.add(
            Message(conversation_id=conversation_id, role=role, content=content)
        )
        await session.commit()
