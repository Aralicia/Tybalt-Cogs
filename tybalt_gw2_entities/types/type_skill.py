import struct
import discord
from .type import Type
from collections import namedtuple
from urllib.parse import quote_plus
from .display import FactDisplay, ProfessionDisplay

class TypeSkill(Type):

    def __init__(self, raw=None):
        Type.__init__(self,raw)
        if (self.type_id != 6):
            raise TypeError('Invalid TypeId {} for type Skill ({})'.format(self.type_id, 6))
        data = struct.unpack('<I', raw[1:4]+b'\x00')
        self.skill_id = data[0]
        self.data = None

    def __str__(self):
        if self.queried:
            if self.data is not None:
                return "(Skill \"{}\" ({}))".format(self.data['name'], self.skill_id)
            else:
                return "(Invalid Skill : {})".format(self.skill_id)
        else:
            return "(Unknown Skill : {})".format(self.skill_id)

    async def query_api(self, gw2api, config):
        data = await gw2api.call('{}/{}'.format('skills', self.skill_id))
        if ('name' in data):
            self.data = data;
        self.queried = True
        return None

    def get_message(self, channel):
        if self.queried and self.data is not None:
            profession = self.get_profession_info()
            title = self.data['name']
            facts = []
            if 'facts' in self.data:
                facts = FactDisplay.format(self.data['facts'])
            description = self.data['description']
            #description = self.data.__str__()
            border_color = profession['color']
            wiki_url = "https://wiki.guildwars2.com/index.php?title=Special%3ASearch&search={}&go=Go".format(quote_plus(self.get_code()))

            em = discord.Embed(title=title, description=description, colour=border_color)
            em.set_thumbnail(url=self.data['icon'])
            em.set_author(name=self.get_skill_type(), icon_url=profession['icon'], url=wiki_url)
            em.set_footer(text= "{} (ID: {})".format(self.get_code(), self.skill_id))
            for fact in facts:
                em.add_field(name=fact.name, value=fact.value, inline=False)

            return namedtuple('Message', 'message embed')("", em)
        return namedtuple('Message', 'message embed')("Unknown skill with ID {}".format(self.skill_id), None)
    
    def get_profession_info(self):
        if "professions" not in self.data:
            return ProfessionDisplay.default
        professions = self.data['professions']
        if len(professions) != 1:
            return ProfessionDisplay.default
        return ProfessionDisplay.data(professions[0])

    def get_skill_type(self):
        if self.data is None:
            return "Common Skill"
        profession = self.get_profession_info()
        skill_type = "";
        if "type" in self.data:
            if self.data["type"] == "Weapon":
                weapon_type = self.data["weapon_type"]
                if weapon_type == "None":
                    weapon_type = "Downed"
                if profession['name'] == "Elementalist":
                    skill_type = "{} ({})".format(weapon_type, self.data["attunement"])
                elif profession['name'] == "Thief":
                    skill_type = weapon_type
                else:
                    skill_type = weapon_type
            else:
                skill_type = self.data["type"]
        return "{} {} Skill".format(profession['name'], skill_type)

