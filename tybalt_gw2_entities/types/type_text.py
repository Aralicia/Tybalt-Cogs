import struct
from .type import Type

class TypeText(Type):

    def __init__(self, raw=None):
        Type.__init__(self,raw)
        if (self.type_id != 3):
            raise TypeError('Invalid TypeId {} for type Text ({})'.format(self.type_id, 3))
        #data = struct.unpack('<BI', raw[1:6])
        #self.item_count = data[0] 
        #self.item_id = data[1]

    def __str__(self):
        return "(Text)"

    async def query_api(self, gw2api, config):
        self.queried = True
        return None
