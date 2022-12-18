import struct
import math
import re
from discord import TextChannel
from collections import namedtuple

class CoinDisplay:
    def format(coin_value, channel=None):
        currency = ['g', 's', 'c']
        if isinstance(channel, TextChannel):
            for emoji in channel.guild.emojis:
                if emoji.name.lower() == "gold" or emoji.name.lower() == "g":
                    currency[0] = str(emoji)
                elif emoji.name.lower() == "silver" or emoji.name.lower() == "s":
                    currency[1] = str(emoji)
                elif emoji.name.lower() == "copper" or emoji.name.lower() == "c":
                    currency[2] = str(emoji)
        value = ""
        gold = math.floor(coin_value/10000)
        if (gold != 0):
            value = "{} {}{}".format(value, gold, currency[0])
        silver = math.floor((coin_value%10000)/100)
        if (silver != 0):
            value = "{} {}{}".format(value, silver, currency[1])
        copper = coin_value%100
        if (copper != 0):
            value = "{} {}{}".format(value, copper, currency[2])
        return value


class FactDisplay:

    def format(facts):
        formated = []
        if facts is not None:
            for fact in facts:
                name = fact["text"]
                value = None
                if fact["type"] == "Damage":
                    if fact["hit_count"] > 1:
                        name = "{} (x{})".format(name, fact["hit_count"])
                    value = "{} ({})".format(404*fact["dmg_multiplier"], fact["dmg_multiplier"])
                elif fact["type"] == "Radius":
                    value = fact["distance"]
                elif fact["type"] == "Buff":
                    apply_count = fact['apply_count'] if 'apply_count' in fact else 1
                    duration = fact['duration'] if 'duration' in fact else 1
                    if apply_count > 1:
                        if duration > 1:
                            name = "{} ({}s, x{})".format(fact["status"], duration, apply_count)
                        else:
                            name = "{} (x{})".format(fact["status"], fact['apply_count'])
                    elif duration > 1:
                        name = "{} ({}s)".format(fact["status"], duration)
                    else:
                        name = "{}".format(fact["status"])
                    value = fact['description']
                elif fact["type"] in ["Recharge"]:
                    pass
                elif "value" in fact:
                    value = fact["value"]
                else:
                    with open("/home/discord/tybalt/debug.log", "a") as f:
                        print("Unhandled Skill Fact : {}".format(fact), file=f)
                        f.close()
                if name is not None and value is not None:
                    formated.append(namedtuple('Attribute', 'name value')(name, value))
        return formated

class ProfessionDisplay:

    default = { "name" : "Common", "color" : 0xDDDDDD, "icon" : "https://wiki.guildwars2.com/images/8/86/Any_tango_icon_20px.png" }
    professions = {
            "elementalist" : { "name" : "Elementalist", "color" : 0xF68A87, "icon" : "https://wiki.guildwars2.com/images/a/a2/Elementalist_icon.png" },
            "engineer" : { "name" : "Engineer", "color" : 0xD09C59, "icon" : "https://wiki.guildwars2.com/images/4/41/Engineer_icon.png" },
            "guardian" : { "name" : "Guardian", "color" : 0x72C1D9, "icon" : "https://wiki.guildwars2.com/images/c/cc/Guardian_icon.png" },
            "mesmer" : { "name" : "Mesmer", "color" : 0xB679D5, "icon" : "https://wiki.guildwars2.com/images/3/3a/Mesmer_icon.png" },
            "necromancer" : { "name" : "Necromancer", "color" : 0x52A76F, "icon" : "https://wiki.guildwars2.com/images/6/62/Necromancer_icon.png" },
            "ranger" : { "name" : "Ranger", "color" : 0x8CDC82, "icon" : "https://wiki.guildwars2.com/images/9/9c/Ranger_icon.png" },
            "revenant" : { "name" : "Revenant", "color" : 0xD16E5A, "icon" : "https://wiki.guildwars2.com/images/8/89/Revenant_icon.png" },
            "thief" : { "name" : "Thief", "color" : 0xC08F95, "icon" : "https://wiki.guildwars2.com/images/d/d8/Thief_icon.png" },
            "warrior" : { "name" : "Warrior", "color" : 0xFFD166, "icon" : "https://wiki.guildwars2.com/images/c/c8/Warrior_icon.png" },
    }
    
    @classmethod
    def data(cls, profession):
        if profession is not None:
            pl = profession.lower()
            if pl in cls.professions:
                return cls.professions[pl]
            return {
                "name": profession,
                "color": cls.default['color'],
                "icon": cls.default['icon']
            }
        return cls.default

    @classmethod
    def name(cls, profession):
        return cls.data(profession)['name']

    @classmethod
    def color(cls, profession):
        return cls.data(profession)['color']

    @classmethod
    def icon(cls, profession):
        return cls.data(profession)['icon']

class RarityDisplay:

    colors = {
            "junk"       : 0xAAAAAA,
            "basic"      : 0x000000,
            "fine"       : 0x62A4DA,
            "masterwork" : 0x1a9306,
            "rare"       : 0xfcd00b,
            "exotic"     : 0xffa405,
            "ascended"   : 0xfb3e8d,
            "legendary"  : 0x4C139D
    }

    @classmethod
    def color(cls, rarity):
        if rarity is not None:
            r = rarity.lower();
            if r in cls.colors:
                return cls.colors[r]
        return 0x0

class ItemDisplay:

    @classmethod
    def title(cls, data):
        return data['name']

    @classmethod
    def full_title(cls, data, infix, skin, upgrades):
        title = ItemDisplay.title(data)
        showsuffixes = 'HideSuffix' not in data['flags']
        if skin is not None:
            title = ItemDisplay.title(skin)

        if showsuffixes:
            if infix is not None:
                print(infix)
                title = "{} {}".format(infix['name'].capitalize(), title);
            for upgrade in upgrades:
                if 'suffix' in upgrade['details']:
                    title = "{} {}".format(title, upgrade['details']['suffix'])
                    break
        return title

    @classmethod
    def description(cls, data, skin, upgrades, channel=None):
        description = [];
        if data['type'] == 'Weapon':
            description.append("Weapon Strength: {} - {}".format(data['details']['min_power'], data['details']['max_power']))
        if data['type'] == 'Armor':
            description.append("Defense: {}".format(data['details']['defense']))

        if 'details' in data and 'infix_upgrade' in data['details']:
            for attribute in data['details']['infix_upgrade']['attributes']:
                description.append("+{} {}".format(attribute['modifier'], attribute['attribute']))
            if 'buff' in data['details']['infix_upgrade']:
                description.append("{}".format(ItemDisplay.clean_description(data['details']['infix_upgrade']['buff']['description'])))
            description.append("");

        if 'details' in data and 'bonuses' in data['details']:
            for num, bonus in enumerate(data['details']['bonuses'], start=1):
                description.append("({}): {}".format(num, ItemDisplay.clean_description(bonus)))
            description.append("");

        for upgrade in upgrades:
            description.append("**{}**".format(ItemDisplay.title(upgrade)))
            if 'infix_upgrade' in upgrade['details'] and 'buff' in upgrade['details']['infix_upgrade']:
                description.append("{}".format(ItemDisplay.clean_description(upgrade['details']['infix_upgrade']['buff']['description'])))
            if 'bonuses' in upgrade['details']:
                for num, bonus in enumerate(upgrade['details']['bonuses'], start=1):
                    description.append("({}): {}".format(num, ItemDisplay.clean_description(bonus)))
            description.append("")

        if skin is not None:
            description.append("Transmuted {}".format(ItemDisplay.title(data)))

        description.append("{} {}".format(data['rarity'], ItemDisplay.type(data)))

        if data['level'] > 0:
            description.append("Required Level: {}".format(data['level']))

        description.append("")

        if 'description' in data and data['description']:
            description.append(ItemDisplay.clean_description(data['description']))
            description.append("")

        if 'AccountBound' in data['flags']:
            description.append("Account Bound on Acquire")
        if 'AccountBindOnUse' in data['flags']:
            description.append("Account Bound on Use")
        if 'SoulBindOnUse' in data['flags']:
            description.append("Soulbound on Use")
        if 'NoSell' in data['flags']:
            description.append("Cannot be Sold")
        if 'NoSalvage' in data['flags']:
            description.append("Cannot be Salvaged")

        if 'vendor_value' in data and 'NoSell' not in data['flags']:
            description.append("Vendor Value : {}".format(CoinDisplay.format(data['vendor_value'], channel)))
        return "\r\n".join(description)

    @classmethod
    def clean_description(cls, description):
        description = re.sub(r'<c(=.*?)?>(.*?)\s*</c>', '*\\2* ', description)
        description = re.sub(r'<br>', '\r\n', description)
        return description

    @classmethod
    def type(cls, data):
        if data['type'] == 'Weapon':
            return data['details']['type']
        if data['type'] == 'Armor':
            return ItemDisplay.armor_type(data)
        if data['type'] == 'UpgradeComponent':
            return data['details']['type']
        
        return data['type']

    @classmethod
    def armor_type(cls, data):
        weight = data['details']['weight_class']
        type = data['details']['type']
        if (type == "Helm"):
            type = 'Head Armor'
        elif (type == "Shoulders"):
            type = 'Shoulders Armor'
        elif (type == "Coat"):
            type = 'Chest Armor'
        elif (type == "Gloves"):
            type = 'Hands Armor'
        elif (type == "Leggings"):
            type = 'Legs Armor'
        elif (type == "Boots"):
            type = 'Feet Armor'

        return "{} {}".format(weight, type)


class MapTypeDisplay:

    default = { "name" : "Unknown", "color" : 0xDDDDDD, "icon" : None }

    map_types = {
        'waypoint' : { "name" : "Waypoint", "color" : 0x330066, "icon" : "https://wiki.guildwars2.com/images/d/d2/Waypoint_%28map_icon%29.png" },
        'vista' : { "name" : "Vista", "color" : 0x330066, "icon" : "https://wiki.guildwars2.com/images/f/ff/Vista_%28map_icon%29.png" },
        'landmark' : { "name" : "Point of Interest", "color" : 0x330066, "icon" : "https://wiki.guildwars2.com/images/d/d2/Waypoint_%28map_icon%29.png" },
    }

    @classmethod
    def data(cls, poi):
        if poi is not None:
            pl = poi.lower()
            if pl in cls.map_types:
                return cls.map_types[pl]
            return {
                "name": poi.capitalize(),
                "color": cls.default['color'],
                "icon": cls.default['icon']
            }
        return cls.default

    @classmethod
    def name(cls, poi):
        return cls.data(poi)['name']

    @classmethod
    def color(cls, poi):
        return cls.data(poi)['color']

    @classmethod
    def icon(cls, poi):
        return cls.data(poi)['icon']
