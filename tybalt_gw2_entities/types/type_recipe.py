import struct
import re
import discord
from .type import Type
from .display import RarityDisplay
from collections import namedtuple
from urllib.parse import quote_plus

class TypeRecipe(Type):

    def __init__(self, raw=None):
        Type.__init__(self,raw)
        if (self.type_id != 9):
            raise TypeError('Invalid TypeId {} for type Recipe ({})'.format(self.type_id, 9))
        data = struct.unpack('<I', raw[1:4]+b'\x00')
        self.recipe_id = data[0]
        self.data = None
        self.item_data = None

    def __str__(self):
        return "(Recipe)"

    async def query_api(self, gw2api, config):
        data = await gw2api.call('{}/{}'.format('recipes', self.recipe_id))
        print(data)
        if ('id' in data):
            self.data = data;
            ids = []
            ids.append(str(self.data['output_item_id']))
            for item in self.data['ingredients']:
                ids.append(str(item['item_id']))
            self.item_data = {}
            data =  await gw2api.call('items?ids={}'.format(",".join(ids)))
            for item in data:
                self.item_data[item['id']] = item
            print(data)
        self.queried = True
        return None

    def get_message(self, channel):
        if self.queried and self.data is not None:
            output = self.item_data[self.data['output_item_id']] if self.data['output_item_id'] in self.item_data else None
            output_name = output["name"] if output is not None else "Unknown"
            if self.data['output_item_count'] > 1:
                title = "Recipe: {} {}".format(self.data['output_item_count'], output_name)
            else:
                title = "Recipe: {}".format(output_name)
            description = "**Type:** {}".format(re.sub(r"(\w)([A-Z])", r"\1 \2", self.data["type"]))
            description = "{}\n**Disciplines:** {}".format(description, ", ".join(sorted(self.data["disciplines"])))
            description = "{}\n**Required Rating:** {}".format(description, self.data['min_rating'])
            description = "{}\n\n**Ingredients**".format(description)
            for ingredient in self.data["ingredients"]:
                if (ingredient['item_id'] in self.item_data):
                    item_name = self.item_data[ingredient['item_id']]["name"]
                else:
                    item_name = "Unknown Item ({})".format(ingredient['item_id'])
                description = "{}\n{} {}".format(description, ingredient['count'], item_name)

            border_color = RarityDisplay.color(output["rarity"]) if output is not None else 0x0

            em = discord.Embed(title=title, description=description, colour=border_color)
            em.set_footer(text= "{} (ID: {})".format(self.get_code(), self.recipe_id))
            if output is not None:
                em.set_thumbnail(url=output['icon'])

            return namedtuple('Message', 'message embed')("", em)
        return namedtuple('Message', 'message embed')("Unknown recipe with ID {}".format(self.recipe_id), None)
