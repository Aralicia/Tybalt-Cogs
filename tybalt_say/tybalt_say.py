import discord
from discord import MessageType
from redbot.core import checks, commands
from datetime import datetime
from dateutil import parser
from urllib import request
import aiohttp
import json
import random
import copy
import re

class TybaltSay(commands.Cog):
    """TybaltSay."""

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True)
    @checks.has_permissions(manage_messages=True)
    async def say(self, ctx, *message):
        """
        """
        if message:
            message = await self.clean_text(message[0], ctx.message)
            files = await self.get_files(ctx.message)

            await ctx.message.delete()
            await ctx.send(message, files=files)

    @commands.command(pass_context=True, no_pm=True)
    @checks.has_permissions(manage_messages=True)
    async def reply(self, ctx, reply, *message):
        """
        """
        await ctx.message.delete()
        target = await ctx.fetch_message(reply);

        if (target):
            message = " ".join(message, )

            await ctx.send(message, reference=target)


    async def clean_text(self, start, message):
        text = message.content
        pos = text.find(start)
        print(pos);
        text = text[pos:]

        return text

    async def get_files(self, message):
        files = []
        for a in message.attachments:
            files.append(await a.to_file())
        return files
