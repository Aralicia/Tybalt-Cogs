from .tybalt_ms import TybaltMegaserver

def setup(bot):
    bot.add_cog(TybaltMegaserver(bot))

