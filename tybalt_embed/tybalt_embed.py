import discord
from redbot.core import commands
from redbot.core import checks
import urllib.parse
import aiohttp
import json
from datetime import datetime
import dateutil.parser

class TybaltEmbed(commands.Cog):
    """TybaltEmbed."""

    @commands.command(pass_context=True, no_pm=True)
    @checks.admin_or_permissions(manage_roles=True)
    async def embed(self, ctx, *search):
        """Create an embed from a json url
        Json build can be found at https://leovoel.github.io/embed-visualizer/

        Example:
        !embed https://pastebin.com/raw/1PacLKkf
       """
        try:
            await ctx.trigger_typing()

            url = " ".join(search)

            async with aiohttp.ClientSession() as session:
                async with session.get(url) as r:
                    data = await r.text()
                    status = r.status

            try:
                parsed = json.loads(data)
            except:
                parsed = None

            if parsed is not None:
                content = None

                if 'content' in parsed:
                    content = parsed['content']

                if 'embed' in parsed:
                    embedData = parsed['embed']
                    title = None
                    description = None
                    url = None
                    color = 0x000000
                    timestamp = discord.Embed.Empty

                    if 'title' in embedData:
                        title = embedData['title']
                    if 'description' in embedData:
                        description = embedData['description']
                    if 'url' in embedData:
                        url = embedData['url']
                    if 'color' in embedData:
                        color = embedData['color']
                    if 'timestamp' in embedData:
                        timestamp = dateutil.parser.parse(embedData['timestamp'])

                    embed = discord.Embed(title=title, description=description, url=url, colour=color, timestamp=timestamp)
                    if 'image' in embedData and 'url' in embedData['image']:
                        embed.set_image(url=embedData['image']['url'])
                    if 'thumbnail' in embedData and 'url' in embedData['thumbnail']:
                        embed.set_thumbnail(url=embedData['thumbnail']['url'])

                    if 'author' in embedData:
                        author_name = None
                        author_url = None
                        author_icon = None
                        if 'name' in embedData['author']:
                            author_name = embedData['author']['name']
                        if 'url' in embedData['author']:
                            author_url = embedData['author']['url']
                        if 'icon_url' in embedData['author']:
                            author_icon = embedData['author']['icon_url']
                        embed.set_author(name=author_name, url=author_url, icon_url=author_icon)

                    if 'footer' in embedData:
                        footer_text = None
                        footer_icon = None
                        if 'text' in embedData['footer']:
                            footer_text = embedData['footer']['text']
                        if 'icon_url' in embedData['footer']:
                            footer_icon = embedData['footer']['icon_url']
                        embed.set_footer(text=footer_text, icon_url=footer_icon)

                    if 'fields' in embedData:
                        for field in embedData['fields']:
                            name = None
                            value = None
                            if 'name' in field:
                                name = field['name']
                            if 'value' in field:
                                value = field['value']
                            if 'inline' in field:
                                embed.add_field(name=name, value=value, inline=field['inline'])
                            else:
                                embed.add_field(name=name, value=value)
                    await ctx.send(content, embed=embed)
                else:
                    await ctx.send(content)

        except Exception as e:
            print(e)
            await ctx.send("Something went wrong.")

