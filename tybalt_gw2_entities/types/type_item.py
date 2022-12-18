import struct
import discord
from .type import Type
from collections import namedtuple
from urllib.parse import quote_plus
from .display import RarityDisplay, ItemDisplay

class TypeItem(Type):

    def __init__(self, raw=None):
        Type.__init__(self,raw)
        if (self.type_id != 2):
            raise TypeError('Invalid TypeId {} for type Item ({})'.format(self.type_id, 2))
        self.item_count = int.from_bytes(raw[1:2], 'little')
        self.item_id = int.from_bytes(raw[2:5], 'little')
        self.extra_code = int.from_bytes(raw[5:6], 'little')
        self.skin_id = None
        self.skin_data = None
        self.upgrade_ids = []
        self.upgrades = []
        self.infix = None

        offset = 6
        if (self.extra_code & 0x80) != 0:
            self.skin_id = int.from_bytes(raw[offset:offset+4], 'little')
            offset += 4
        if (self.extra_code & 0x40) != 0:
            self.upgrade_ids.append(int.from_bytes(raw[offset:offset+4], 'little'))
            offset += 4
        if (self.extra_code & 0x20) != 0:
            self.upgrade_ids.append(int.from_bytes(raw[offset:offset+4], 'little'))

        offset = 0
        self.data = None

    def __str__(self):
        if self.queried:
            if self.data is not None:
                return "(Item {}x {}({}) : {})".format(self.item_count, self.data['name'], self.item_id, self.get_code())
            else:
                return "(Invalid Item {}x {} : {})".format(self.item_count, self.item_id, self.get_code())
        else:
            return "(Unknown Item {}x {} : {})".format(self.item_count, self.item_id, self.get_code())

    async def query_api(self, gw2api, config):
        data = await gw2api.call('{}/{}'.format('items', self.item_id))
        if ('name' in data):
            self.data = data;
            if 'details' in data and 'infix_upgrade' in self.data['details']:
                data = await gw2api.call('{}/{}'.format('itemstats', self.data['details']['infix_upgrade']['id']))
                if ('name' in data):
                    self.infix = data
        if self.skin_id is not None:
            data = await gw2api.call('{}/{}'.format('skins', self.skin_id))
            if ('name' in data):
                self.skin_data = data
        for upgrade_id in self.upgrade_ids:
            data = await gw2api.call('{}/{}'.format('items', upgrade_id))
            if ('name' in data):
                self.upgrades.append(data)
        self.queried = True
        return None

    def get_message(self, channel):
        if self.queried:
            if self.data is not None:
                title = ItemDisplay.full_title(self.data, self.infix, self.skin_data, self.upgrades)
                description = ItemDisplay.description(self.data, self.skin_data, self.upgrades, channel)
                border_color = RarityDisplay.color(self.data['rarity'])

                wiki_url = "https://wiki.guildwars2.com/index.php?title=Special%3ASearch&search={}&go=Go".format(quote_plus(self.get_code()))

                em = discord.Embed(title=title, description=description, colour=border_color, url=wiki_url)
                if (self.skin_data is not None):
                    em.set_thumbnail(url=self.skin_data['icon'])
                else:
                    em.set_thumbnail(url=self.data['icon'])
                em.set_footer(text=self.get_code())
                return namedtuple('Message', 'message embed')("", em)
            return namedtuple('Message', 'message embed')("Invalid item with ID {}".format(self.item_id), None)
        return namedtuple('Message', 'message embed')("Unknown item with ID {}".format(self.item_id), None)
