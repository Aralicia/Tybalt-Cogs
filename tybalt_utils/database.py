import asyncio
import discord
import os
import mysql.connector
from redbot.core import Config, commands

class TybaltDatabase(commands.Cog):
    """TybaltDatabase."""

    def __init__(self):
        self.key = 64449859223754906028
        self.config = Config.get_conf(self, identifier=self.key)
        self.config.register_global(database='',user='',password='',host='')
        self.connection = None
        self.cursor = None

    async def verify_connection(self):
        cnx = await self.get_connection()
        if cnx.is_connected() == False:
            cnx.reconnect()
            self.cursor = None

    async def get_connection(self):
        if self.connection is None:
            database = await self.config.get_raw('database');
            user = await self.config.get_raw('user');
            password = await self.config.get_raw('password');
            host = await self.config.get_raw('host');
            self.connection = mysql.connector.connect(user=user, password=password, host=host, database=database)
        return self.connection

    async def get_cursor(self):
        if self.cursor is None:
            cnx = await self.get_connection()
            self.cursor = cnx.cursor()
        return self.cursor

