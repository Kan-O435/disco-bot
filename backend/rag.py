from pathlib import Path

from sqlalchemy import delete, select

from db import async_session
from embeddings import embed
from models import Document

CHUNK_SIZE = 500


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE) -> list[str]:
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

    chunks = []
    current = ""
    for paragraph in paragraphs:
        if current and len(current) + len(paragraph) + 2 > chunk_size:
            chunks.append(current)
            current = paragraph
        else:
            current = f"{current}\n\n{paragraph}" if current else paragraph

    if current:
        chunks.append(current)
    return chunks


async def ingest_file(path: str) -> int:
    text = Path(path).read_text(encoding="utf-8")
    chunks = chunk_text(text)

    async with async_session() as session:
        await session.execute(delete(Document).where(Document.source == path))

        for index, chunk in enumerate(chunks):
            embedding = await embed(chunk)
            session.add(
                Document(
                    source=path,
                    chunk_index=index,
                    content=chunk,
                    embedding=embedding,
                )
            )

        await session.commit()

    return len(chunks)


async def ingest_directory(directory: str) -> dict[str, int]:
    results = {}
    for md_path in sorted(Path(directory).rglob("*.md")):
        results[str(md_path)] = await ingest_file(str(md_path))
    return results


async def search_documents(conversation_id: str, query: str, limit: int = 3) -> str:
    embedding = await embed(query)
    async with async_session() as session:
        result = await session.execute(
            select(Document)
            .order_by(Document.embedding.cosine_distance(embedding))
            .limit(limit)
        )
        docs = result.scalars().all()

    if not docs:
        return "関連するドキュメントは見つかりませんでした。"
    return "\n\n".join(f"[出典: {d.source}]\n{d.content}" for d in docs)
