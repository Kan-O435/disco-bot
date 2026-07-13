import discord
from discord import app_commands
from discord.ext import commands


class Chat(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="chat", description="AIと会話します")
    @app_commands.describe(message="AIに送るメッセージ")
    async def chat(self, interaction: discord.Interaction, message: str):
        # TODO: Phase 2でOpenAI APIによる応答生成に置き換える
        await interaction.response.send_message(
            f"「{message}」を受け取りました。AI応答は現在準備中です。"
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Chat(bot))
