import discord
from random import choice
from discord.ext import tasks
from redbot.core import commands

class TybaltPresence(commands.Cog):
    """Tybalt Presence management."""

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.ticker.start()

    def cog_unload(self):
        self.ticker.cancel()

    @tasks.loop(minutes=5.0)
    async def ticker(self):
        await self.tick()
        return

    async def tick(self):
        activities = [
                "Stealing Secrets",
                "Down the Hatch",
                "They Went Thataway",
                "Thrown Off Guard",
                "An Apple a Day",
                "Doubt",
                "Salvation Through Heresy",
                "The False God's Lair",
                "Attempted Deicide",
                "Champion's Sacrifice",
                "Chosen of the Sun",
                "Convincing the Faithful",
                "Unholy Grounds",
                "Untamed Wilds",
                "Pets and Walls Make Stronger Kraals",
                "The Lost Chieftain's Return",
                "Bad Ice",
                "Enraged and Unashamed",
                "Pastkeeper",
                "Evacuation",
                "Rat-Tastrophe",
                "The Hatchery",
                "Thieving from Thieves",
                "Set To Blow",
                "Suspicious Activity",
                "The Battle of Claw Island",
                "Hearts and Minds",
                "Battle of Champion's Dusk"
                ]
        activity = choice(activities)
        await self.bot.change_presence(activity=discord.Game(activity))
