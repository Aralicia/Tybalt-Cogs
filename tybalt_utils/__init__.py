from .database import TybaltDatabase
from .gw2api import TybaltGW2API
from .tabmessage import TabMessages
from .utilcommands import UtilCommands

def setup(bot):
    bot.add_cog(TybaltDatabase())
    bot.add_cog(TybaltGW2API())
    bot.add_cog(TabMessages(bot))
    bot.add_cog(UtilCommands(bot));

