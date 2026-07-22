from datetime import date, datetime

from sqlalchemy import select

from db import async_session
from models import Task
from news import get_ai_news, get_english_news, get_it_news, get_semiconductor_news
from timeutil import JST


async def get_current_time(conversation_id: str) -> str:
    return datetime.now(JST).strftime("%Y-%m-%d %H:%M:%S JST")


async def add_daily_task(conversation_id: str, title: str, remind_time: str) -> str:
    async with async_session() as session:
        existing = await session.execute(
            select(Task).where(
                Task.conversation_id == conversation_id,
                Task.task_type == "daily",
                Task.title == title,
                Task.remind_time == remind_time,
            )
        )
        if existing.scalars().first() is not None:
            return f"毎日{remind_time}の「{title}」は既に登録されています。"

        session.add(
            Task(
                conversation_id=conversation_id,
                task_type="daily",
                title=title,
                remind_time=remind_time,
            )
        )
        await session.commit()
    return f"毎日{remind_time}にリマインドするタスク「{title}」を登録しました。"


async def add_deadline_task(conversation_id: str, title: str, due_date: str) -> str:
    due_date_value = date.fromisoformat(due_date)

    async with async_session() as session:
        existing = await session.execute(
            select(Task).where(
                Task.conversation_id == conversation_id,
                Task.task_type == "deadline",
                Task.title == title,
                Task.due_date == due_date_value,
            )
        )
        if existing.scalars().first() is not None:
            return f"締切{due_date}の「{title}」は既に登録されています。"

        session.add(
            Task(
                conversation_id=conversation_id,
                task_type="deadline",
                title=title,
                due_date=due_date_value,
            )
        )
        await session.commit()
    return f"締切{due_date}のタスク「{title}」を登録しました。"


async def list_tasks(conversation_id: str) -> str:
    async with async_session() as session:
        result = await session.execute(
            select(Task).where(Task.conversation_id == conversation_id)
        )
        tasks = result.scalars().all()

    if not tasks:
        return "登録されているタスクはありません。"

    lines = []
    for task in tasks:
        if task.task_type == "daily":
            lines.append(f"[毎日 {task.remind_time}] {task.title}")
        else:
            lines.append(f"[締切 {task.due_date}] {task.title}")
    return "\n".join(lines)


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "現在の日時(日本時間, JST)を取得します",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "add_daily_task",
            "description": "毎日決まった時刻にリマインドするタスクを登録します",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "タスクの内容"},
                    "remind_time": {
                        "type": "string",
                        "description": "リマインドする時刻。24時間表記のHH:MM形式(例: 09:00)",
                    },
                },
                "required": ["title", "remind_time"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "add_deadline_task",
            "description": "締切のあるタスクを登録します",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "タスクの内容"},
                    "due_date": {
                        "type": "string",
                        "description": "締切日。YYYY-MM-DD形式",
                    },
                },
                "required": ["title", "due_date"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "登録されているタスク一覧を取得します",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_ai_news",
            "description": "直近24時間のAI関連ニュースを取得します(Hacker News検索)",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_it_news",
            "description": "AWSやIT技術全般など、Hacker Newsの現在の上位ニュースを取得します",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_english_news",
            "description": "英語学習用に、BBC Newsの英語の国際ニュースを取得します",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_semiconductor_news",
            "description": "半導体やシミュレーション分野の最新論文(arXiv)を取得します",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
]

TOOL_FUNCTIONS = {
    "get_current_time": get_current_time,
    "add_daily_task": add_daily_task,
    "add_deadline_task": add_deadline_task,
    "list_tasks": list_tasks,
    "get_ai_news": get_ai_news,
    "get_it_news": get_it_news,
    "get_english_news": get_english_news,
    "get_semiconductor_news": get_semiconductor_news,
}
