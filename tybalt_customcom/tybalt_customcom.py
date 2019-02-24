import discord
import random
from redbot.core import commands
from redbot.core.utils.chat_formatting import pagify, box

class TybaltCustomCommands(commands.Cog):
    """TybaltCustomCommands."""

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        cc_cog = self.bot.get_cog("CustomCommands")
        cc_list_command = commands.command('list')(self.cc_list)
        cc_cog.cc_list = cc_list_command
        cc_cog.customcom.remove_command('list')
        cc_cog.customcom.add_command(cc_list_command)


    async def cc_list(self, ctx: commands.Context):
        """List all available custom commands.

        """

        cc_cog = self.bot.get_cog("CustomCommands")
        cc_guild = cc_cog.config.guild(ctx.guild)
        cc_dict = await cc_guild.commands()
        
        if not cc_dict:
            await ctx.send(
                _(
                    "There are no custom commands in this server."
                    " Use `{command}` to start adding some."
                ).format(command="{}customcom create".format(ctx.prefix))
            )
            return

        results = []
        for command, body in sorted(cc_dict.items(), key=lambda t: t[0]):
            results.append('{}{}'.format(ctx.prefix, command))
        
        content = "\n".join(results)
        pages = list(pagify(content, page_length=1920))
        for page in pages:
            await ctx.author.send(box(page))

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
            
