import base64
import struct
from collections import namedtuple

class Type:

    def __init__(self, raw=None):
        self.raw = raw
        self.type_id = None
        self.queried = False
        if (raw is not None):
            self.type_id = struct.unpack('<B', raw[:1])[0]

    def __str__(self):
        return "(Entity {} {})".format(self.type_id, self.get_code())

    async def query_api(self, gw2api, config):
        self.queried = False
        return None

    def get_code(self):
        return "[&{}]".format(base64.standard_b64encode(self.raw).decode('ascii'))

    def get_message(self, channel):
        return namedtuple('Message', 'message embed')(self.__str__(), None)
