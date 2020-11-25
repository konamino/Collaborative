# Standard Library
import discord
import asyncio
import itertools
# Python Modules
from typing import Optional
from datetime import datetime
from contextlib import suppress
from validator_collection import validators
# Exterior Files
from .prosegur import Embed
# Redbot Core
from redbot.core import commands, checks, Config, bank, modlog
from redbot.core.errors import BalanceTooHigh
from redbot.core.utils.menus import start_adding_reactions
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
from redbot.core.utils.predicates import ReactionPredicate, MessagePredicate

class City(commands.Cog):
  """Emergency procedures to keep yourself busy!"""

  def __init__(self, bot):
      self.bot = bot
      self.config = Config.get_conf(self, 4093957493, force_registration=True)
      default_guild = {
        "ic": None,
        "ac": None,
        "esc": None,
        "ir": None,
        "ar": None,
        "esr": None,
      }
      self.config.register_guild(**default_guild)
      
  @commands.command()
  async def test(self, ctx):
    await ctx.author.send("Pong.")
    await ctx.message.delete()
        
  @commands.command()
  async def citysetup(self, ctx):
    """Set up your city!"""
    await ctx.send("**Loading...**")
    settings = await self.config.guild(ctx.guild).all()
    if not settings["ic"]:
      category = await ctx.guild.create_category(name="Industry", reason="Procedure Game")
      await self.config.guild(ctx.guild).ic.set(category.id)
      await ctx.send("<:success:777167188816560168> Industrial Category set!")
    if not settings["ac"]:
      category = await ctx.guild.create_category(name="Accommodation", reason="Procedure Game")
      await self.config.guild(ctx.guild).ac.set(category.id)
      await ctx.send("<:success:777167188816560168> Accommodation Category has been created!")
    if not settings["esc"]:
      category = await ctx.guild.create_category(name="Emergency Services", reason="Procedure Game")
      await self.config.guild(ctx.guild).esc.set(category.id)
      await ctx.send("<:success:777167188816560168> Emergency Services Category!")
    if not settings["ir"]:
      role = await ctx.guild.create_role(name="Industrial Workers 👷", hoist=True, mentionable=True, reason="Procedure Game")
      await self.config.guild(ctx.guild).ir.set(role.id)
      await ctx.send(f"<:success:777167188816560168> {role.mention} has been created!")
    if not settings["ar"]:
      role = await ctx.guild.create_role(name="Home Manager 🏘️", hoist=True, mentionable=True, reason="Procedure Game")
      await self.config.guild(ctx.guild).ar.set(role.id)
      await ctx.send(f"<:success:777167188816560168> {role.mention} has been created!")
    if not settings["esr"]:
      role = await ctx.guild.create_role(name="Emergency Services 👮", hoist=True, mentionable=True, reason="Procedure Game")
      embed = Embed.create(
        self, ctx, title="<:success:777167188816560168> Your city has been constructed.",
        description=f"Use `{ctx.clean_prefix}cityhelp` for more information."
      )
      await self.config.guild(ctx.guild).esr.set(role.id)
      await ctx.send(f"<:success:777167188816560168> {role.mention} has been created!")
      await ctx.send(embed=embed)
      
  @commands.command()
  async def cityhelp(self, ctx):
    """Get help on how your city will work!"""
    embed = Embed.create(
      self, ctx, title="City Information",
      description=(
        f"Firstly, you can create your city using {ctx.clean_prefix}citysetup. Your city will operate in three different categories, each of which will contain civilians requiring help!"
        "Your objective is to server for your newly formed city, keep everyone happy, prevent deaths and grow your population!"
      )
    )
    await ctx.send(embed=embed)
#    elif settings ["ic", "ac", "esc", "ir", "ar", "esr"]:
#      await ctx.send("Test")
     
#      async def canceloption(self, ctx, commands.Context):
#      message = "Are you sure?"
#      can_react = ctx.channel.permissions_for(ctx.me).add_reactions
#      if not can_react:
#        message += " (y/n)"
#      question: discord.Message = await ctx.send(message)
#      if can_react:
#        start_adding_reactions(
#         question, ReactionPredicate.YES_OR_NO_EMOJIS
#        )
#        pred = ReactionPredicate.yes_or_no(question, ctx.author)
#        event = "reaction_add"
#      else:
#        pred = ReactionPredicate.yes_or_no(ctx)
#        event = "message"
#      try:
#        await ctx.bot.wait_for(event, check=pred, timeout=20)
#      except asyncio.TimeoutError:
#        await question.delete()
#        await ctx.send("You timed out!")
#      if not pred.result:
#        await question.delete()
#        return await ctx.send("Cancelled the city construction.")
#      else:
#        if can_react:
#          with suppress(discord.Forbidden):
#            await question.clear_reactions()
#      await self.config.guild(ctx.guild).set_raw(value=None)
#      await ctx.send("Let's build our city then!")
