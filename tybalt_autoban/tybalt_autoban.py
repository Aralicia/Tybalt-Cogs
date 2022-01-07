import discord
from redbot.core import checks, commands
from redbot.core import Config

class TybaltAutoban(commands.Cog):
    """TybaltAutoban."""

    def __init__(self):
        super().__init__()
        self.config = Config.get_conf(self, identifier=1840351931)
        default_guild = {
                'ban_like': [],
                'ban_regex': []
        }
        self.config.register_guild(**default_guild)

    @commands.command(pass_context=True, no_pm=True, aliases=["autoban"])
    @checks.has_permissions(ban_members=True)
    async def autoban_add(self, ctx, *match):
        """Add a term to the autoban filter
        Example:
        !autoban_add "Zythas"
        """

        msg = " ".join(match).lower()
        matches = await self.config.guild(ctx.guild).ban_like()
        if msg not in matches:
            matches.append(msg)
            await self.config.guild(ctx.guild).ban_like.set(matches)
            await ctx.message.channel.send("Added to autoban : `{}`".format(msg))
        else:
            await ctx.message.channel.send("Already in autoban : `{}`".format(msg))

    @commands.command(pass_context=True, no_pm=True)
    @checks.has_permissions(ban_members=True)
    async def autoban_del(self, ctx, *match):
        """Removes a term to the autoban filter
        Example:
        !autoban_del "Zythas"
        """

        msg = " ".join(match)
        matches = await self.config.guild(ctx.guild).ban_like()
        if msg in matches:
            matches.remove(msg)
            await self.config.guild(ctx.guild).ban_like.set(matches)
            await ctx.message.channel.send("Removed from autoban : `{}`".format(msg))
        else:
            await ctx.message.channel.send("Not in autoban : `{}`".format(msg))


    @commands.command(pass_context=True, no_pm=True)
    @checks.has_permissions(ban_members=True)
    async def autoban_list(self, ctx, *match):
        matches = await self.config.guild(ctx.guild).ban_like()
        msg = "\n".join(matches)
        await ctx.message.channel.send("List of autoban filters : \n{}".format(msg))


    @commands.Cog.listener()
    async def on_member_join(self, member):
        member_name = member.name.lower()
        matches = await self.config.guild(member.guild).ban_like()
        for match in matches:
            if match in member_name:
                print("Ban ! ({})".format(member.name))
                await member.ban(reason="Autoban : {}".format(match))
                break

