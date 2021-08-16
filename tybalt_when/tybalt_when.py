import discord
from redbot.core import commands
from datetime import datetime
from dateutil import parser
import urllib.parse
import aiohttp
import json

class TybaltWhen(commands.Cog):
    """TybaltWhen."""

    @commands.command(pass_context=True, no_pm=True)
    async def when(self, ctx, *filters):
        """Give the expected date of the next patch
        *Uses that_shaman's timer*

        Example:
        !when
        """

        try:
            url = "https://www.thatshaman.com/tools/countdown/?format=json"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as r:
                    data = await r.text()
                    status = r.status
            parsed = json.loads(data)
        except:
            parsed = json.loads('{}')

        if 'when' in parsed and 'confirmed' in parsed:
            message = ""
            when = parsed['when']
            date = parser.parse(when)

            # New method (uses discord time codes)
            ts = int(datetime.timestamp(date))
            if parsed['confirmed']:
                message = "The next update will be <t:{:d}:R>.".format(ts)
            else:
                message = "The next update should be <t:{:d}:R>".format(ts)

            # Old method
            # now =  datetime.now()
            # delta = date - datetime.now()
            #
            #if (date < now):
            #    if delta.days > -2 and delta.days < 2:
            #        message = "very soon !"
            #    else:
            #        message = "in the past !"
            #else:
            #    if delta.days == 0:
            #        if (delta.seconds < 3*60*60):
            #            message = "soon !"
            #        else:
            #            message = "today !"
            #    elif delta.days == 1:
            #        message = "tomorrow !"
            #    else:
            #        message = "in {} days ({})".format(delta.days, date.strftime("%B %d, %Y"))
            #if parsed['confirmed']:
            #    message = "The next update will be {}".format(message)
            #else:
            #    message = "The next update should be {}".format(message)
            await ctx.send(message, reference=ctx.message)
        else:
            await ctx.send('Sorry, I have no idea.', reference=ctx.message)


    @commands.command(pass_context=True, no_pm=True)
    async def eod(self, ctx, *filters):
        """Gives a timer until EoD release
        *Uses that_shaman's timer*

        Example:
        !when
        """

        try:
            url = "https://www.thatshaman.com/tools/eod/?format=json"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as r:
                    data = await r.text()
                    status = r.status
            parsed = json.loads(data)
        except:
            parsed = json.loads('{}')

        if 'when' in parsed:
            message = ""
            when = parsed['when']
            date = parser.parse(when)

            ts = int(datetime.timestamp(date))
            message = "End of Dragons will release <t:{:d}:R> (<t:{:d}:D>).".format(ts, ts)

            await ctx.send(message, reference=ctx.message)
        else:
            await ctx.send('Sorry, I have no idea.', reference=ctx.message)

