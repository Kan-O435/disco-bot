import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

import httpx

HN_ALGOLIA_URL = "https://hn.algolia.com/api/v1/search_by_date"
HN_ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"
HN_TOPSTORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
BBC_RSS_URL = "https://feeds.bbci.co.uk/news/world/rss.xml"
ARXIV_API_URL = "https://export.arxiv.org/api/query"

ATOM_NS = {"atom": "http://www.w3.org/2005/Atom"}


def _format_list(items: list[tuple[str, str]]) -> str:
    if not items:
        return "現在取得できるニュースがありません。"
    return "\n".join(f"- {title}\n  {url}" for title, url in items)


async def get_ai_news(conversation_id: str) -> str:
    since = int((datetime.now(timezone.utc) - timedelta(days=1)).timestamp())
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            HN_ALGOLIA_URL,
            params={
                "tags": "story",
                "query": "AI",
                "numericFilters": f"created_at_i>{since}",
            },
        )
        resp.raise_for_status()
        hits = resp.json()["hits"][:5]

    items = [
        (
            h["title"],
            h.get("url") or f"https://news.ycombinator.com/item?id={h['objectID']}",
        )
        for h in hits
    ]
    return _format_list(items)


async def get_it_news(conversation_id: str) -> str:
    async with httpx.AsyncClient() as client:
        resp = await client.get(HN_TOPSTORIES_URL)
        resp.raise_for_status()
        story_ids = resp.json()[:5]

        items = []
        for story_id in story_ids:
            item_resp = await client.get(HN_ITEM_URL.format(story_id))
            item_resp.raise_for_status()
            data = item_resp.json()
            title = data.get("title", "(no title)")
            url = data.get("url") or f"https://news.ycombinator.com/item?id={story_id}"
            items.append((title, url))

    return _format_list(items)


async def get_english_news(conversation_id: str) -> str:
    async with httpx.AsyncClient() as client:
        resp = await client.get(BBC_RSS_URL)
        resp.raise_for_status()

    root = ET.fromstring(resp.text)
    entries = root.findall(".//item")[:5]
    items = [(e.find("title").text, e.find("link").text) for e in entries]
    return _format_list(items)


async def get_semiconductor_news(conversation_id: str) -> str:
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            ARXIV_API_URL,
            params={
                "search_query": "cat:cs.AR OR cat:physics.comp-ph",
                "sortBy": "submittedDate",
                "sortOrder": "descending",
                "max_results": 5,
            },
        )
        resp.raise_for_status()

    root = ET.fromstring(resp.text)
    entries = root.findall("atom:entry", ATOM_NS)
    items = []
    for entry in entries:
        title = entry.find("atom:title", ATOM_NS).text.strip().replace("\n", " ")
        link = entry.find("atom:id", ATOM_NS).text
        items.append((title, link))
    return _format_list(items)
