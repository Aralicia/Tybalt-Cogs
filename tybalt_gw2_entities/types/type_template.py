import struct
from .type import Type

class TypeTemplateSpec:
    def __init__(self, id, traits):
        self.id = id
        self.traits = traits

class TypeTemplate(Type):
    def __init__(self, raw=None):
        Type.__init__(self,raw)
        if (self.type_id != 13):
            raise TypeError('Invalid TypeId {} for type Build Template ({})'.format(self.type_id, 13))
        data = struct.unpack('<BBBBBBB', raw[1:8])
        self.class_id = data[0]
        self.spec1 = TypeTemplateSpec(data[1], data[2])
        self.spec2 = TypeTemplateSpec(data[3], data[4])
        self.spec3 = TypeTemplateSpec(data[5], data[6])
        print(self)

    def __str__(self):
        if self.queried:
            return ""
        return "" #"(Build Template)"

    async def query_api(self, gw2api, config):
        self.queried = True
        return None

    
