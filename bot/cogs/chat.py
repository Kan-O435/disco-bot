import os
import re

import aiohttp
import discord
from discord.ext import commands

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")


class Chat(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.session: aiohttp.ClientSession | None = None

    async def cog_load(self):
        self.session = aiohttp.ClientSession()

    async def cog_unload(self):
        await self.session.close()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if self.bot.user not in message.mentions:
            return

        content = re.sub(rf"<@!?{self.bot.user.id}>", "", message.content).strip()
        if not content:
            return

        async with message.channel.typing():
            async with self.session.post(
                f"{BACKEND_URL}/chat",
                json={
                    "conversation_id": str(message.channel.id),
                    "message": content,
                },
            ) as resp:
                resp.raise_for_status()
                data = await resp.json()

        await message.reply(data["reply"])


async def setup(bot: commands.Bot):
    await bot.add_cog(Chat(bot))
