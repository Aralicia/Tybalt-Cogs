import discord
from redbot.core import checks, commands
from redbot.core import Config

class TybaltAds(commands.Cog):
    """Tybalt Ads Handling."""

    def __init__(self):
        super().__init__()
        self.config = Config.get_conf(self, identifier=1840251931)
        default_guild = {
                "adschannels" : []
        }
        default_channel = {
                "lastmessages" : {
                }
        }
        self.config.register_guild(**default_guild)

    @commands.command(pass_context=True, no_pm=True)
    @checks.has_permissions(manage_messages=True)
    async def adschannel(self, ctx):
        channel_id = ctx.message.channel.id
        adschannels = await self.config.guild(ctx.guild).adschannels()
        if channel_id in adschannels:
            adschannels.remove(channel_id)
            await self.config.guild(ctx.guild).adschannels.set(adschannels)
            await self.config.channel(ctx.message.channel).lastmessages.set({})
            title = "**{} is no longer an Advertisement Channel**".format(ctx.message.channel.name)
            description = "You are now free to talk as much as you want."
            embed = discord.Embed(title=title, description=description, colour=0x990000)
            await ctx.message.channel.send("", embed=embed)
        else:
            adschannels.append(channel_id)
            await self.config.guild(ctx.guild).adschannels.set(adschannels)

            title = "**{} is now an Advertisement Channel**".format(ctx.message.channel.name)
            description = "You can post in it only once per week."
            embed = discord.Embed(title=title, description=description, colour=0x990000)
            await ctx.message.channel.send("", embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is not None:
            adschannels = await self.config.guild(message.guild).adschannels()
            if message.channel.id in adschannels and message.author.bot is False:
                author = message.author
                author_id = str(author.id)
                lastmessages = await self.config.channel(message.channel).lastmessages()
                if (lastmessages is None):
                    lastmessages = {}
                created_at = message.created_at.timestamp()
                if author_id in lastmessages :
                    if (created_at - lastmessages[author_id]) > 604800: # 7 days
                        lastmessages[author_id] = created_at
                        await self.config.channel(message.channel).lastmessages.set(lastmessages)
                    else:
                        if message.channel.permissions_for(author).manage_messages == False :
                            await message.delete()
                            await message.channel.send('*Message deleted. You have already posted a message in the last 7 days.*', delete_after=15)
                else:
                    lastmessages[author_id] = created_at
                    await self.config.channel(message.channel).lastmessages.set(lastmessages)

