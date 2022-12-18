import discord
import random
from redbot.core import commands
from discord import MessageType

class TybaltRainbow(commands.Cog):
    """Tybalt Rainbow."""

    @commands.Cog.listener()
    async def on_message(self, message):
        author = message.author
        if author.bot == False and message.guild is not None and message.type == MessageType.default:
            rainbow_roles = self.get_rainbow_roles(message.guild)
            if rainbow_roles:
                if (self.is_rainbowed(author, rainbow_roles) == False):
                    role = random.choice(rainbow_roles)
                    await author.add_roles(role)

    @commands.command(pass_context=True, no_pm=True)
    async def rainbow(self, ctx):
        message = ctx.message
        author = message.author
        if author.bot == False and message.guild is not None:
            rainbow_roles = self.get_rainbow_roles(message.guild)
            if rainbow_roles:
                for role in rainbow_roles:
                    if (role in author.roles):
                        await author.remove_roles(role)
                role = random.choice(rainbow_roles)
                await author.add_roles(role)
            await message.delete()

    def get_rainbow_roles(self, guild):
        rolenames = ["Green", "Orange", "Yellow", "Purple", "Blue", "Red", "Pink", "Other Pink"]
        rainbow_roles = []
        roles = guild.roles
        for role in roles:
            if role.name in rolenames:
                rainbow_roles.append(role)
        return rainbow_roles


    def is_rainbowed(self, author, roles):
        for role in roles:
            if (role in author.roles):
                return True
        return False

