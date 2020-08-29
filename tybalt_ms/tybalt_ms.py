import asyncio
import discord
import random
import sys
from redbot.core import commands

class TybaltMegaserver(commands.Cog):
    """TybaltMegaserver."""

    def __init__(self, bot):
        self.bot = bot
        self.roles = [
                { 'role' : 'na', 'emoji' : '\N{REGIONAL INDICATOR SYMBOL LETTER U}\N{REGIONAL INDICATOR SYMBOL LETTER S}', 'name' : 'NA', 'description' : 'You play on the NA megaserver.'},
                { 'role' : 'eu', 'emoji' : '\N{REGIONAL INDICATOR SYMBOL LETTER E}\N{REGIONAL INDICATOR SYMBOL LETTER U}', 'name' : 'EU', 'description' : 'You play on the EU megaserver.'},
                { 'role' : 'f2p', 'emoji' : '\N{SQUARED FREE}', 'name' : 'F2P', 'description' : 'You play on a f2p account, without the expansions.'}
            ]

    @commands.command(pass_context=True, no_pm=True)
    async def roles(self, ctx):
        """Display a message on which you can mention to change your roles (In dev)

        Example:
        !roles
        """
        content = "> **User Roles**\n> Use the reactions below this message to gain or lose the following roles :";

        for role in self.roles:
            content = "{}\n> {} : {} - {}".format(content, role['emoji'], role['name'], role['description'])

        message = await ctx.send(content);

        for role in self.roles:
            await message.add_reaction(role['emoji'])
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        member, role = await self.get_reaction_context(payload)
        if member is not None and role is not None:
            if role not in member.roles:
                await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        member, role = await self.get_reaction_context(payload)
        if member is not None and role is not None:
            if role in member.roles:
                await member.remove_roles(role)


    @commands.command(pass_context=True, no_pm=True, aliases=["NA"])
    async def na(self, ctx):
        """Join NA group/role

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
        """Join EU group/role

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

    async def get_reaction_context(self, payload):
        try:
            guild = self.bot.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            channel = guild.get_channel(payload.channel_id)
            emoji = payload.emoji

            if not member.bot:
                message = await channel.fetch_message(payload.message_id)
                if message.author == guild.me:
                    for _role in self.roles:
                        if (emoji.name == _role['emoji']):
                            role = self.get_role_by_name(guild, _role['role'])
                            if role is not None:
                                return (member, role)
        except:
            print("{}".format(sys.exc_info()[0]))
        return (member, None)
