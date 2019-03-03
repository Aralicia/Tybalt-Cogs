import discord
from redbot.core import commands

class TabMessage:
    def __init__(self):
        self.tabs = []
        self.client = None
        self.channel = None
        self.message = None

    def addTab(self, page, emoji):
        self.tabs.append({'page':page, 'emoji':emoji})

    def setClient(self, client):
        self.client = client

    def setChannel(self, channel):
        self.channel = channel

    async def send(self):
        if len(self.tabs) > 0 and self.client is not None and self.channel is not None:
            firstpage = self.tabs[0]['page']
            if isinstance(firstpage, discord.Embed):
                self.message = await self.channel.send(embed=firstpage)
            else:
                self.message = await self.channel.send(firstpage)
            for tab in self.tabs:
                await self.message.add_reaction(tab['emoji'])
            return self.message.id
        return None
    
    async def handleReaction(self, reaction, user):
        if (user.bot == False):
            for tab in self.tabs:
                if reaction.emoji == tab['emoji']:
                    if isinstance(tab['page'], discord.Embed):
                        await reaction.message.edit(embed=tab['page'])
                    else:
                        await reaction.message.edit(new_content=tab['page'])
        if (reaction.me == False):
            await reaction.remove()


class TabMessages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.messages = {}
        self.TabMessage = TabMessage

    async def send(self, message, channel):
        message.setClient(self.bot)
        message.setChannel(channel)
        result = await message.send()
        if result is not None:
            self.messages[result] = message

    async def on_reaction_add(self, reaction, user):
        if reaction.message.id in self.messages:
            await self.messages[reaction.message.id].handleReaction(reaction, user)

