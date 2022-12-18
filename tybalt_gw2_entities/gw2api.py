from pymemcache.client import base as memcache
import aiohttp
import json

def json_serializer(key, value):
    if type(value) == str:
        return value, 1
    return json.dumps(value), 2

def json_deserializer(key, value, flags):
    if flags == 1:
        return value.decode('utf-8')
    if flags == 2:
        return json.loads(value.decode('utf-8'))
    return value

class GW2API:
    def __init__(self):
        self.memcache = memcache.Client(('127.0.0.1', 11211), serializer=json_serializer, deserializer=json_deserializer)

    async def call(self, path, version='v2', memcached=True):
        url = 'https://api.guildwars2.com/{}/{}'.format(version, path)
        data = None
        if memcached:
            data = self.memcache.get(url);
        if data is None:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as r:
                    data = await r.text()
                    status = r.status
            try:
                data = json.loads(data)
            except:
                data = json.loads({})
            if memcached:
                self.memcache.set(url, data)
        return data

gw2api = GW2API()
