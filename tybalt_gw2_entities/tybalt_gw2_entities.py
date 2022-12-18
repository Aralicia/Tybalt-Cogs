import discord
import re
import base64
import struct
from itertools import islice
from redbot.core import commands, checks
from redbot.core import Config

from .types.display import CoinDisplay
from .types.type import Type
from .types.type_coin import TypeCoin
from .types.type_item import TypeItem
from .types.type_text import TypeText
from .types.type_map import TypeMap
from .types.type_pvp import TypePvp
from .types.type_skill import TypeSkill
from .types.type_trait import TypeTrait
from .types.type_user import TypeUser
from .types.type_recipe import TypeRecipe
from .types.type_skin import TypeSkin
from .types.type_outfit import TypeOutfit
from .types.type_wvw import TypeWvw
from .types.type_template import TypeTemplate
from .gw2api import gw2api


class TybaltGW2Entities(commands.Cog):
    """TybaltGW2Entities."""

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1845251931)
        self.default_type = Type
        self.types = {
            1 : TypeCoin,
            2 : TypeItem,
            #3 : TypeText,
            4 : TypeMap,
            #5 : TypePvp,
            6 : TypeSkill,
            7 : TypeTrait,
            #8 : TypeUser,
            9 : TypeRecipe,
            10: TypeSkin,
            11: TypeOutfit,
            12: TypeWvw,
            13: TypeTemplate
        }
        self.config.register_global(
            map_points={}
        )


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot is False:
            link = None
            match = re.search("^\\[\\&(.*)\\]$", message.content)
            if (match is not None):
                link = self.chatlink_decode(match.group(1))
            else:
                match = re.search("`\\[\\&(.*)\\]`", message.content)
                if (match is not None):
                    link = self.chatlink_decode(match.group(1))
            if link:
                await link.query_api(gw2api, self.config);
                msg = link.get_message(message.channel)
                if msg and (msg.message or msg.embed):
                    await message.channel.send(content=msg.message, embed=msg.embed, reference=message)

    def chatlink_decode(self, code):
        raw = base64.standard_b64decode(code)
        data = struct.unpack('B', raw[:1])[0]
        if data in self.types:
            return self.types[data](raw)
        return self.default_type(raw)

    @commands.command(pass_context=True, no_pm=False, aliases=["gem"])
    async def gems(self, ctx):
        data_gtc = await gw2api.call('commerce/exchange/gems?quantity=100', memcached=False)
        data_ctg = await gw2api.call('commerce/exchange/coins?quantity=1000000', memcached=False)
        
        description = "**Buying Gems**";
        description = "{}\n100 gems costs {}".format(description, CoinDisplay.format(100*data_ctg['coins_per_gem'], ctx.channel))

        description = "{}\n\n**Selling Gems**".format(description);
        description = "{}\n100 gems sells for {}".format(description, CoinDisplay.format(data_gtc['quantity'], ctx.channel))
        description = "{}\n*that's about {} per dollar*".format(description, CoinDisplay.format(round(data_gtc['quantity']*0.8), ctx.channel))

        em = discord.Embed(title="Gem exchange", description=description, colour=0x3e69ca)
        em.set_thumbnail(url="https://wiki.guildwars2.com/images/f/fc/Chest_of_Gems.jpg")

        await ctx.channel.send(content=None, embed=em, reference=ctx.message)

    @commands.command(pass_context=True, no_pm=True)
    @checks.has_permissions(manage_messages=True)
    async def gw2_update_pointmap(self, ctx):
        data_continents_id = await gw2api.call('continents')
        data_continents = await gw2api.call('continents?ids={}'.format(','.join(str(x) for x in data_continents_id)))
        map_points = await self.config.map_points()

        for continent in data_continents:
            floor_ids = continent['floors']
            data_floors = []
            floor_ids = floor_ids[:1]
            for floor_id in floor_ids:
                endpoint = 'continents/{}/floors/{}'.format(continent['id'], floor_id)
                data_floors_info = await gw2api.call(endpoint, memcached=False)
                for region_id, region_data in data_floors_info['regions'].items():
                    for map_id, map_data in region_data['maps'].items():
                        for poi_id, poi_data in map_data['points_of_interest'].items():
                            poi_data['map'] = map_data['name']
                            poi_data['region'] = region_data['name']
                            poi_data['continent'] = continent['name']
                            map_points[poi_id] = poi_data

        await self.config.map_points.set(map_points)
        
