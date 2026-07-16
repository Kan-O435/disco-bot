import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = 1522506364449062952

INITIAL_EXTENSIONS = [
    "cogs.ping",
    "cogs.chat",
    "cogs.help",
]

intents = discord.Intents.default()


class AgentBot(commands.Bot):
    async def setup_hook(self):
        for extension in INITIAL_EXTENSIONS:
            try:
                await self.load_extension(extension)
            except Exception:
                print(f"⚠️ {extension} の読み込みに失敗しました")
                import traceback
                traceback.print_exc()

        guild = discord.Object(id=GUILD_ID)
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)


bot = AgentBot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"✅ ログインしました: {bot.user}")


bot.run(TOKEN)
