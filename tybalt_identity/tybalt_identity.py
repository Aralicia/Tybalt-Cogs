import discord
import random
from redbot.core import checks, commands
from redbot.core import Config
from discord.ext import tasks

class TybaltIdentity(commands.Cog):
    """Tybalt identity features."""

    def __init__(self, bot):
        super().__init__()
        self.identityId = None;
        self.identity = None;
        self.bot = bot
        self.config = Config.get_conf(self, identifier=186348696931)
        default_global = {
            "prefix":"",
            "identities":{}
        }
        self.config.register_global(**default_global)
        self.ticker.start()

    def cog_unload(self):
        self.ticker.cancel()

    @tasks.loop(minutes=15.0)
    async def ticker(self):
        await self.tick()
        return

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.identity and len(message.mentions) == 1 and message.mentions[0].id == self.bot.user.id and message.author.bot is False:
            reply = random.choice(self.identity['replies'])
            await message.channel.send(reply, reference=message)
            #print(reply)


    async def tick(self):
        if self.identity:
            await self.choose_identity()
            #await self.bot.user.edit(username=self.identity['name'])
            #await self.bot.get_guild(144894829199884288).get_member(self.bot.user.id).edit(nick=self.identity['name'])
            #await self.bot.change_presence(activity=discord.Status.offline)
            activity = random.choice(self.identity['activities'])
            await self.bot.change_presence(activity=discord.Game(activity))
            #print(activity)

    async def choose_identity(self):
        identities = await self.config.identities()
        identityId = random.choice(list(identities))
        identityId = "tybalt"
        if self.identityId != identityId:
            self.identityId = identityId
            self.identity = identities[self.identityId]
            #print(self.bot.user.avatar)
