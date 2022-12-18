import discord
from discord import MessageType
from redbot.core import commands
from datetime import datetime
from dateutil import parser
import urllib.parse
import aiohttp
import json
import random
import copy
import re

class TybaltAutoCommand(commands.Cog):
    """TybaltAutoCommand."""

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        author = message.author
        if author.bot == False and message.guild is not None and message.type == MessageType.default:
            lower = message.content.lower()
            # Next Update/Patch
            if re.match(r'.*(when|next) [^.,!?]*(patch|update)[^.,!?]*\?.*', lower) or re.match(r'.*(patch|update) [^.,!?]*(when|next)[^.,!?]*\?.*', lower):
                pass #do nothing : used by tybalt_when
            # Next Guild Chat/Stream
            elif re.match(r'.*(when|next) [^.,!?]*(guild chat|stream)[^.,!?]*\?', lower) or re.match(r'(guild chat|stream) [^.,!?]*(when|next)[^.,!?]*\?.*', lower):
                pass #do nothing : used by tybalt_when. TODO: Move from tybalt_when to here
                msg = copy.copy(message)
                msg.content = "!guildchat"
                await self.bot.get_cog('CustomCommands').on_message_without_command(msg)
            #elif re.match(r'.*(time|release) [^.,!?]*steam[^.,!?]*\?', lower) or re.match(r'.*steam [^.,!?]*(time|release)[^.,!?]*\?', lower):
            #    msg = copy.copy(message)
            #    msg.content = "!steamrelease"
            #    await self.bot.get_cog('CustomCommands').on_message_without_command(msg)
            #elif re.match(r'.*(add|account|connect|transfer|link) [^.,!?]*steam[^.,!?]*\?', lower) or re.match(r'.*steam [^.,!?]*(add|account|connect|transfer|link)[^.,!?]*\?', lower):
            #    msg = copy.copy(message)
            #    msg.content = "!steamlink"
            #    await self.bot.get_cog('CustomCommands').on_message_without_command(msg)
            elif re.match(r'.*most effective tactic.*', lower):
                msg = copy.copy(message)
                msg.content = "!metaetymology"
                await self.bot.get_cog('CustomCommands').on_message_without_command(msg)
