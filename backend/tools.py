from datetime import datetime, timezone


def get_current_time() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "現在の日時(UTC)を取得します",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
]

TOOL_FUNCTIONS = {
    "get_current_time": get_current_time,
}
