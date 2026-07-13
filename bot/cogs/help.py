import discord
from discord import app_commands
from discord.ext import commands

COMMAND_DESCRIPTIONS = (
    "**/ping** - pongと返信します\n"
    "**/chat** - AIと会話します(準備中)\n"
    "**/help** - コマンド一覧を表示します"
)


class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="help", description="コマンド一覧を表示します")
    async def help(self, interaction: discord.Interaction):
        await interaction.response.send_message(COMMAND_DESCRIPTIONS)


async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))
