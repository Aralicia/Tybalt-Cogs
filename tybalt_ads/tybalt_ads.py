import re
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

    @commands.command(pass_context=True, no_pm=True)
    @checks.has_permissions(manage_messages=True)
    async def adsallow(self, ctx, user: discord.Member):
        adschannels = await self.config.guild(ctx.message.guild).adschannels()
        if ctx.message.channel.id in adschannels and user is not None:
            user_id = str(user.id)
            lastmessages = await self.config.channel(ctx.message.channel).lastmessages()
            if (lastmessages is None):
                lastmessages = {}
            if user_id in lastmessages :
                del lastmessages[user_id]
                await self.config.channel(ctx.message.channel).lastmessages.set(lastmessages)
                await ctx.message.delete()
                await ctx.message.channel.send('*Done. User {} can now post again.*'.format(user.mention), delete_after=360)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is not None:
            adschannels = await self.config.guild(message.guild).adschannels()
            ok = (message.channel.id in adschannels and message.author.bot is False)
            if ok:
                ok = await self.verify_message_rules(message)
            if ok:
                ok = await self.verify_post_rules(message)

    async def verify_message_rules(self, message):
        message_content = message.content
        rules = ""
        lines_pattern = r'(\r\s*\r|\n\s*\n|\r\n\s*\r\n)'
        #print('verify_message_rules');
        #print(message.author);
        #print(len(re.findall(lines_pattern, message_content)))

        if len(re.findall(lines_pattern, message_content)) > 5:
            rules = "{}\n- {}".format(rules, "No more than five empty lines")
        if len(rules) > 0:
            await self.remove(message, '*Message deleted. It did not respect the following rules:*{}'.format(rules))
            return False
        return True


    async def verify_post_rules(self, message):
        author = message.author
        author_id = str(author.id)
        lastmessages = await self.config.channel(message.channel).lastmessages()
        if (lastmessages is None):
            lastmessages = {}
        created_at = message.created_at.timestamp()
        if author_id in lastmessages :
            if (created_at - lastmessages[author_id]) > 590400: # 6 days, 20 hours ; was 604800: # 7 days
                lastmessages[author_id] = created_at
                await self.config.channel(message.channel).lastmessages.set(lastmessages)
            else:
                await self.remove(message, '*Message deleted. You have already posted a message in the last 7 days.*')
                return False
        else:
            lastmessages[author_id] = created_at
            await self.config.channel(message.channel).lastmessages.set(lastmessages)
        return True

    async def remove(self, message, reason):
        if message.channel.permissions_for(message.author).manage_messages == False :
            await message.delete()
            await message.channel.send(reason, delete_after=15)
