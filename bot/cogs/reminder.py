import os

import aiohttp
from discord.ext import commands, tasks

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")
CHECK_INTERVAL_SECONDS = int(os.getenv("REMINDER_CHECK_INTERVAL", "60"))


class Reminder(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.session: aiohttp.ClientSession | None = None

    async def cog_load(self):
        self.session = aiohttp.ClientSession()
        self.check_reminders.start()

    async def cog_unload(self):
        self.check_reminders.cancel()
        await self.session.close()

    @tasks.loop(seconds=CHECK_INTERVAL_SECONDS)
    async def check_reminders(self):
        try:
            async with self.session.get(f"{BACKEND_URL}/reminders/due") as resp:
                resp.raise_for_status()
                reminders = await resp.json()

            for reminder in reminders:
                try:
                    channel_id = int(reminder["conversation_id"])
                except ValueError:
                    continue

                channel = self.bot.get_channel(channel_id)
                if channel is not None:
                    await channel.send(reminder["message"])
        except Exception as e:
            print(f"⚠️ リマインドチェック中にエラーが発生しました: {e}")

    @check_reminders.before_loop
    async def before_check_reminders(self):
        await self.bot.wait_until_ready()


async def setup(bot: commands.Bot):
    await bot.add_cog(Reminder(bot))
