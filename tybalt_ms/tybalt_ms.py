import asyncio
import discord
import random
import sys
from redbot.core import checks, commands
from redbot.core import Config
from collections import namedtuple

class TybaltMegaserver(commands.Cog):
    """TybaltMegaserver."""

    def __init__(self, bot):
        self.bot = bot
        self.roles = [
                { 'role' : None, 'emoji' : '\N{ROBOT FACE}', 'name' : 'Bot', 'description' : 'You are a bot, and are trying to infiltrate the discord.' },
                { 'role' : 'guest', 'emoji' : '\N{BUST IN SILHOUETTE}', 'name' : 'Guest', 'description' : 'You don\'t play or you don\'t want to tell on which megaserver you play.' },
                { 'role' : 'na', 'emoji' : '\N{REGIONAL INDICATOR SYMBOL LETTER U}\N{REGIONAL INDICATOR SYMBOL LETTER S}', 'name' : 'NA', 'description' : 'You play on the NA megaserver.' },
                { 'role' : 'eu', 'emoji' : '\N{REGIONAL INDICATOR SYMBOL LETTER E}\N{REGIONAL INDICATOR SYMBOL LETTER U}', 'name' : 'EU', 'description' : 'You play on the EU megaserver.' },
                { 'role' : 'f2p', 'emoji' : '\N{SQUARED FREE}', 'name' : 'F2P', 'description' : 'You play on a f2p account, without the expansions.'}
            ]
        self.config = Config.get_conf(self, identifier=1840255631)
        default_guild = {
                "rolechannels" : []
        }
        self.config.register_guild(**default_guild)
    
    @commands.command(pass_context=True, no_pm=True)
    @checks.has_permissions(manage_messages=True)
    async def rolechannel(self, ctx):
        channel_id = ctx.message.channel.id
        rolechannels = await self.config.guild(ctx.guild).rolechannels()
        if channel_id in rolechannels:
            rolechannels.remove(channel_id)
            await self.config.guild(ctx.guild).rolechannels.set(rolechannels)
        else:
            rolechannels.append(channel_id)
            await self.config.guild(ctx.guild).rolechannels.set(rolechannels)
            #TODO : Add role message here ?


    @commands.command(pass_context=True, no_pm=True)
    async def roles(self, ctx):
        """Display a message on which you can mention to change your roles (In dev)

        Example:
        !roles
        """
        content = "> **User Roles**\n> Use the reactions below this message to gain or lose the following roles :";

        for role in self.roles:
            content = "{}\n> {} : {} - {}".format(content, role['emoji'], role['name'], role['description'])

        message = await ctx.send(content, reference=ctx.message);

        for role in self.roles:
            await message.add_reaction(role['emoji'])
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        message, member, role = await self.get_reaction_context(payload)
        if member is not None and role is not None:
            if role == "":
                description = "It seems you have failed this IQ test; I must then conclude that you are not a member of my krewe and are, most assuredly, a skritt.\r\n\r\nAs proper lab regulations does not allow for live subjects to enter unaccompanied by a properly trained lab assistant, your access has been summarily revoked."
                embed = discord.Embed(description=description, colour=0x7F2AFF)
                embed.set_footer(text="Yerkk, Brill Alliance Labs", icon_url="https://wiki.guildwars2.com/images/d/d7/Asura_tango_icon_48px.png")
                try:
                    await member.send("", embed=embed)
                except:
                    pass
                await member.kick(reason="Identifies as a bot")
            else:
                if role not in member.roles:
                    #print("Adding {} to {}".format(role.name, member.name))
                    try:
                        await member.add_roles(role)
                    except:
                        pass
                else:
                    #print("Removing {} to {}".format(role.name, member.name))
                    try:
                        await member.remove_roles(role)
                    except:
                        pass

            await message.remove_reaction(payload.emoji, member)

    #@commands.Cog.listener()
    #async def on_raw_reaction_remove(self, payload):
    #    member, role = await self.get_reaction_context(payload)
    #    if member is not None and role is not None:
    #        if role in member.roles:
    #            await member.remove_roles(role)


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
                await ctx.send("Done ! You are now a NA player.", reference=ctx.message)
            else:
                await author.remove_roles(role_na)
                await ctx.send("Well, you **were** a NA player.", reference=ctx.message)
                #if (random.randint(0, 9) == 0):
                #    await ctx.send("Cogs and gears, can't people read ? You are already NA, so you are protected from the purge.")
                #else:
                #    await ctx.send("Role Removal has been temporarily disabled. You are already protected from the Purge.")
        except discord.Forbidden:
            await ctx.send("I need permissions to edit roles first.", reference=ctx.message)
        except Exception as e:
            print(e)
            await ctx.send("Something went wrong.", reference=ctx.message)

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
                await ctx.send("Done ! You are now a EU player.", reference=ctx.message)
            else:
                await author.remove_roles(role_eu)
                await ctx.send("Well, you **were** a EU player.", reference=ctx.message)
                #if (random.randint(0, 9) == 0):
                #    await ctx.send("Cogs and gears, can't people read ? You are already EU, so you are protected from the purge.")
                #else:
                #    await ctx.send("Role Removal has been temporarily disabled. You are already protected from the Purge")
        except discord.Forbidden:
            await ctx.send("I need permissions to edit roles first.", reference=ctx.message)
        except Exception as e:
            print(e)
            await ctx.send("Something went wrong.", reference=ctx.message)

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
                await ctx.send("Done ! You are now a F2P player.", reference=ctx.message)
            else:
                await author.remove_roles(role_f2p)
                await ctx.send("Congratulations, you are no longer a F2P player.", reference=ctx.message)
        except discord.Forbidden:
            await ctx.send("I need permissions to edit roles first.", reference=ctx.message)
        except Exception as e:
            print(e)
            await ctx.send("Something went wrong.", reference=ctx.message)


    #@commands.Cog.listener()
    #async def on_member_join(self, member):
        #role_nc = self.get_role_by_name(member.guild, "newcomer")
        #await member.add_roles(role_nc)


    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.roles != after.roles:
            roles = self.get_roles_by_name(after.guild)
            changes = self.get_roles_diff(before.roles, after.roles)
            if "eu" in roles and "na" in roles and "guest" in roles and "f2p" in roles:
                if roles["eu"] in changes.added or roles["na"] in changes.added or roles["guest"] in changes.added:
                    toremove = []
                    if roles["guest"] in changes.added:
                        if roles["eu"] in after.roles:
                            toremove.append(roles["eu"])
                        if roles["na"] in after.roles:
                            toremove.append(roles["na"])
                    if roles["eu"] in changes.added or roles["na"] in changes.added:
                        toremove.append(roles["guest"])
                    if len(toremove) > 0:
                        await after.remove_roles(*toremove)
                if roles["eu"] in changes.removed or roles["na"] in changes.removed:
                    if roles["eu"] not in after.roles and roles["na"] not in after.roles and roles["guest"] not in after.roles:
                        await after.add_roles(roles["guest"])
                if roles["f2p"] in changes.added:
                    if roles["eu"] not in after.roles and roles["na"] not in after.roles and roles["guest"] not in after.roles:
                        await after.add_roles(roles["guest"])


    def get_roles_diff(self, before, after):
        added = []
        removed = []
        for role in after:
            if role not in before:
                added.append(role)
        for role in before:
            if role not in after:
                removed.append(role)
        return namedtuple('diff', 'added removed')(added, removed)

    def get_roles_by_name(self, guild):
        roles = {}
        for role in guild.roles:
            roles[role.name.lower()] = role
        return roles

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
                            if _role['role'] is None:
                                return (message, member, "")
                            role = self.get_role_by_name(guild, _role['role'])
                            if role is not None:
                                return (message, member, role)
                return (message, member, None)
            return (None, member, None)
        except:
            print("{}".format(sys.exc_info()[0]))
        return (None, None, None)
