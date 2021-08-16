import discord
from discord.utils import get
import os

class GW2Embed:

    def __init__(self, bot):
        self.bot = bot

    async def invalid(self, message):
        bot_owner = (await self.bot.application_info()).owner
        await bot_owner.send(message)
        em = discord.Embed(title="Invalid Data", description=message, colour=0xFF0000)
        return em


    async def item(self, api_id, extras = None, emojis = []):
        gw2api = self.bot.get_cog("TybaltGW2API")
        data = await gw2api.call('{}/{}'.format('items', api_id))
        if 'text' in data and data['text'] == 'no such id':
            return await self.invalid("Woops. The entry ('item', {}) is invalid. The bot tinkerer has been informed. Sorry!".format(api_id))
        prices = await gw2api.call('{}/{}'.format('commerce/prices', api_id))
        title = '{} {} '.format(data['name'], u"\u2022")
        border_color = self._get_rarity_color(data['rarity'])
        description = '';
        if data['type'] == 'Weapon':
            title += "{} {}".format(data['rarity'], data['details']['type'])
            if data['level'] > 0:
                title += ' (Level {})'.format(data['level'])
        elif data['type'] == 'Armor':
            title += "{} {}".format(data['rarity'], data['details']['type'])
            if data['level'] > 0:
                if 'details' in data and 'weight_class' in data['details']:
                    title += ' (Level {} {} Armor)'.format(data['level'], data['details']['weight_class'])
                else:
                    title += ' (Level {} Armor)'.format(data['level'])
            elif 'details' in data and 'weight_class' in data['details']:
                title += ' ({} Armor)'.format(data['details']['weight_class'])
            else:
                title += ' (Armor)'
        elif data['type'] == 'Trinket':
            title += "{} {}".format(data['rarity'], data['details']['type'])
            if data['level'] > 0:
                title += ' (Level {})'.format(data['level'])
        elif data['type'] == 'Consumable':
            title += "{} {}".format(data['rarity'], data['details']['type'])
            if data['level'] > 0:
                title += ' (Level {})'.format(data['level'])
        elif data['type'] == 'UpgradeComponent':
            title += "{} {}".format(data['rarity'], data['details']['type'])
            if data['level'] > 0:
                title += ' (Level {})'.format(data['level'])
        else:
            title += "{} {}".format(data['rarity'], data['type'])
            if data['level'] > 0:
                title += ' (Level {})'.format(data['level'])

        description = '';
        if 'AccountBound' in data['flags']:
            if 'SoulBindOnUse' in data['flags']:
                description += 'Account Bound, Soulbound on Use' + "\r\n\r\n"
            else:
                description += 'Account Bound' + "\r\n\r\n"
        elif 'AccountBindOnUse' in data['flags']:
            description += 'Accound Bound on Use' + "\r\n\r\n"
        elif 'SoulBindOnUse' in data['flags']:
            description += 'Soulbound on Use' + "\r\n\r\n"
        
        if 'description' in data:
            description += self._translate_tags(data['description'])
            if data['type'] == "UpgradeComponent" and 'infix_upgrade' in data['details'] and 'buff' in data['details']['infix_upgrade'] :
                 description += u"\r\n\u00A0\u00A0{}".format(data['details']['infix_upgrade']['buff']['description'])
            if 'details' in data and 'bonuses' in data['details']:
                for idx, bonus in enumerate(data['details']['bonuses'], start=1):
                    description += u"\r\n\u00A0\u00A0*({}):* {}".format(idx, bonus)
            description += "\r\n\r\n"
        #description += "```json\r\n"+str(data)+"```"

        print(description)
        em = discord.Embed(title=title, description=description, colour=border_color)
        em.set_thumbnail(url=data['icon'])
        em.set_footer(text="Item ID: {}".format(api_id))
        em.add_field(name='Usable in:', value=', '.join(data['game_types']), inline=False)
        em.add_field(name='Vendor Value:', value=self._get_gold_code(data['vendor_value'], emojis), inline=True)
        em.add_field(name='Salvageable:', value=('No' if 'NoSalvage' in data['flags'] else 'Yes'), inline=True)
        if 'id' in prices:
            em.add_field(name='Buy Price:', value=self._get_gold_code(prices['buys']['unit_price'], emojis), inline=True)
            em.add_field(name='Sell Price:', value=self._get_gold_code(prices['sells']['unit_price'], emojis), inline=True)
        em.add_field(name='Chat Code', value=data['chat_link'], inline=False)

        return em

    async def recipe(self, api_id, extras = None, emojis = []):
        gw2api = self.bot.get_cog("TybaltGW2API")
        data = await gw2api.call('{}/{}'.format('recipes', api_id))
        if 'text' in data and data['text'] == 'no such id':
            return await self.invalid("Woops. The entry ('item', {}) is invalid. The bot tinkerer has been informed. Sorry!".format(api_id))
        ids = [str(data['output_item_id'])]
        for item in data['ingredients']:
            ids.append(str(item['item_id']))
        subdata = await gw2api.call('items', parameters={'ids':','.join(ids)})
        if 'text' in data:
            return await self.invalid("Woops. Something went wrong with the recipe ('item', {}). The bot tinkerer has been informed. Sorry!".format(api_id))
        items = {}
        for item in subdata:
            items[item['id']] = item
        title = items[data['output_item_id']]['name']
        if (data['output_item_count'] > 1):
            title += ' x'+data['output_item_count']
        description = ''
        if 'description' in items[data['output_item_id']]:
            description = self._translate_tags(items[data['output_item_id']]['description'])
        border_color = self._get_rarity_color(items[data['output_item_id']]['rarity'])
        ingredients = [];
        for item in data['ingredients']:
            ingredients.append('{} {}'.format(item['count'], items[item['item_id']]['name']))

        em = discord.Embed(title=title, description=description, colour=border_color)
        em.set_thumbnail(url=items[data['output_item_id']]['icon'])
        em.set_footer(text="Recipe ID: {} - Item ID: {}".format(api_id, data['output_item_id']))

        em.add_field(name='Discipline', value='\r\n'.join(data['disciplines']), inline = True)
        em.add_field(name='Req. rating', value=data['min_rating'], inline = True)
        em.add_field(name='Ingredients', value='\r\n'.join(ingredients), inline = False)
        em.add_field(name='Chat Code', value=data['chat_link'], inline=False)

        return em

    async def skin(self, api_id, extras = None, emojis = []):
        gw2api = self.bot.get_cog("TybaltGW2API")
        data = await gw2api.call('{}/{}'.format('skins', api_id))
        if 'text' in data and data['text'] == 'no such id':
            return await self.invalid("Woops. The entry ('item', {}) is invalid. The bot tinkerer has been informed. Sorry!".format(api_id))
        print(data)

    async def skill(self, api_id, extras = None, emojis = []):
        gw2api = self.bot.get_cog("TybaltGW2API")
        data = await gw2api.call('{}/{}'.format('skills', api_id))
        if 'text' in data and data['text'] == 'no such id':
            return await self.invalid("Woops. The entry ('item', {}) is invalid. The bot tinkerer has been informed. Sorry!".format(api_id))
        print(data)
        em = discord.Embed(title='', description=repr(data), colour=0x00FF00)
        return em


    async def entityList(self, entities, extracount=0):
        title="Other similar entries"
        description=""

        for entity in entities:
            description += "- {} ({})\r\n".format(entity['name'], entity['id'])

        if extracount == 1:
            description += "\r\n There is 1 another entry not shown."
        if extracount > 0:
            description += "\r\n There are {} another entries not shown.".format(extracount)

        em = discord.Embed(title=title, description=description, colour=0x0)
        return em

    def _translate_tags(self, string):
        string = string.replace('\n', "\r\n").replace('<c=@flavor>', "").replace('<c=@abilitytype>', "").replace('</c>', '').replace('<br>', "\r\n")
        return string;
    
    def _get_rarity_color(self, rarity):
        colors = {
            'Junk':0xAAAAAA,
            'Basic':0x000000,
            'Fine':0x62A4DA,
            'Masterwork':0x1A9306,
            'Rare':0xfcd00b,
            'Exotic':0xffa405,
            'Ascended':0xfb3e8d,
            'Legendary':0x4C139D
        }
        if (rarity in colors):
            return colors[rarity]
        return 0xCCCCCC

    def _get_gold_code(self, value, emojis):
        if value == 0:
            return u"\u2014"
        gold = int(value/10000)
        silver = int(value/100)%100
        copper = int(value)%100

        goldc = get(emojis, name="gold")
        silverc = get(emojis, name="silver")
        copperc = get(emojis, name="copper")
        return '{}{} {}{} {}{}'.format(
                gold, goldc if goldc is not None else 'gp',
                silver, silverc if silverc is not None else 'sp',
                copper, copperc if copperc is not None else 'cp'
        )


