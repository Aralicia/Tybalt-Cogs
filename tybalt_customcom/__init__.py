from .tybalt_customcom import CustomCommands

def setup(bot):
    bot.add_cog(CustomCommands(bot))

