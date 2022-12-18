import discord
import random
from redbot.core import checks, commands
from redbot.core import Config
from discord.ext import tasks
from discord import Message

class TybaltMisc(commands.Cog):
    """Tybalt misc features."""

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    def cog_unload(self):
        #self.ticker.cancel()
        pass

    @commands.command(pass_context=True, no_pm=True)
    @checks.has_permissions(manage_messages=True)
    async def pick(self, ctx, picks="1", *data):
        if ctx.message.reference is not None and isinstance(ctx.message.reference.resolved, Message):
            message = discord.utils.get(self.bot.cached_messages, id=ctx.message.reference.message_id)
            if (message is None):
                message = await ctx.fetch_message(ctx.message.reference.message_id)
            reactions = message.reactions
            try:
                picks = int(picks)
            except Exception:
                return
            if picks < 1:
                picks = 1
            candidates = []

            for reaction in reactions:
                users = [user async for user in reaction.users()]
                candidates = list(set(candidates + users))

            random.shuffle(candidates)
            count = len(candidates)
            message = None
            if count == 0:
                message = "Sadly, there was no-one to pick."
            else:
                winners = candidates[0:picks]
                if picks == 1:
                    message = "The winner is {}!".format(winners[0].mention)
                elif count < picks :
                    message = "The winners are:\r\n{}".format(self.pick_list_winners(winners))
                    if picks-count == 1:
                        message = "{}\r\n\r\nThere could have been 1 more winner!".format(message)
                    else:
                        message = "{}\r\n\r\nThere could have been {} more winners!".format(message, picks-count)
                else:
                    message = "The winners are:\r\n{}".format(self.pick_list_winners(winners))
            if message is not None:
                await ctx.send(message, reference=ctx.message)
 
    def pick_list_winners(self, winners):
        mentions = []
        for winner in winners:
            mentions.append(winner.mention)

        return "\r\n• ".join(mentions);

