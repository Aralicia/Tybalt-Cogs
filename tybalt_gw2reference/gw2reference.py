import discord
from itertools import islice
from redbot.core import commands
from .gw2entities import GW2Entities, EntityType
from .gw2embed import GW2Embed

class TybaltGW2Reference(commands.Cog):
    """TybaltGW2Reference."""

    def __init__(self, bot):
        self.bot = bot
        self.embed = GW2Embed(bot)
        self.entities = GW2Entities(bot)

    @commands.command(pass_context=True, no_pm=True)
    async def item(self, ctx, *data):
        """Describe a item

        Example:
        !item Sword
        """

        await ctx.trigger_typing()

        name = " ".join(data)
        if name.isdigit():
            items = await self.entities.findById(name, EntityType.item())
        else:
            items = await self.entities.findByName(name, EntityType.item(), 9+25)

        if items[1] == 0:
            await ctx.send("I've not found anything, sorry.")
        elif items[1] == 1:
            embed = await self.embed.item(items[0][0]['id'], None, ctx.message.guild.emojis)
            await ctx.send(embed=embed)
        else:
            tabmessages = self.bot.get_cog("TabMessages")
            message = tabmessages.TabMessage()
            for idx, item in enumerate(islice(items[0], 9), start=1):
                embed = await self.embed.item(item['id'], None, ctx.message.guild.emojis)
                message.addTab(embed, str(idx) + u"\u20E3")

            if items[1] > 9:
                extracount = items[1] - (9+25)
                if extracount < 0:
                    extracount = 0
                embed = await self.embed.entityList(items[0][9:], extracount)
                message.addTab(embed, u"\U0001F4C4")

            await tabmessages.send(message, ctx.message.channel)

    @commands.command(pass_context=True, no_pm=True)
    async def recipe(self, ctx, *data):
        """Describe a recipe

        Example:
        !recipe Sword
        """

        await ctx.trigger_typing()

        name = " ".join(data)
        if name.isdigit():
            items = await self.entities.findById(name, EntityType.recipe())
        else:
            items = await self.entities.findByName(name, EntityType.recipe(), 9+25)

        if items[1] == 0:
            await ctx.send("I've not found anything, sorry.")
        elif items[1] == 1:
            embed = await self.embed.recipe(items[0][0]['id'], None, ctx.message.guild.emojis)
            await ctx.send(embed=embed)
        else:
            tabmessages = self.bot.get_cog("TabMessages")
            message = tabmessages.TabMessage()
            for idx, recipe in enumerate(islice(items[0], 9), start=1):
                embed = await self.embed.recipe(recipe['id'], None, ctx.message.guild.emojis)
                message.addTab(embed, str(idx) + u"\u20E3")

            if items[1] > 9:
                extracount = items[1] - (9+25)
                if extracount < 0:
                    extracount = 0
                embed = await self.embed.entityList(items[0][9:], extracount)
                message.addTab(embed, u"\U0001F4C4")

            await tabmessages.send(message, ctx.message.channel)

    @commands.command(pass_context=True, no_pm=True)
    async def test_skin(self, ctx, *data):
        """Describe a skin

        Example:
        !skin Sword
        """

        await ctx.trigger_typing()

        name = " ".join(data)
        if name.isdigit():
            items = await self.entities.findById(name, EntityType.skin())
        else:
            items = await self.entities.findByName(name, EntityType.skin(), 9+25)

        if items[1] == 0:
            await ctx.send("I've not found anything, sorry.")
        elif items[1] == 1:
            embed = await self.embed.skin(items[0][0]['id'], None, ctx.message.guild.emojis)
            await ctx.send(embed=embed)
        else:
            tabmessages = self.bot.get_cog("TabMessages")
            message = tabmessages.TabMessage()
            for idx, recipe in enumerate(islice(items[0], 9), start=1):
                embed = await self.embed.skin(recipe['id'], None, ctx.message.guild.emojis)
                message.addTab(embed, str(idx) + u"\u20E3")

            if items[1] > 9:
                extracount = items[1] - (9+25)
                if extracount < 0:
                    extracount = 0
                embed = await self.embed.entityList(items[0][9:], extracount)
                message.addTab(embed, u"\U0001F4C4")

            await tabmessages.send(message, ctx.message.channel)

    @commands.command(pass_context=True, no_pm=True)
    async def test_skill(self, ctx, *data):
        """Describe a skill

        Example:
        !skill Impale
        """

        await ctx.trigger_typing()

        name = " ".join(data)
        if name.isdigit():
            items = await self.entities.findById(name, EntityType.skill())
        else:
            items = await self.entities.findByName(name, EntityType.skill(), 9+25)

        if items[1] == 0:
            await ctx.send("I've not found anything, sorry.")
        elif items[1] == 1:
            embed = await self.embed.skill(items[0][0]['id'], None, ctx.message.guild.emojis)
            await ctx.send(embed=embed)
        else:
            tabmessages = self.bot.get_cog("TabMessages")
            message = tabmessages.TabMessage()
            for idx, skill in enumerate(islice(items[0], 9), start=1):
                embed = await self.embed.skill(skill['id'], None, ctx.message.guild.emojis)
                message.addTab(embed, str(idx) + u"\u20E3")

            if items[1] > 9:
                extracount = items[1] - (9+25)
                if extracount < 0:
                    extracount = 0
                embed = await self.embed.entityList(items[0][9:], extracount)
                message.addTab(embed, u"\U0001F4C4")

            await tabmessages.send(message, ctx.message.channel)

