import discord
from redbot.core import checks, commands
from redbot.core import Config

class UtilCommands(commands.Cog):
    """UtilCommands."""

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.dm_only()
    async def clear_dm(self, ctx):
        messages = await ctx.message.channel.history(limit=50).flatten();
        to_delete = []
        for message in messages:
            if message.author == self.bot.user:
                await message.delete();


