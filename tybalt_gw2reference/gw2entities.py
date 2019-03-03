from enum import Enum
import aiohttp
import json

class EntityType(Enum):
    def item():
        return {'sql':'item', 'api':'items'}
    def recipe():
        return {'sql':'recipe', 'api':'recipes'}

class GW2Entities:

    def __init__(self, bot):
        self.bot = bot
        self.database = None

    async def verifyDatabase(self):
        if (self.database == None):
            self.database = self.bot.get_cog("TybaltDatabase")
        await self.database.verify_connection()

    async def findById(self, id, type):
        await self.verifyDatabase()
        cursor = await self.database.get_cursor()
        query = ("SELECT api_id, name FROM entity WHERE type = %s AND api_id = %s and removed = 0")
        cursor.execute(query, (type['sql'], id))
        for (api_id, name) in cursor:
            return ([{'id': api_id, 'name': name}], 1)
        return ([], 0)

    async def findByName(self, name, type, limit):
        await self.verifyDatabase()
        results = []
        cursor = await self.database.get_cursor()
        query = ("SELECT SQL_CALC_FOUND_ROWS api_id, name, distance FROM (SELECT api_id, name, damlevlim(%s, name, 254) as `distance` FROM entity WHERE type = %s and removed = 0) t WHERE (distance < 3 OR name LIKE %s) ORDER BY IF(name LIKE %s,1,0) DESC, distance ASC LIMIT %s")
        pattern = '%'+name+'%'
        cursor.execute(query, (name, type['sql'], pattern, pattern, limit))
        for (api_id, name, distance) in cursor:
            results.append({'id': api_id, 'name': name, 'distance': distance})
        cursor.execute("SELECT FOUND_ROWS()");
        (total,) = cursor.fetchone();
        return (results, total)

