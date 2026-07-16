import os
import discord
from discord import app_commands
from discord.ext import commands
from openai import AsyncOpenAI

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


class Chat(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.client = AsyncOpenAI()

    @app_commands.command(name="chat", description="AIと会話します")
    @app_commands.describe(message="AIに送るメッセージ")
    async def chat(self, interaction: discord.Interaction, message: str):
        await interaction.response.defer()
        response = await self.client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": message}],
        )
        reply = response.choices[0].message.content
        await interaction.followup.send(reply)


async def setup(bot: commands.Bot):
    await bot.add_cog(Chat(bot))
