from redbot.core.bot import Red
from .money import Money


def setup(bot: Red):
    bot.add_cog(Money(bot))
