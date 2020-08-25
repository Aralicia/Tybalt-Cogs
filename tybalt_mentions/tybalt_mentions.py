import discord
import random
from redbot.core import checks, commands
from redbot.core import Config

class TybaltMentions(commands.Cog):
    """Tybalt answers to Mentions."""

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.config = Config.get_conf(self, identifier=186348296931)
        self.config.register_global(
            quotes=[]
        )

    @commands.Cog.listener()
    async def on_message(self, message):
        if len(message.mentions) == 1 and message.mentions[0].id == self.bot.user.id :
            quotes = await self.config.quotes()
            quote = random.choice(quotes)
            await message.channel.send(quote)

