import discord
from discord import MessageType
from redbot.core import commands
from datetime import datetime
from dateutil import parser
import urllib.parse
import aiohttp
import json
import random
import copy
import re

class TybaltWhen(commands.Cog):
    """TybaltWhen."""

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True)
    async def when(self, ctx, *filters):
        """Give the expected date of the next patch
        *Uses that_shaman's timer*

        Example:
        !when
        """
        await self.do_when(ctx.message)

    @commands.Cog.listener()
    async def on_message(self, message):
        author = message.author
        if author.bot == False and message.guild is not None and message.type == MessageType.default:
            lower = message.content.lower()
            if re.match('.*(when|next) [^.,!?]*(patch|update)[^.,!?]*\?.*', lower) or re.match('.*(patch|update) [^.,!?]*(when|next)[^.,!?]*\?.*', lower):
                await self.do_when(message)
            elif re.match('.*(when|next) [^.,!?]*(guild chat|stream)[^.,!?]*\?', lower) or re.match('(guild chat|stream) [^.,!?]*(when|next)[^.,!?]*\?.*', lower):
                msg = copy.copy(message)
                msg.content = "!guildchat"
                await self.bot.get_cog('CustomCommands').on_message_without_command(msg)
        pass

    async def do_when(self, message):
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
            msg = ""
            when = parsed['when']
            date = parser.parse(when)

            # New method (uses discord time codes)
            ts = int(datetime.timestamp(date))
            joker = random.randrange(0, 10);
            if random.randrange(1, 20) ==1 :
                msg = random.choice([
                    "The next update will be `Soon™️`.",
                    "The next update `is on the table™️`.",
                    "The next update will be <t:{:d}:R>, I think.".format(ts + random.randrange(-18000, 18000)),
                    "The next update will be <t:{:d}:R>, I think.".format(ts + 31536000),
                    "The last update was <t:{:d}:R>, I believe.".format(0),
                    "The next update is `coming`, it seems.",
                    "The next update is  <t:{:d}:R>, maybe. I'm sorry, you didn't specify which update.".format(ts - 31536000),
                    "The next update is `somewhere in the queue`.",
                    "I don't know, for which update ? The previous one ?"
                ])
            elif parsed['confirmed']:
                msg = "The next update will be <t:{:d}:R>.".format(ts)
            else:
                msg = "The next update should be <t:{:d}:R>".format(ts)

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
            await message.channel.send(msg, reference=message)
        else:
            await message.channel.send('Sorry, I have no idea.', reference=message)


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

