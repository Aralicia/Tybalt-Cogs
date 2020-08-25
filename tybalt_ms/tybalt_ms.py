import discord
import random
from redbot.core import commands

class TybaltMegaserver(commands.Cog):
    """TybaltMegaserver."""

    @commands.command(pass_context=True, no_pm=True, aliases=["NA"])
    async def na(self, ctx):
        """Join NA group/rolee

        Example:
        !na
       """
        author = ctx.message.author
        role_na = self.get_role_by_name(ctx.message.guild, "na")
        try:
            if role_na not in author.roles:
                await author.add_roles(role_na)
                await ctx.send("Done ! You are now a NA player.")
            else:
                await author.remove_roles(role_na)
                await ctx.send("Well, you **were** a NA player.")
                #if (random.randint(0, 9) == 0):
                #    await ctx.send("Cogs and gears, can't people read ? You are already NA, so you are protected from the purge.")
                #else:
                #    await ctx.send("Role Removal has been temporarily disabled. You are already protected from the Purge.")
        except discord.Forbidden:
            await ctx.send("I need permissions to edit roles first.")
        except Exception as e:
            print(e)
            await ctx.send("Something went wrong.")

    @commands.command(pass_context=True, no_pm=True, aliases=["EU"])
    async def eu(self, ctx):
        """Join EU group/rolee

        Example:
        !eu
       """
        author = ctx.message.author
        role_eu = self.get_role_by_name(ctx.message.guild, "eu")
        try:
            if role_eu not in author.roles:
                await author.add_roles(role_eu)
                await ctx.send("Done ! You are now a EU player.")
            else:
                await author.remove_roles(role_eu)
                await ctx.send("Well, you **were** a EU player.")
                #if (random.randint(0, 9) == 0):
                #    await ctx.send("Cogs and gears, can't people read ? You are already EU, so you are protected from the purge.")
                #else:
                #    await ctx.send("Role Removal has been temporarily disabled. You are already protected from the Purge")
        except discord.Forbidden:
            await ctx.send("I need permissions to edit roles first.")
        except Exception as e:
            print(e)
            await ctx.send("Something went wrong.")

    @commands.command(pass_context=True, no_pm=True, aliases=["F2P"])
    async def f2p(self, ctx):
        """Join F2P group/role

        Example:
        !f2p
       """
        author = ctx.message.author
        role_f2p = self.get_role_by_name(ctx.message.guild, "f2p")
        try:
            if role_f2p not in author.roles:
                await author.add_roles(role_f2p)
                await ctx.send("Done ! You are now a F2P player.")
            else:
                await author.remove_roles(role_f2p)
                await ctx.send("Congratulations, you are no longer a F2P player.")
        except discord.Forbidden:
            await ctx.send("I need permissions to edit roles first.")
        except Exception as e:
            print(e)
            await ctx.send("Something went wrong.")


    def get_role_by_name(self, guild, name):
        roles = guild.roles
        for role in roles:
            if role.name.lower() == name.lower():
                return role

