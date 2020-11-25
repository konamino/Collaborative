from .finance import Finance, is_owner_if_bank_global


def setup(bot):
    bot.add_cog(Finance(bot))
