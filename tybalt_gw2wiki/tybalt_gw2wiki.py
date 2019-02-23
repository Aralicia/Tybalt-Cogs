import discord
from redbot.core import commands
import urllib.parse
import aiohttp
import json

class TybaltWiki(commands.Cog):
    """TybaltWiki."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True)
    async def wiki(self, ctx, *search):
        """Search on the Guild Wars 2 wiki
        Example:
        !wiki "Game Updates"
        """

        try:
            await ctx.trigger_typing()

            msg = " ".join(search)
            f = { 'search' : msg}

            # uses the wiki API to do a real search. Links for articles are posted if there is any
            url = "https://wiki.guildwars2.com/api.php?action=opensearch&limit=11&redirects=resolve&"+urllib.parse.urlencode(f)

            async with aiohttp.ClientSession() as session:
                async with session.get(url) as r:
                    data = await r.text()
                    status = r.status

            try:
                parsed = json.loads(data)
            except:
                parsed = json.loads('{}')

            res = ""

            if len(parsed[3]) > 0:

                i = 0
                for a in parsed[3]:
                    i = i + 1
                    if i <= 10: #prevents it to show more than 10 results
                        res = "{}\n<{}>".format(res,a)
                    else:
                        break

                if len(parsed[3]) > 1: #if there are more than 1 result, show this plus the results, otherwise, shows the link right away
                    res = "Ok, I have found these results for \"{}\":\n{}".format(msg,res)

                    if len(parsed[3]) > 10: #if it found more than 10 results, show a notice plus a link to the full search page (similar to the old one)
                        link = "http://wiki.guildwars2.com/index.php?title=Special%3ASearch&fulltext=1&"+urllib.parse.urlencode(f) #the "fulltext" param is to avoid a redirect in case there is a page matching exactly the search terms
                        res = "{}\n\nMore than 10 results were found and these are just the first 10.\nTry to narrow your search terms to be more specific or check the full results at <{}>.".format(res,link)

                await ctx.send("{}".format(res))

            else:
                await ctx.send("Hmm, nothing was found for \"{}\".".format(msg))

        except Exception as e:
            print(e)
            await ctx.send("Something went wrong.")

