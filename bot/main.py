import os
import discord
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = 1522506364449062952

intents = discord.Intents.default()

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    guild = discord.Object(id=GUILD_ID)
    tree.copy_global_to(guild=guild)
    await tree.sync(guild=guild)
    print(f"✅ ログインしました: {client.user}")

@tree.command(name="ping", description="pongと返信します")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("pong")

client.run(TOKEN)