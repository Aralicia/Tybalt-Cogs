from .gw2api import gw2api

class gw2map:

    def __init__(self):
        self.data = None

    async def build(self):
        if self.data is None:
            self.data = {}
            raw = await gw2api.call('v2/continents/1/floors/1')

            #for region in raw.regions
            print(raw);
            self.data = {}
            self.data.raw = raw

    async def get_poi(self, id):
        self.build()
        if self.poi_data
        if self.map_data is not None and self.poi_data is None:


    


gw2map = GW2MAP()
