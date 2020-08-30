import discord
from random import choice
from redbot.core import commands

class TybaltNewchar(commands.Cog):
    """TybaltNewchar."""

    def random_race(self, char):
        char['race'] = choice(["Asura", "Charr", "Human", "Norn", "Sylvari"])

    def random_gender(self, char):
        char['gender'] = choice(["Male", "Female"])

    def random_profession(self, char):
        char['profession'] = choice(["Elementalist", "Engineer", "Guardian", "Mesmer", "Necromancer", "Ranger", "Revenant", "Thief", "Warrior"])

    def random_bio(self, char):
        # profession question
        char['bio_profession'] = ('', '')
        if char['profession'] == "Elementalist":
            char['bio_profession'] = ("Pet", "I wear a gem of", choice(["**Water**", "**Fire**", "**Earth**", "**Air**"]))
        if char['profession'] == "Engineer":
            char['bio_profession'] = ("Pet", "My tool is", choice(["a **Universal Multitool Pack**", "**Eagle-Eye Goggles**", "a **Panscopic Monocle**"]))
        if char['profession'] == "Guardian":
            char['bio_profession'] = ("Pet", "I wear", choice(["**Conqueror's Pauldrons**", "**Fanatic's Pauldron**", "a **Visionary's Helm**"]))
        if char['profession'] == "Mesmer":
            char['bio_profession'] = ("Pet", "My mask is", choice(["**Harlequin's Smile**", "**Phantasm of Sorrow**", "**Fanged Dread**"]))
        if char['profession'] == "Necromancer":
            char['bio_profession'] = ("Pet", "I mark my face with the symbol of a", choice(["**Trickster Demon**", "**Skull**", "**Ghostly Wraith**"]))
        if char['profession'] == "Ranger":
            if char['race'] == "Asura":
                char['bio_profession'] = ("Pet", "My pet is a", choice(["**Moa**", "**Stalker**", "**Drake**"]))
            if char['race'] == "Charr":
                char['bio_profession'] = ("Pet", "My pet is a", choice(["**Devourer**", "**Stalker**", "**Drake**"]))
            if char['race'] == "Human":
                char['bio_profession'] = ("Pet", "My pet is a", choice(["**Bear**", "**Stalker**", "**Drake**"]))
            if char['race'] == "Norn":
                char['bio_profession'] = ("Pet", "My pet is a", choice(["**Bear**", "**Wolf**", "**Snow Leopard**"]))
            if char['race'] == "Sylvari":
                char['bio_profession'] = ("Pet", "My pet is a", choice(["**Moa**", "**Stalker**", "**Fern Hound**"]))
        if char['profession'] == "Revenant":
            char['bio_profession'] = ("Pet", "I fight with my", choice(["**Mist Scrim** blindfold", "**Veil Piercer** blindfold", "**Resplendent Curtain** blindfold"]))
        if char['profession'] == "Thief":
            char['bio_profession'] = ("Pet", "I understand the power of", choice(["**Anonymity**", "**Determination**", "**Subterfuge**"]))
        if char['profession'] == "Warrior":
            char['bio_profession'] = ("Pet", "I wear", choice(["a **Spangenhelm**", "a **Galea**", "no helm at all"]))

        # personality question
        char['bio_personality'] = ("I use my", choice(["**Charm** to overcome trouble", "**Dignity** to overcome trouble", "**Ferocity** to overcome trouble"]))

        # race question
        char['bio_race_1'] = ('', '')
        char['bio_race_2'] = ('', '')
        char['bio_race_3'] = ('', '')
        if char['race'] == "Asura":
            char['bio_race_1'] = ("College", "I'm a member of the College of", choice(["**Statics**", "**Dynamics**", "**Synergetics**"]))
            char['bio_race_2'] = ("Creation", "My first creation was", choice(["the **VAL-A golem**", "a **Transatmospheric Converter**", "an **Infinity Ball**"]))
            char['bio_race_3'] = ("Advisor", "My first advicsor was", choice(["**Bronk**", "**Zinga**", "**Blipp**", "**Canni**"]))
        if char['race'] == "Charr":
            char['bio_race_1'] = ("Legion", "I am proud to be", choice(["a **Blood Legion** soldier", "an **Ash Legion** soldier", "an **Iron Legion** soldier"]))
            char['bio_race_2'] = ("Partner", "My sparring is", choice(["**Maverick** the soldier", "**Euryale** the elementalist", "**Clawspur** the thief", "**Dinky** the guardian", "**Reeva** the engineer"]))
            char['bio_race_3'] = ("Father", "My father is", choice(["a **Loyal Soldier**", "a **Sorcerous Shaman**", "a **Honorless Gladium**"]))
        if char['race'] == "Human":
            char['bio_race_1'] = ("Upbringing", "I grew up", choice(["as a **Street Rat**", "as a **Commoner**", "among the **Nobility**"]))
            char['bio_race_2'] = ("Regret", "My biggest regret is", choice(["my **Unknown Parents**", "my **Dead Sister**", "a **Missed Opportunity**"]))
            char['bio_race_3'] = ("Blessing", "I was blessed by", choice(["**Dwayna**", "**Grenth**", "**Balthazar**", "**Melandru**", "**Lyssa**", "**Kormir**"]))
        if char['race'] == "Norn":
            char['bio_race_1'] = ("Quality", "My most important quality is the", choice(["**Strength** to defeat acient foes", "**Cunning** to protect the spirits", "**Intuition** to guard the Mists"]))
            char['bio_race_2'] = ("Shameful Event", "In a recent Moot, I", choice(["**blacked out**", "**got in a fight**", "**lost an heirloom**"]))
            char['bio_race_3'] = ("Guardian Spirit", "My Guardian Spirit is", choice(["**Bear**", "**Snow Leopard**", "**Wolf**", "**Raven**"]))
        if char['race'] == "Sylvari":
            char['bio_race_1'] = ("Vision", "I had a vision of the", choice(["**White Stag**", "**Green Knight**", "**Shield of the Moon**"]))
            char['bio_race_2'] = ("Ventari's Teaching", "The most important of Ventari's teaching is", choice(["**Act with wisdom, but act.**", "**All things have a right to grow.**", "**Where life goes, so too, should you.**"]))
            char['bio_race_3'] = ("Cycle", "The Pale Tree awakened me during", choice(["the **Cycle of Dawn**", "the **Cycle of Noon**", "the **Cycle of Dusk**", "the **Cycle of Night**"]))

    def get_colour(self, char):
        if char['profession'] == "Elementalist":
            return 0xF68A87
        if char['profession'] == "Engineer":
            return 0xD09C59
        if char['profession'] == "Guardian":
            return 0x72C1D9
        if char['profession'] == "Mesmer":
            return 0xB679D5
        if char['profession'] == "Necromancer":
            return 0x52A76F
        if char['profession'] == "Ranger":
            return 0x8CDC82
        if char['profession'] == "Revenant":
            return 0xD16E5A
        if char['profession'] == "Thief":
            return 0xC08F95
        if char['profession'] == "Warrior":
            return 0xFFD166
        return 0xBBBBBB

    def get_thumbnail(self, char):
        if char['profession'] == "Elementalist":
            return "https://wiki.guildwars2.com/images/a/a2/Elementalist_icon.png"
        if char['profession'] == "Engineer":
            return "https://wiki.guildwars2.com/images/4/41/Engineer_icon.png"
        if char['profession'] == "Guardian":
            return "https://wiki.guildwars2.com/images/c/cc/Guardian_icon.png"
        if char['profession'] == "Mesmer":
            return "https://wiki.guildwars2.com/images/3/3a/Mesmer_icon.png"
        if char['profession'] == "Necromancer":
            return "https://wiki.guildwars2.com/images/6/62/Necromancer_icon.png"
        if char['profession'] == "Ranger":
            return "https://wiki.guildwars2.com/images/9/9c/Ranger_icon.png"
        if char['profession'] == "Revenant":
            return "https://wiki.guildwars2.com/images/8/89/Revenant_icon.png"
        if char['profession'] == "Thief":
            return "https://wiki.guildwars2.com/images/d/d8/Thief_icon.png"
        if char['profession'] == "Warrior":
            return "https://wiki.guildwars2.com/images/c/c8/Warrior_icon.png"
        return None

    def get_icon(self, char):
        if char['race'] == "Asura":
            return "https://wiki.guildwars2.com/images/1/1f/Asura_tango_icon_20px.png"
        if char['race'] == "Charr":
            return "https://wiki.guildwars2.com/images/f/fa/Charr_tango_icon_20px.png"
        if char['race'] == "Human":
            return "https://wiki.guildwars2.com/images/e/e1/Human_tango_icon_20px.png"
        if char['race'] == "Norn":
            return "https://wiki.guildwars2.com/images/3/3d/Norn_tango_icon_20px.png"
        if char['race'] == "Sylvari":
            return "https://wiki.guildwars2.com/images/2/29/Sylvari_tango_icon_20px.png"
        return None

    @commands.command(pass_context=True, no_pm=True)
    async def newchar(self, ctx, *filters):
        """Create a new random character
        Example:
        !newchar
        """

        # Char randomizer
        char = {}
        self.random_race(char)
        self.random_gender(char)
        self.random_profession(char)
        self.random_bio(char)

        # Generate Embed
        title = ""
        description = ""
        colour = self.get_colour(char)

        embed = discord.Embed(title=title, description=description, colour=colour)
        embed.set_thumbnail(url=self.get_thumbnail(char))
        embed.set_author(name=ctx.message.author.name, icon_url=self.get_icon(char))
        embed.add_field(name="Profession", value=char['profession'])
        embed.add_field(name="Race & Gender", value="{} {}".format(char['gender'], char['race']))
        embed.add_field(name="Biography - {}".format(char['bio_profession'][0]), value="{} {}".format(char['bio_profession'][1], char['bio_profession'][2]), inline=False)
        embed.add_field(name="Biography - Personality", value="{} {}".format(char['bio_personality'][0], char['bio_personality'][1]), inline=False)
        embed.add_field(name="Biography - {}".format(char['bio_race_1'][0]), value="{} {}".format(char['bio_race_1'][1], char['bio_race_1'][2]), inline=False)
        embed.add_field(name="Biography - {}".format(char['bio_race_2'][0]), value="{} {}".format(char['bio_race_2'][1], char['bio_race_2'][2]), inline=False)
        embed.add_field(name="Biography - {}".format(char['bio_race_3'][0]), value="{} {}".format(char['bio_race_3'][1], char['bio_race_3'][2]), inline=False)

        # Random response
        response = choice([
            "I think you will like this one.",
            "Have you tried this ?",
            "A great character for a great person.",
            "How about that ?",
            "Here's what I thought for you.",
            "Maybe this one ? Not sure. You're a bit hard to grasp.",
        ])

        await ctx.send(response, embed=embed)
        #try:
        #    await ctx.trigger_typing()

        #    msg = " ".join(search)
        #    results = await self.query_wiki(msg)

        #    if results:
        #        if len(results) == 1:
        #            await ctx.send("{} : <{}>".format(results[0][0], results[0][1]))
        #        else:
        #            res = "Ok, I have found these results for \"{}\":".format(msg)
        #            for i, row in enumerate(results):
        #                res = "{}\n{} : <{}>".format(res, row[0], row[1])
        #                if i >= 9: #prevents it to show more than 10 results
        #                    break
        #            if len(results) > 10:#if it found more than 10 results, show a notice plus a link to the full search page
        #                link = "http://wiki.guildwars2.com/index.php?title=Special%3ASearch&fulltext=1&"+urllib.parse.urlencode({'search' : msg}) #the "fulltext" param is to avoid a redirect in case there is a page matching exactly the search terms
        #                res = "{}\n\nMore than 10 results were found and these are just the first 10.\nTry to narrow your search terms to be more specific or check the full results at <{}>.".format(res,link)
        #            await ctx.send("{}".format(res))
        #    else:
        #        await ctx.send("Hmm, nothing was found for \"{}\".".format(msg))

        #except Exception as e:
        #    print(e)
        #    traceback.print_exc()
        #    await ctx.send("Something went wrong.")

