from .tybalt_feeds import TybaltFeeds

def setup(bot):
    bot.add_cog(TybaltFeeds(bot))

