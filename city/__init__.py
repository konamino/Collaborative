from .city import City

async def setup(bot):
    cog = City(bot)
    bot.add_cog(cog)
