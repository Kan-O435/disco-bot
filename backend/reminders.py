from datetime import datetime, timedelta, timezone

from sqlalchemy import select

from db import async_session
from models import Task

JST = timezone(timedelta(hours=9))
DEADLINE_REMIND_TIME = "09:00"


def build_reminder_message(task: Task) -> str:
    if task.task_type == "daily":
        return f"🔔 リマインド: {task.title}"
    return f"⏰ 締切が近づいています: {task.title}(締切: {task.due_date})"


async def get_due_reminders() -> list[dict]:
    now = datetime.now(JST)
    today = now.date()
    current_time = now.strftime("%H:%M")

    due_messages = []

    async with async_session() as session:
        result = await session.execute(select(Task))
        tasks = result.scalars().all()

        for task in tasks:
            if task.last_reminded_date == today:
                continue

            is_due = False
            if task.task_type == "daily":
                if task.remind_time is not None and current_time >= task.remind_time:
                    is_due = True
            elif task.task_type == "deadline":
                if (
                    task.due_date is not None
                    and task.due_date - today == timedelta(days=1)
                    and current_time >= DEADLINE_REMIND_TIME
                ):
                    is_due = True

            if is_due:
                task.last_reminded_date = today
                due_messages.append(
                    {
                        "conversation_id": task.conversation_id,
                        "message": build_reminder_message(task),
                    }
                )

        await session.commit()

    return due_messages
