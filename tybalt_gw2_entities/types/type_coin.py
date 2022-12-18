import math
import struct
from .type import Type
from collections import namedtuple
from discord import TextChannel

class TypeCoin(Type):

    def __init__(self, raw=None):
        Type.__init__(self,raw)
        if (self.type_id != 1):
            raise TypeError('Invalid TypeId {} for type Coin ({})'.format(self.type_id, 1))
        self.coin_value = struct.unpack('<I', raw[1:5])[0]

    def __str__(self):
        return "(Coin {})".format(self.get_code())

    async def query_api(self, gw2api, config):
        self.queried = True
        return None

    def get_code(self):
        self.raw = struct.pack('<BI', self.type_id, self.coin_value)
        return Type.get_code(self)

    def get_message(self, channel):
        if self.coin_value <= 0:
            return None
        currency = ['g', 's', 'c']
        if isinstance(channel, TextChannel):
            for emoji in channel.guild.emojis:
                if emoji.name.lower() == "gold":
                    currency[0] = str(emoji)
                elif emoji.name.lower() == "silver":
                    currency[1] = str(emoji)
                elif emoji.name.lower() == "copper":
                    currency[2] = str(emoji)
        value = ""
        gold = math.floor(self.coin_value/10000)
        if (gold != 0):
            value = "{} {}{}".format(value, gold, currency[0])
        silver = math.floor((self.coin_value%10000)/100)
        if (silver != 0):
            value = "{} {}{}".format(value, silver, currency[1])
        copper = self.coin_value%100
        if (copper != 0):
            value = "{} {}{}".format(value, copper, currency[2])
        return namedtuple('Message', 'message embed')('> {}'.format(value.strip()), None)

