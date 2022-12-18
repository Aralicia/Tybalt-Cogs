from .tybalt_identity import TybaltIdentity

async def setup(bot):
    identity = TybaltIdentity(bot)
    bot.add_cog(identity)
    await identity.choose_identity()

