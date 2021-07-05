import discord
import datetime
import random
from dateutil import relativedelta
from redbot.core import checks, commands
from redbot.core import Config

class TybaltRip(commands.Cog):
    """TybaltRip."""

    def __init__(self):
        super().__init__()

    @commands.command(pass_context=True, no_pm=False)
    async def rip(self, ctx, *item):
        """Present a RIP embed for registered skills
        Example:
        !rip soi
        """

        key = " ".join(item).lower()
        if key:
            await self.named_rip(ctx, key)
        else:
            await self.random_rip(ctx)

    async def named_rip(self, ctx, key):
        rips = self.get_rips()
        if key in rips:
            await ctx.send("", embed=self.format_rip(rips[key]))

    async def random_rip(self, ctx):
        rips = self.get_rips()
        rip = random.choice(list(rips.values()))
        await ctx.send("", embed=self.format_rip(rip))


    def format_rip(self, rip):
        title = "RIP {}".format(rip['title'])
        action = self.random_action()
        now = datetime.datetime.now()
        r = relativedelta.relativedelta(now, rip['date'])
        duration = []
        if r.years > 0:
            if r.years == 1:
                duration.append("1 year")
            else:
                duration.append("{} years".format(r.years))
        if r.months > 0:
            if r.months == 1:
                duration.append("1 month")
            else:
                duration.append("{} months".format(r.months))
        if r.days > 0:
            if r.days == 1:
                duration.append("1 day")
            else:
                duration.append("{} days".format(r.months))
        duration = ", ".join(duration)
        quote = "*\u201C{}\u201D*".format(rip['quote'])
        date = rip['date'].strftime("%B %d, %Y")

        description = "{} {} ago.\n\n{}\nArenaNet, {}".format(action, duration, quote, date)
        embed = discord.Embed(title=title, description=description, colour=rip['color'])
        embed.set_thumbnail(url=rip['icon'])
        return embed

    def random_action(self):
        actions = ['Nerfed','Destroyed','Murdered', 'Butchered', 'Slaughtered']
        return random.choice(actions)


    def get_rips(self):
        rips = {'soi': {'title': 'Signet of Inspiration',
                        'color': 0x660066,
                        'icon': 'https://wiki.guildwars2.com/images/e/ed/Signet_of_Inspiration.png',
                        'date': datetime.datetime(2018, 12, 11),
                        'quote': 'The active effect of this signet no longer shares the mesmer\'s boons with allies'},
                'sa':  {'title': 'Shattered Aegis',
                        'color': 0x006666,
                        'icon': 'https://wiki.guildwars2.com/images/d/d0/Shattered_Aegis.png',
                        'date': datetime.datetime(2018, 12, 11),
                        'quote': 'This trait can no longer critically hit.'}}
        return rips

