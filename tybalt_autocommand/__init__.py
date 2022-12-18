from .tybalt_autocommand import TybaltAutoCommand

def setup(bot):
    bot.add_cog(TybaltAutoCommand(bot))

