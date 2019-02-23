import discord
import random
from redbot.core import commands

class TybaltCustomCommands(commands.Cog):
    """TybaltCustomCommands."""

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True)
    async def randcom(self, ctx):
        """execute a random custom command"""
        
        cc_cog = self.bot.get_cog("CustomCommands")
        if cc_cog is not None:
            guild_config = cc_cog.config.guild(ctx.guild)
            guild_commands = await guild_config.commands()
            guild_command_names = list(guild_commands)
            command_name = random.choice(guild_command_names)
            command = guild_commands[command_name]

            if isinstance(command['response'], list):
                response = random.choice(command['response'])
            else:
                response = command['response']

            raw_response = '{}{} \n{}'.format(ctx.prefix, command_name, response)

            fake_cc = commands.Command(ctx.invoked_with, cc_cog.cc_callback)
            fake_cc.params = cc_cog.prepare_args(raw_response)
            ctx.command = fake_cc

            await self.bot.invoke(ctx)
            if not ctx.command_failed:
                await cc_cog.cc_command(*ctx.args, **ctx.kwargs, raw_response=raw_response)
            
