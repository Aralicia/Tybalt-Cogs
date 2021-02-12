import discord
from redbot.core import commands
import urllib.parse
import aiohttp
import json
import traceback

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
            results = await self.query_wiki(msg)

            if results:
                if len(results) == 1:
                    await ctx.send("{} : <{}>".format(results[0][0], results[0][1]),  reference=ctx.message)
                else:
                    res = "Ok, I have found these results for \"{}\":".format(msg)
                    for i, row in enumerate(results):
                        res = "{}\n{} : <{}>".format(res, row[0], row[1])
                        if i >= 9: #prevents it to show more than 10 results
                            break
                    if len(results) > 10:#if it found more than 10 results, show a notice plus a link to the full search page
                        link = "http://wiki.guildwars2.com/index.php?title=Special%3ASearch&fulltext=1&"+urllib.parse.urlencode({'search' : msg}) #the "fulltext" param is to avoid a redirect in case there is a page matching exactly the search terms
                        res = "{}\n\nMore than 10 results were found and these are just the first 10.\nTry to narrow your search terms to be more specific or check the full results at <{}>.".format(res,link)
                    await ctx.send("{}".format(res),  reference=ctx.message)
            else:
                await ctx.send("Hmm, nothing was found for \"{}\".".format(msg), reference=ctx.message)

        except Exception as e:
            print(e)
            traceback.print_exc()
            await ctx.send("Something went wrong.", reference=ctx.message)

    @commands.command(pass_context=True, no_pm=True)
    async def wikus(self, ctx, *search):
        """Search for an exact match on the Guild Wars 2 wiki
        Example:
        !wikus "Game Updates"
        """

        try:
            await ctx.trigger_typing()

            msg = " ".join(search)
            results = await self.query_wiki(msg)
            msg = msg.lower();

            for row in results:
                if (row[0].lower() == msg or msg == ""):
                    await ctx.send("{} : <{}>".format(row[0], row[1]), reference=ctx.message)
                    return
            await ctx.send("Hmm, nothing was found for \"{}\".".format(msg), reference=ctx.message)
        except Exception as e:
            print(e)
            await ctx.send("Something went wrong.", reference=ctx.message)

    async def query_wiki(self, keyword):
        try:
            if not keyword:
                return [ ('Wiki', 'https://wiki.guildwars2.com/') ]

            f = { 'search' : keyword }
            url = "https://wiki.guildwars2.com/api.php?action=opensearch&limit=11&redirects=resolve&format=json&"+urllib.parse.urlencode(f)
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as r:
                    data = await r.text()
                    status = r.status
            
            parsed = json.loads(data)
        except:
            parsed = json.loads('{}')
        
        results = []
        if len(parsed[1]) > 0:
            for i, title in enumerate(parsed[1]):
                results.append([title, parsed[3][i]])

        return results
