import struct
import discord
from .type import Type
from collections import namedtuple
from urllib.parse import quote_plus
from .display import RarityDisplay

class TypeSkin(Type):

    def __init__(self, raw=None):
        Type.__init__(self,raw)
        if (self.type_id != 10):
            raise TypeError('Invalid TypeId {} for type Skin ({})'.format(self.type_id, 10))
        data = struct.unpack('<I', raw[1:4]+b'\x00')
        self.skin_id = data[0]
        self.data = None

    def __str__(self):
        if self.queried:
            if self.data is not None:
                return "(Skin \"{}\" ({}))".format(self.data['name'], self.skin_id)
            else:
                return "(Invalid Skin : {})".format(self.skin_id)
        else:
            return "(Unknown Skin : {})".format(self.skin_id)

    async def query_api(self, gw2api, config):
        data = await gw2api.call('{}/{}'.format('skins', self.skin_id))
        if ('name' in data):
            self.data = data;
        self.queried = True
        return None

    def get_message(self, channel):
        if self.queried and self.data is not None:
            title = self.data['name']
            description = None
            border_color = RarityDisplay.color(self.data['rarity'])
            wiki_url = "https://wiki.guildwars2.com/index.php?title=Special%3ASearch&search={}&go=Go".format(quote_plus(self.get_code()))

            if 'restrictions' in self.data and len(self.data['restrictions']) > 0:
                description = "*{} Only.*".format(", ".join(self.data['restrictions']))

            em = discord.Embed(title=title, description=description, colour=border_color)
            em.set_thumbnail(url=self.data['icon'])
            em.set_author(name=self.get_skin_type(), url=wiki_url)
            em.set_footer(text= "{} (ID: {})".format(self.get_code(), self.skin_id))

            if ('details' in self.data):
                if 'damage_type' in self.data['details']:
                    em.add_field(name="Damage Type", value=self.data['details']['damage_type'])
                if 'dye_slots' in self.data['details']:
                    em.add_field(name="Dye Slots", value=len([slot for slot in self.data['details']['dye_slots']['default'] if slot]))

            return namedtuple('Message', 'message embed')("", em)
        return namedtuple('Message', 'message embed')("Unknown skin with ID {}".format(self.skill_id), None)

    def get_skin_type(self):
        if self.data is None:
            return "Skin"
        if (self.data['type'] == 'Armor'):
            return "{} {} skin".format(self.data['details']['weight_class'], self.data['details']['type'])
        elif (self.data['type'] == 'Weapon'):
            return "{} skin".format(self.data['details']['type'])
        elif (self.data['type'] == 'Back'):
            return "Back skin"
        return "Skin";
