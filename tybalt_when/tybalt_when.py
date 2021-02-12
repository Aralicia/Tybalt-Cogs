import discord
from redbot.core import commands
from datetime import datetime
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

        print(parsed)
        if 'when' in parsed and 'confirmed' in parsed:
            message = ""
            when = parsed['when'][:-6]
            date = datetime.strptime(when, '%Y-%m-%dT%H:%M:%S')
            now =  datetime.now()
            delta = date - datetime.now()

            if (date < now):
                if delta.days > -2 and delta.days < 2:
                    message = "very soon !"
                else:
                    message = "in the past !"
            else:
                if delta.days == 0:
                    if (delta.seconds < 3*60*60):
                        message = "soon !"
                    else:
                        message = "today !"
                elif delta.days == 1:
                    message = "tomorrow !"
                else:
                    message = "in {} days ({})".format(delta.days, date.strftime("%B %d, %Y"))
            if parsed['confirmed']:
                message = "The next update will be {}".format(message)
            else:
                message = "The next update should be {}".format(message)
            await ctx.send(message, reference=ctx.message)
        else:
            await ctx.send('Sorry, I have no idea.', reference=ctx.message)

