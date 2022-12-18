import struct
import discord
from collections import namedtuple
from .type import Type
from .display import MapTypeDisplay

class TypeMap(Type):

    def __init__(self, raw=None):
        Type.__init__(self,raw)
        if (self.type_id != 4):
            raise TypeError('Invalid TypeId {} for type Map ({})'.format(self.type_id, 4))
        data = struct.unpack('<I', raw[1:4]+b'\x00')
        self.map_id = data[0]
        self.data = None

    def __str__(self):
        if self.queried:
            if self.data is not None:
                return "({} \"{}\" ({}, {}, {}))".format(self.data['type'], self.data['name'], self.data['map'], self.data['region'], self.data['continent'])
            return "(Invalid Map Link : {})".format(self.map_id)
        return "(Unknown Map Link : {})".format(self.map_id)

    async def query_api(self, gw2api, config):
        map_points = await config.map_points()
        map_id = str(self.map_id)
        if map_id in map_points:
            self.data = map_points[map_id]
        self.queried = True
        return None

    def get_message(self, channel):
        if self.queried and self.data is not None:
            title = self.data['name']
            description = ""
            border_color = MapTypeDisplay.color(self.data['type'])

            description = "{}**Type :** {}".format(description, MapTypeDisplay.name(self.data['type']))
            description = "{}\n**Map :** {}".format(description, self.data['map'])
            description = "{}\n**Region :** {}".format(description, self.data['region'])
            description = "{}\n**World :** {}".format(description, self.data['continent'])

            em = discord.Embed(title=title, description=description, colour=border_color)
            em.set_thumbnail(url=MapTypeDisplay.icon(self.data['type']))
            em.set_footer(text= "{} (ID: {})".format(self.get_code(), self.map_id))
            return namedtuple('Message', 'message embed')("", em)
        return namedtuple('Message', 'message embed')("Unknown map link with ID {}".format(self.map_id), None)
