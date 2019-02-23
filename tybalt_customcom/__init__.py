from .tybalt_customcom import TybaltCustomCommands

def setup(bot):
    bot.add_cog(TybaltCustomCommands(bot))

