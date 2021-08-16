import discord
import feedparser
import re
import time
from time import mktime
from datetime import datetime
from discord.ext import tasks
from redbot.core import checks, commands
from redbot.core import Config

class TybaltFeeds(commands.Cog):
    """Tybalt Feed management."""

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1840521931)
        default_global = {
                "feeds" : []
        }
        self.config.register_global(**default_global)
        self.ticker.start()

    def cog_unload(self):
        self.ticker.cancel()

    @tasks.loop(minutes=1.0)
    async def ticker(self):
        await self.tick()
        return

    @commands.group()
    @commands.guild_only()
    @checks.has_permissions(manage_messages=True)
    async def feeds(self, ctx: commands.Context):
        """Tybalt feed management."""
        pass

    @feeds.group(name="add", invoke_without_command=True)
    async def feeds_add(self, ctx: commands.Context):
        """Add a new feed to the channel."""
        await ctx.invoke(self.feeds_add_rss, uri=uri)

    @feeds_add.command(name="rss", pass_context=True)
    async def feeds_add_rss(self, ctx: commands.Context, uri: str.lower):
        channel_id = str(ctx.message.channel.id)
        feed = await self.find_feed("rss", uri, True)
        if channel_id not in feed["channels"]:
            feed["channels"][channel_id] = {
                "display.mode" : None,
                "display.color": None,
                "display.icon" : None,
            }
            await self.update_feed(feed)
        await ctx.message.add_reaction('\U00002705');

    @feeds.command(name="config", pass_context=True)
    async def feeds_config(self, ctx: commands.Context, uri: str.lower, key:str.lower, value:str):
        channel_id = str(ctx.message.channel.id)
        feed = await self.find_feed("rss", uri, False) #TODO: handle non-rss feeds
        if channel_id in feed["channels"]:
            if key in ["display.mode", "display.color", "display.icon"]:
                feed["channels"][channel_id][key] = value
                await self.update_feed(feed)
                await ctx.message.add_reaction('\U00002705');
                return
        await ctx.message.add_reaction('\U0001F1FD');

    @feeds.command(name="list", pass_context=True)
    async def feeds_list(self, ctx: commands.Context):
        channel_id = str(ctx.message.channel.id)
        feeds = await self.config.feeds()
        matching_feeds = []
        message = ""
        for feed in feeds:
            if (channel_id in feed['channels']):
                message = "{}\n[{}] {}".format(message, feed['mode'], feed['uri'])
        if (len(message) == 0):
            message = "No feed in this channel"
        else:
            message = "Feeds in this channel :{}".format(message)
        await ctx.send(message)

    @feeds.command(name="info", pass_context=True)
    async def feeds_info(self, ctx: commands.Context, uri: str.lower):
        channel_id = str(ctx.message.channel.id)
        feed = await self.find_feed("rss", uri, False) #TODO: handle non-rss feeds
        if channel_id in feed["channels"]:
            message = "Mode : {}".format(feed["mode"])
            message = "{}\ndisplay.mode : {}".format(message, feed["channels"][channel_id]['display.mode'])
            message = "{}\ndisplay.color : {}".format(message, feed["channels"][channel_id]['display.color'])
            message = "{}\ndisplay.icon : {}".format(message, feed["channels"][channel_id]['display.icon'])
        else:
            message = "This feed is not tracked in this channel"
        await ctx.send(message)

    @feeds.command(name="clear", pass_context=True)
    async def feeds_clear(self, ctx: commands.Context):
        channel_id = str(ctx.message.channel.id)
        feeds = await self.config.feeds()
        for feed in feeds:
            if channel_id in feed['channels']:
                del feed['channels'][channel_id]
        await self.config.feeds.set(feeds)
        await ctx.message.add_reaction('\U00002705');

    @feeds.command(name="del", pass_context=True)
    async def feeds_del(self, ctx: commands.Context, uri: str.lower):
        channel_id = str(ctx.message.channel.id)
        feed = await self.find_feed("rss", uri, False) #TODO: handle non-rss feeds
        if channel_id in feed["channels"]:
            await self.delete_feed(uri)
            await ctx.message.add_reaction('\U00002705');
            return
        await ctx.message.add_reaction('\U0001F1FD');


    @feeds.command(name="tick", pass_context=False)
    async def feeds_tick(self, ctx: commands.Context):
        await self.tick()

    async def tick(self):
        feeds = await self.config.feeds()
        for feed in feeds:
            try:
                if feed['channels']:
                    if feed['mode'] == 'rss':
                        d = feedparser.parse(feed['uri'])
                        if feed['last_update'] is None:
                            feed['last_update'] = d.entries[0].published_parsed
                        else:
                            last_update = time.struct_time(feed['last_update'])
                            new_update = last_update
                            new_entries = list(entry for entry in d.entries if entry.published_parsed > last_update)
                            new_entries = sorted(new_entries, key=lambda entry: entry.published_parsed)
                            for entry in new_entries:
                                for channel_id, config in feed['channels'].items():
                                    if (config['display.mode'] == 'upnotes'):
                                        embed = self.get_upnotes_embed(config, d.feed, entry)
                                    elif config['display.mode'] == 'news':
                                        embed = self.get_news_embed(config, d.feed, entry)
                                    else:
                                        embed = self.get_rss_embed(config, d.feed, entry)
                                    channel = self.bot.get_channel(int(channel_id))
                                    await channel.send(content=None, embed=embed)
                                feed['last_update'] = entry.published_parsed
            except OSError:
                pass
        await self.config.feeds.set(feeds)

    async def find_feed(self, mode, uri, create=False):
        feeds = await self.config.feeds()
        for feed in (feed for feed in feeds if feed['mode'] == mode and feed['uri'] == uri):
            return feed
        if create:
            feed = {"mode":mode, "uri":uri, "channels":{}, "last_update":None}
            feeds.append(feed)
            await self.config.feeds.set(feeds)
            return feed
        return None

    async def update_feed(self, update):
        feeds = await self.config.feeds()
        for feed in (feed for feed in feeds if feed['mode'] == update['mode'] and feed['uri'] == update['uri']):
            feed["channels"] = update["channels"]
            feed["last_update"] = update["last_update"]
        await self.config.feeds.set(feeds)

    def get_rss_embed(self, config, feed, entry):
        description = entry.summary
        if len(description) > 1500:
            description = "{}...".format(description[:1500])
        description = re.sub(r'\n+', r'\n', description)
        description = re.sub(r'<h1>(.*?)</h1>', r'\n\n**\1**', description)
        description = re.sub(r'<h2>(.*?)</h2>', r'\n**\1**', description)
        description = re.sub(r'<h3>(.*?)</h3>', r'\n**\1**', description)
        description = re.sub(r'<.*?>', r'', description)
        color = int(config["display.color"], 0) if config["display.color"] != None else discord.Embed.Empty

        em = discord.Embed(title=entry.title, description=description, colour=color, url=entry.link)
        if config["display.icon"]:
            em.set_thumbnail(url=config["display.icon"])
        em.set_author(name=feed.title, url=feed.link)
        em.set_footer(text=entry.author)
        em.timestamp = datetime.fromtimestamp(mktime(entry.published_parsed))
        return em

    def get_upnotes_embed(self, config, feed, entry):
        description = entry.summary
        if len(description) > 1500:
            description = "{}...".format(description[:1500])
        description = re.sub(r'\n+', r'\n', description)
        description = re.sub(r'<h1>(.*?)</h1>', '', description)
        description = re.sub(r'<h2>(.*?)</h2>', (lambda m: "\n**{}**".format(m.group(1).upper())), description)
        description = re.sub(r'<h3>(.*?)</h3>', (lambda m: "\n**{}**".format(m.group(1).capitalize())), description)
        description = re.sub(r'\n', r'\n\n', description)
        description = re.sub(r'<.*?>', r'', description)
        color = int(config["display.color"], 0) if config["display.color"] != None else discord.Embed.Empty

        em = discord.Embed(title=entry.title, description=description, colour=color, url=entry.link)
        if config["display.icon"]:
            em.set_thumbnail(url=config["display.icon"])
        em.set_author(name=feed.title, url=feed.link)
        em.set_footer(text=entry.author)
        em.timestamp = datetime.fromtimestamp(mktime(entry.published_parsed))
        return em

    def get_news_embed(self, config, feed, entry):
        description = entry.summary
        if ('content' in entry and entry.content[0]):
            description =  entry.content[0].value
        if len(description) > 1500:
            description = "{}...".format(description[:1500])
        description = re.sub(r'\n+', r'\n', description)
        description = re.sub(r'<h1>(.*?)</h1>', '', description)
        description = re.sub(r'<h2>(.*?)</h2>', (lambda m: "\n**{}**".format(m.group(1).upper())), description)
        description = re.sub(r'<h3>(.*?)</h3>', (lambda m: "\n**{}**".format(m.group(1).capitalize())), description)
        description = re.sub(r'\n', r'\n\n', description)
        description = re.sub(r'<.*?>', r'', description)
        color = int(config["display.color"], 0) if config["display.color"] != None else discord.Embed.Empty

        em = discord.Embed(title=entry.title, description=description, colour=color, url=entry.link)
        if config["display.icon"]:
            em.set_thumbnail(url=config["display.icon"])
        em.set_author(name=feed.title, url=feed.link)
        em.set_footer(text=entry.author)
        em.timestamp = datetime.fromtimestamp(mktime(entry.published_parsed))
        return em

