import os
import re
import discord
from discord.ext import commands
from openai import AsyncOpenAI

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


class Chat(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.client = AsyncOpenAI()

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
            response = await self.client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": content}],
            )
        reply = response.choices[0].message.content
        await message.reply(reply)


async def setup(bot: commands.Bot):
    await bot.add_cog(Chat(bot))
