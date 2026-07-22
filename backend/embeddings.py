from openai import AsyncOpenAI

EMBEDDING_MODEL = "text-embedding-3-small"

client = AsyncOpenAI()


async def embed(text: str) -> list[float]:
    response = await client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    return response.data[0].embedding
