import discord
from redbot.core import commands
from urllib import parse
import aiohttp
import json
import traceback
from collections import Counter
import asyncio

class WikiSession:
    def __init__(self):
        self.session = None
        self.base_url = "https://wiki.guildwars2.com/"
    
    async def login(self):
        if self.session is None:
            return await self.prepare_session()
        else:
            pass #no login necessary. yet.

    async def opensearch(self, search, limit=11):
        return await self.api('opensearch', parameters = {
            "limit" : limit,
            "redirects" : "resolve",
            "search" : search
        })

    async def api(self, action, parameters={}):
        parameters["action"] = action;
        parameters["format"] = "json";
        data = await self.raw('api.php?'+parse.urlencode(parameters))
        parsed = json.loads(data)
        return parsed

    async def raw(self, query):
        await self.prepare_session()
        url = self.base_url + query
        try:
            r = await self.session.get(url)
            if (r.status >= 300):
                print('http error : {}'.format(r.status))
                print(await r.text())
                data = "[]"
            else:
                data = await r.text()
        except Exception as e:
            print(e)
            data = "[]"
        return data

    async def prepare_session(self):
        if self.session is None:
            headers = {
                "User-Agent":"TybaltBot/v2",
                #"User-Agent":"Mozilla/5.0 (Windows NT 6.2; WOW64; rv:17.0) Gecko/20100101 Firefox/17.0",
            }
            self.session = aiohttp.ClientSession(headers=headers)
            await self.login()

    def unload(self):
        if self.session is not None:
            asyncio.create_task(self.session.close())


class TybaltWiki(commands.Cog):
    """TybaltWiki."""
    def __init__(self, bot):
        self.bot = bot
        self.wiki = WikiSession()

    def cog_unload(self):
        self.wiki.unload()

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
                        link = "https://wiki.guildwars2.com/index.php?title=Special%3ASearch&fulltext=1&"+parse.urlencode({'search' : msg}) #the "fulltext" param is to avoid a redirect in case there is a page matching exactly the search terms
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

    @commands.command(aliases=["gs", "GS"], pass_context=True, no_pm=True)
    async def gearsearch(self, ctx, *search):
        """Run the Equipment Query with the given parameters
        Example:
        !gearsearch ascended viper trinkets
        """

        try:
            query_params = {
                    "title" : "Special:RunQuery/Equipment_query",
                    "pfRunQueryFormName" : "Equipment query",
                    "Equipment query[rarity]" : "",
                    "Equipment query[supertype]" : "",
                    "Equipment query[type]" : "",
                    "Equipment query[class]" : "",
                    "Equipment query[prefix]" : "",
                    "Equipment query[exclude selectable]" : "",
                    "Equipment query[offset]" : 0
                    }
            keywords = " ".join(search).lower()
            title = []

            prefix = self.guess_prefix(keywords)
            if prefix is not None:
                query_params["Equipment query[prefix]"] = prefix
                title.append("{}'s".format(prefix.capitalize()))

            rarity = self.guess_rarity(keywords)
            if rarity is not None:
                query_params["Equipment query[rarity]"] = rarity
                title.append(rarity)
            
            item_type = self.guess_weapon_type(keywords)
            if item_type is None:
                item_type = self.guess_armor_type(keywords)
            if item_type is None:
                item_type = self.guess_trinket_type(keywords)
            if item_type is not None:
                for key in item_type:
                    query_params["Equipment query["+key+"]"] = item_type[key]
                title = title + list(item_type.values())

            title = "Wiki Equipment Query : " + " ".join(title)
            url = "https://wiki.guildwars2.com/wiki/Special:RunQuery/Equipment_query?{}".format(parse.urlencode(query_params))
            em = discord.Embed(title=title, url=url)
            await ctx.channel.send(content=None, embed=em, reference=ctx.message)

        except Exception as e:
            print(e)
            await ctx.send("Something went wrong.", reference=ctx.message)

    @commands.command(pass_context=True, no_pm=True)
    async def gallery(self, ctx, *search):
        """Search the wiki galleries associated to the given parameters
        Example:
        !gallery human heavy armor
        """

        #msg = " ".join(search)
        #link = "https://wiki.guildwars2.com/index.php?title=Special%3ASearch&fulltext=1&"+parse.urlencode({'search' : msg})
        #await ctx.send("Due to changes in the Guild Wars 2 Wiki, this command is temporarily unavailable.\r\nYou can find a list of galleries here : <https://wiki.guildwars2.com/wiki/Category:Item_galleries_by_type>", reference=ctx.message)
        #return None

        try:
            await ctx.trigger_typing()
            keywords = list(search)
            
            # special plural cases
            if 'focus' in keywords:
                keywords.append("foci");
            if 'staff' in keywords:
                keywords.append("staves");

            item_results = await self.query_wiki_category('Category:Item_galleries_by_type', keywords)
            armor_results = await self.query_wiki_category('Category:Armor', keywords)
            results = item_results + armor_results
            max_weight = max([sublist[0] for sublist in results])
            results = [entry for entry in results if entry[0] == max_weight];

            if results:
                if len(results) == 1:
                    await ctx.send("{} : <{}>".format(results[0][1], results[0][2]),  reference=ctx.message)
                elif len(results) < 11:
                    res = "Ok, I have found these galleries for \"{}\":".format(" ".join(search))
                    for i, row in enumerate(results):
                        res = "{}\n{} : <{}>".format(res, row[1], row[2])
                    await ctx.send("{}".format(res),  reference=ctx.message)
                else:
                    await ctx.send("I found too many results for \"{}\". Be more precise, please.".format(" ".join(search)), reference=ctx.message)
            else:
                await ctx.send("Hmm, no gallery was found for \"{}\".".format(" ".join(search)), reference=ctx.message)

        except Exception as e:
            print(e)
            await ctx.send("Something went wrong.", reference=ctx.message)



    async def query_wiki(self, keyword):
        if not keyword:
            return [ ('Wiki', 'https://wiki.guildwars2.com/') ]

        parsed = await self.wiki.opensearch(keyword)
        results = []
        if len(parsed) > 0 and len(parsed[1]) > 0:
            for i, title in enumerate(parsed[1]):
                results.append([title, parsed[3][i]])

        return results

    async def query_wiki_category(self, category, keywords):
        if not category:
            return []

        parsed = await self.wiki.api('query', parameters = {
            "list" : "categorymembers",
            "cmprop" : "ids|title|type",
            "cmlimit" : "100",
            "cmtitle" : category,
        })

        results = []
        if 'query' in parsed and 'categorymembers' in parsed['query'] and len(parsed['query']['categorymembers']) > 0:
            for i, entry in enumerate(parsed['query']['categorymembers']):
                if entry['type'] == 'page':
                    title_parts = entry['title'].lower().split(' ')
                    matches = 0
                    for word in keywords:
                        for part in title_parts:
                            if part.startswith(word.lower()):
                                matches+=1
                                break;
                    if matches > 0:
                        results.append([matches, entry['title'], 'https://wiki.guildwars2.com/wiki/{}'.format(entry['title'].replace(' ','_'))])
        return results

    def guess_rarity(self, keywords):
        rarities = {
                "basic" : "Basic", "black" : "Basic",
                "fine" : "Fine", "blue" : "Basic",
                "masterwork" : "Masterwork", "green" : "Masterwork",
                "rare" : "Rare", "yellow" : "Rare",
                "exotic" : "Exotic", "exo" : "Exotic", "orange" : "Exotic",
                "ascended" : "Ascended", "asc" : "Ascended", "pink" : "Ascended",
                "legendary" : "Legendary", "leggy" : "Legendary", "purple" : "Legendary"
                }
        for key in rarities:
            if key in keywords:
                return rarities[key]
        return None

    def guess_weapon_type(self, keywords):
        types = {
                "axe" : "Axe", "dagger" : "Dagger", "focus" : "Focus", "greatsword" : "Greatsword", "hammer" : "Hammer", "longbow" : "Longbow", "mace" : "Mace", "pistol" : "Pistol", "rifle" : "Rifle", "scepter" : "Scepter", "shield" : "Shield", "short bow" : "Short bow", "staff" : "Staff", "sword" : "Sword", "torch" : "Torch", "warhorn": "Warhorn", "spear" : "Spear", "harpoon gun" : "Harpoon gun", "trident" : "Trident",
                "long bow" : "longbow", "shortbow" : "Short bow", "horn" : "Warhorn", "harpoon" : "Harpoon gun",
                }
        for key in types:
            if key in keywords:
                return {"type" : types[key]}
        if "weapon" in keywords or "weap" in keywords:
            return {"supertype" : "Weapon"}
        return None

    def guess_armor_type(self, keywords):
        ret = {}
        types = {
                "aquatic helm" : "Aquatic helm", "helm" : "Helm", "shoulders" : "Shoulders", "coat" : "Coat", "gloves" : "Gloves", "leggings" : "Leggings", "boots" : "Boots",
                "breather" : "Aquatic helm", "head" : "Helm", "hat" : "Helm", "shoulder" : "Shoulders", "chest" : "Coat", "glove" : "Gloves", "hand" : "Gloves", "boot" : "Boots", "legs" : "Leggings",
                }
        classes = {"light" : "Light", "medium" : "Medium", "heavy" : "Heavy"}
        for key in classes:
            if key in keywords:
                ret['class'] = classes[key]
                break
        for key in types:
            if key in keywords:
                ret['type'] = types[key]
                break
        if len(ret) > 0:
            if "type" not in ret:
                ret["supertype"] = "Armor"
            return ret
        if "armor" in keywords:
            return {"supertype" : "Armor"}
        return None

    def guess_trinket_type(self, keywords):
        types = {
                "accessory" : "Accessory", "amulet" : "Amulet", "ring" : "Ring", "back item" : "Back item",
                "backpack" : "Back item", "back" : "Back item"
                }
        for key in types:
            if key in keywords:
                return {"type" : types[key]}
        if "trinket" in keywords:
            return {"supertype" : "Trinket"}
        return None
    
    def guess_prefix(self, keywords):
        prefixes = {
                "berserker and valkyrie" : "berserker and valkyrie","dire and rabid" : "dire and rabid","rabid and apothecary" : "rabid and apothecary",
                "apothecary" : "apothecary","apostate" : "apostate","assassin" : "assassin","berserker" : "berserker","bringer" : "bringer","captain" : "captain","carrion" : "carrion","cavalier" : "cavalier","celestial" : "celestial","cleric" : "cleric","commander" : "commander","crusader" : "crusader","dire" : "dire","diviner" : "diviner","dragon" : "dragon","forsaken" : "forsaken","giver" : "giver","grieving" : "grieving","harrier" : "harrier","knight" : "knight","magi" : "magi","marauder" : "marauder","marshal" : "marshal","minstrel" : "minstrel","nomad" : "nomad","plaguedoctor" : "plaguedoctor","rabid" : "rabid","ritualist" : "ritualist","rampager" : "rampager","sentinel" : "sentinel","seraph" : "seraph","settler" : "settler","shaman" : "shaman","sinister" : "sinister","soldier" : "soldier","trailblazer" : "trailblazer","valkyrie" : "valkyrie","vigilant" : "vigilant","viper" : "viper","wanderer" : "wanderer","zealot" : "zealot",
                "healing" : "healing","malign" : "malign","mighty" : "mighty","precise" : "precise","resilient" : "resilient","vital" : "vital","deserter" : "deserter","hearty" : "hearty","honed" : "honed","hunter" : "hunter","lingering" : "lingering","penetrating" : "penetrating","potent" : "potent","ravaging" : "ravaging","rejuvenating" : "rejuvenating","stout" : "stout","strong" : "strong","survivor" : "survivor","vagabond" : "vagabond","vigorous" : "vigorous",
                "selectable" : "selectable",

                "zerker" : "berserker", "valk" : "valkyrie"
                }
        for key in prefixes:
            if key in keywords:
                return prefixes[key]
        return None

