import struct
import discord
from .type import Type
from collections import namedtuple
from urllib.parse import quote_plus

class TypeOutfit(Type):

    def __init__(self, raw=None):
        Type.__init__(self,raw)
        if (self.type_id != 11):
            raise TypeError('Invalid TypeId {} for type Outfit ({})'.format(self.type_id, 11))
        data = struct.unpack('<I', raw[1:4]+b'\x00')
        self.outfit_id = data[0]
        self.data = None

    def __str__(self):
        if self.queried:
            if self.data is not None:
                return "(Outfit \"{}\" ({}))".format(self.data['name'], self.skill_id)
            else:
                return "(Invalid Outfit : {})".format(self.skill_id)
        else:
            return "(Unknown Outfit : {})".format(self.skill_id)

    async def query_api(self, gw2api, config):
        data = await gw2api.call('{}/{}'.format('outfits', self.outfit_id))
        if ('name' in data):
            self.data = data
        self.queried = True
        return None

    def get_message(self, channel):
        if self.queried and self.data is not None:
            title = self.data['name']
            wiki_url = "https://wiki.guildwars2.com/index.php?title=Special%3ASearch&search={}&go=Go".format(quote_plus(self.get_code()))

            em = discord.Embed(title=title, description=None, colour=0x0)
            em.set_thumbnail(url=self.data['icon'])
            em.set_author(name="Outfit", url=wiki_url)
            em.set_footer(text= "{} (ID: {})".format(self.get_code(), self.outfit_id))

            return namedtuple('Message', 'message embed')("", em)
        return namedtuple('Message', 'message embed')("Unknown outfit with ID {}".format(self.outfit_id), None)
