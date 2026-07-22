import os

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")


class Ingest(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.session: aiohttp.ClientSession | None = None

    async def cog_load(self):
        self.session = aiohttp.ClientSession()

    async def cog_unload(self):
        await self.session.close()

    @app_commands.command(
        name="ingest", description="登録済みドキュメント(Markdown)を再取り込みします"
    )
    async def ingest(self, interaction: discord.Interaction):
        await interaction.response.defer()

        async with self.session.post(f"{BACKEND_URL}/documents/ingest", json={}) as resp:
            resp.raise_for_status()
            data = await resp.json()

        if not data:
            await interaction.followup.send(
                "取り込めるMarkdownファイルが見つかりませんでした。"
            )
            return

        lines = [f"- {source}: {count}チャンク" for source, count in data.items()]
        await interaction.followup.send("取り込み完了:\n" + "\n".join(lines))


async def setup(bot: commands.Bot):
    await bot.add_cog(Ingest(bot))
