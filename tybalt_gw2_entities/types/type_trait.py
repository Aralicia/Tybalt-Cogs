import struct
import discord
from .type import Type
from collections import namedtuple
from .display import FactDisplay, ProfessionDisplay
from urllib.parse import quote_plus


class TypeTrait(Type):

    def __init__(self, raw=None):
        Type.__init__(self,raw)
        if (self.type_id != 7):
            raise TypeError('Invalid TypeId {} for type Trait ({})'.format(self.type_id, 7))
        data = struct.unpack('<I', raw[1:4]+b'\x00')
        self.trait_id = data[0]
        self.data = None
        self.spec_data = None

    def __str__(self):
        if self.queried:
            if self.data is not None:
                return "(Trait \"{}\" ({}))".format(self.data['name'], self.trait_id)
            else:
                return "(Invalid Trait : {})".format(self.trait_id)
        return "(Unknown Trait : {})".format(self.trait_id)

    async def query_api(self, gw2api, config):
        data = await gw2api.call('{}/{}'.format('traits', self.trait_id))
        if ('name' in data):
            self.data = data;
        if ('specialization' in data and data['specialization'] is not None):
            data = await gw2api.call('{}/{}'.format('specializations', data['specialization']))
            if ('name' in data):
                self.spec_data = data
        self.queried = True
        return None

    def get_message(self, channel):
        if self.queried and self.data is not None:
            prof = None
            if self.spec_data is not None:
                prof = self.spec_data['profession']

            profession = ProfessionDisplay.data(prof)
            title = self.data['name']
            facts = FactDisplay.format(self.data['facts'])
            description = ""
            if ('description' in self.data):
                description = self.data['description']
            border_color = profession['color']
            wiki_url = "https://wiki.guildwars2.com/index.php?title=Special%3ASearch&search={}&go=Go".format(quote_plus(self.get_code()))
            small_icon = profession['icon']

            if self.spec_data is not None:
                small_icon = self.spec_data['icon'];

            em = discord.Embed(title=title, description=description, colour=border_color)
            em.set_thumbnail(url=self.data['icon'])
            em.set_author(name=self.get_trait_type(), icon_url=small_icon, url=wiki_url)
            em.set_footer(text= "{} (ID: {})".format(self.get_code(), self.trait_id))
            for fact in facts:
                em.add_field(name=fact.name, value=fact.value, inline=False)

            return namedtuple('Message', 'message embed')("", em)
        return namedtuple('Message', 'message embed')("Unknown trait with ID {}".format(self.skill_id), None)

    def get_trait_type(self):
        if self.data is None:
            return "Common Trait";
        tier = ""
        if (self.data['tier'] == 1):
            tier = "Adept"
        if (self.data['tier'] == 2):
            tier = "Master"
        if (self.data['tier'] == 3):
            tier = "Grandmaster"
        if self.spec_data is not None:
            if self.spec_data['elite'] == True:
                return "{} {} {} Trait".format(self.spec_data['name'], self.data['slot'], tier)

            return "{} {} {} Trait ({})".format(self.spec_data['name'], self.data['slot'], tier, ProfessionDisplay.name(self.spec_data['profession']))
        return "{} {} Trait".format(self.data['slot'], tier)



