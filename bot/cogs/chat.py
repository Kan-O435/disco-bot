import os
import re
from collections import defaultdict, deque

import discord
from discord.ext import commands
from openai import AsyncOpenAI

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
HISTORY_LIMIT = int(os.getenv("CHAT_HISTORY_LIMIT", "20"))


class Chat(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.client = AsyncOpenAI()
        self.histories: dict[int, deque[dict]] = defaultdict(
            lambda: deque(maxlen=HISTORY_LIMIT)
        )

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if self.bot.user not in message.mentions:
            return

        content = re.sub(rf"<@!?{self.bot.user.id}>", "", message.content).strip()
        if not content:
            return

        history = self.histories[message.channel.id]
        history.append({"role": "user", "content": content})

        async with message.channel.typing():
            response = await self.client.chat.completions.create(
                model=MODEL,
                messages=list(history),
            )
        reply = response.choices[0].message.content
        history.append({"role": "assistant", "content": reply})

        await message.reply(reply)


async def setup(bot: commands.Bot):
    await bot.add_cog(Chat(bot))
