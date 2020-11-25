import discord
import asyncio
from typing import Optional
from datetime import datetime
from contextlib import suppress
from .helpchannelnames import hcn
from .helpchannelembed import Embed
from validator_collection import validators
from redbot.core.utils.menus import start_adding_reactions
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
from redbot.core import commands, checks, Config, bank, modlog
from redbot.core.utils.predicates import ReactionPredicate, MessagePredicate

class Hc(commands.Cog):
  """Setup rotating help channels."""
      
  def __init__(self):
      self.config = Config.get_conf(self, 5937402754, force_registration=True)
      default_guild = {
          "dormant_category": None,
          "closed_category": None,
          "open_category": None,
          "role": None,
          "message": None,
          "active": [],
          "modlog": True,
          "closed": [],
          "dormant": [],
          "adamantium": None,
          "berylium": None,
          "copper": None,
          "dubnium": None,
          "esarine": None,
      }
      self.config.register_guild(**default_guild)  

  @staticmethod
  async def register_casetypes():
      new_types = [
          {
              "name": "open_help",
              "default_setting": True,
              "image": "\N{BALLOT BOX WITH BALLOT}\N{VARIATION SELECTOR-16}",
              "case_str": "Help Channel Opened",
          }
      ]
      await modlog.register_casetypes(new_types)
        
  @commands.group()
  @checks.admin()
  async def helpchannel(self, ctx):
    """Help channel configuration."""
      
  @helpchannel.group()
  async def category(self, ctx):
    """Category configuration."""
      
  @helpchannel.command()
  async def role(self, ctx, role: discord.Role):
    """Helper role configuration."""
    await self.config.guild(ctx.guild).role.set("role", value=role.id)
    await ctx.send(f"{role.mention} are now help channel helpers.")
      
  @category.command()
  async def open(self, ctx, *, category: discord.CategoryChannel):
    """Open category configuration."""
    await self.config.guild(ctx.guild).open_category.set("open", value=category.id)
    await ctx.send(f"{category.mention} will now be used for open help channels.")
      
  @category.command()
  async def closed(self, ctx, *, category: discord.CategoryChannel):
    """Closed category configuration."""
    await self.config.guild(ctx.guild).closed_category.set("closed", value=category.id)
    await ctx.send(f"{category.mention} will now be used for closed help channels.")
      
  @category.command()
  async def dormant(self, ctx, *, category: discord.CategoryChannel):
    """Dormant category configuration."""
    await self.config.guild(ctx.guild).dormant_category.set("dormant", value=category.id)
    await ctx.send(f"{category.mention} will now be used for dormant help channels.")
    
  @helpchannel.group()
  async def reset(self, ctx):
    """Resets certain configurations."""
    
  @reset.command(name="role")
  async def _role(self, ctx: commands.Context):
    """Resets the role that is used for managing help channels."""
    role = await self.config.guild(ctx.guild).get_raw("role")
    if role is not None:
      await self.removal(ctx, role)
      await ctx.send(f"{role.mention} removed.")
    else:
      await ctx.send("You don't have a role configured.")
      
  @reset.command(name="open")
  async def _open(self, ctx: commands.Context):
    """Resets and deletes the open category and channels within."""
    open_category = await self.config.guild(ctx.guild).get_raw("open")
    if open_category is not None:
      await self.removal(ctx, open_category)
      await ctx.send("Open category wiped.")
    else:
      await ctx.send("You haven't setup an open category yet.")

  @reset.command(name="closed")
  async def _closed(self, ctx: commands.Context):
    """Resets and deletes the closed category."""
    closed_category = await self.config.guild(ctx.guild).get_raw("closed")
    if closed_category is not None:
      await self.removal(ctx, closed_category)
      await ctx.send("Closed category wiped.")
    else:
      await ctx.send("You haven't setup an closed category yet.")

  @reset.command(name="dormant")
  async def _dormant(self, ctx: commands.Context):
    """Resets and deletes the dormant category."""
    dormant_category = await self.config.guild(ctx.guild).get_raw("dormant")
    if dormant_category is not None:
      await self.removal(ctx, dormant_category)
      await ctx.send("Dormant category wiped.")
    else:
      await ctx.send("You haven't setup an dormant category yet.")
  
  @commands.command()
  async def manualsetup(self, ctx):
    """Configures channels and roles automatically."""
    settings = await self.config.guild(ctx.guild).all()
    if not settings["role"]:
      role = await ctx.guild.create_role(
        name="Helpers", hoist=True, mentionable=False, reason="Help channel manualsetup."
      )
      await self.config.guild(ctx.guild).role.set(role.id)
      await ctx.send("Helper role has been configured.")
      if not settings["open_category"]:
        category = await ctx.guild.create_category(
          name="Open Help Channels", reason="Help channel manualsetup."
        )
        await self.config.guild(ctx.guild).open_category.set(category.id)
        await ctx.send("Category for open help channels has been created.")
      if not settings["closed_category"]:
        category = await ctx.guild.create_category(
          name="Closed Help Channels", reason="Help channel manualsetup."
        )
        await self.config.guild(ctx.guild).dormant_category.set(category.id)
        await ctx.send("Category for closed help channels has been created.")
      if not settings["dormant_category"]:
        category = await ctx.guild.create_category(
          name="Dormant Help Channels", reason="Help channel manualsetup."
        )
        await self.config.guild(ctx.guild).closed_category.set(category.id)
        await ctx.send("Category for dormant help channels has been created.")
      if not settings["adamantium"]:
        channel = await ctx.guild.create_text_channel(
          "adamantium",
          category=ctx.guild.get_raw("open"),
          topic="This is a rotating help channel.",
          reason="Help channel manualsetup."
        )
        await self.config.guild(ctx.guild).adamantium.set(channel.id)
        await ctx.send("**1/5 Help Channels Created.**")
      if not settings["berylium"]:
        channel = await ctx.guild.create_text_channel(
          "berylium",
          category=ctx.guild.get_raw("open"),
          topic="This is a rotating help channel.",
          reason="Help channel manualsetup."
        )
        await self.config.guild(ctx.guild).berylium.set(channel.id)
        await ctx.send("**2/5 Help Channels Created.**")
      if not settings["copper"]:
        channel = await ctx.guild.create_text_channel(
          "copper",
          category=ctx.guild.get_raw("open"),
          topic="This is a rotating help channel.",
          reason="Help channel manualsetup."
        )
        await self.config.guild(ctx.guild).copper.set(channel.id)
        await ctx.send("**3/5 Help Channels Created.**")
      if not settings["dubnium"]:
        channel = await ctx.guild.create_text_channel(
          "copper",
          category=ctx.guild.get_raw("open"),
          topic="This is a rotating help channel.",
          reason="Help channel manualsetup."
        )
        await self.config.guild(ctx.guild).dubnium.set(channel.id)
        await ctx.send("**4/5 Help Channels Created.**")
      if not settings["esarine"]:
        channel = await ctx.guild.create_text_channel(
          "esarine",
          category=ctx.guild.get_raw("open"),
          topic="This is a rotating help channel.",
          reason="Help channel manualsetup."
        )
        await self.config.guild(ctx.guild).esarine.set(channel.id)
        await ctx.send("**5/5 Help Channels Created.**")
      else:
        await ctx.send("You have already completed the setup process!")
        
      
    
  @commands.command()
  async def gethelp(self, ctx, *, reason: Optional[str] = "No context provided."):
    """Get support."""
    if await self._check_settings(ctx):
      settings = await self.config.guild(ctx.guild).all()
      await self.config.guild(ctx.guild).open_category.set(
        settings["open_category"] + 1
      )
    found = False
    for channel in ctx.guild.channels:
      if channel.name == name.lower():
        found = True
      if not Found:
        if settings["modlog"]:
          await modlog.create_case(
            ctx.bot,
            ctx.guild,
            ctx.message.created_at,
            action_type="open_help",
            user=ctx.author,
            moderator=ctx.author,
            reason=reason,
          )
        overwrite = {
          ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
          ctx.author: discord.PermissionOverwrite(
            read_messages=True,
            send_messages=True,
            embed_links=True,
            attach_files=True,
          ),
          ctx.guild.get_role(settings["role"]): discord.PermissionOverwrite(
            read_messages=True,
            send_messages=True,
            embed_links=True,
            attach_files=True,
            manage_messages=True,
          ),
        }
        helpchannel = await ctx.guild.create_text_channel(
          name,
          overwrites=overwrite,
          category=ctx.guild.get_channel(settings["open_category"]),
          topic=reason,
        )
        await helpchannel.send(settings["message"])
        embed = Embed.create(
          self, ctx, title=name,
          description=reason,
          timestamp=datetime.utcnow(),
        ).set_footer(text="Last updated at:")
        message = await ctx.guild.get_channel(settings["channel"]).send(embed=embed)
        async with self.config.guild(ctx.guild).active() as active:
          active.append((helpchannel.id, message.id))
      else:
        await ctx.send(f"You already have an open help channel, {ctx.author.name}.")
    else:
        await ctx.send(
          f"You have not configured all the settings needed to operate the help channels.\n"
          "You can use {ctx.clean_prefix}helpchannel to configure these required settings."
        )
            
  async def _check_settings(self, ctx: commands.Context) -> bool:
    settings = await self.config.guild(ctx.guild).all()
    count = 0
    if settings["closed_category"]:
        count += 1
    else:
        await ctx.send("Category for closed help channels has not been set up yet.")
    if settings["open_category"]:
        count += 1
    else:
        await ctx.send("Category for open help channels has not been set up yet.")
    if settings["dormant_category"]:
        count += 1
    else:
        await ctx.send("Category for dormant help channels has not been set up yet.")
    if count == 3:
        return True
    else:
        return False
      
  async def removal(self, ctx: commands.Context, action: str):
    message = "Would you like to reset the {}?".format(action)
    can_react = ctx.channel.permissions_for(ctx.me).add_reactions
    if not can_react:
        message += " (y/n)"
    question: discord.Message = await ctx.send(message)
    if can_react:
        start_adding_reactions(
            question, ReactionPredicate.YES_OR_NO_EMOJIS
        )
        pred = ReactionPredicate.yes_or_no(question, ctx.author)
        event = "reaction_add"
    else:
        pred = MessagePredicate.yes_or_no(ctx)
        event = "message"
    try:
        await ctx.bot.wait_for(event, check=pred, timeout=20)
    except asyncio.TimeoutError:
        await question.delete()
        await ctx.send("Okay then :D")
    if not pred.result:
        await question.delete()
        return await ctx.send("Canceled!")
    else:
        if can_react:
            with suppress(discord.Forbidden):
                await question.clear_reactions()
    await self.config.guild(ctx.guild).set_raw(action, value=None)
    await ctx.send("Removed the {}!".format(action))
  
      
#  @helpchannel.command()
#  async def modlog(self, ctx):
#      """Decides if help channel events should go to modlog."""
#      message = "Would you like to enable the modlog?"
#      can_react = ctx.channel.permissions_for(ctx.me).add_reactions
#      if not can_react:
#          message += " (y/n)"
#      question: discord.Message = await ctx.send(message)
#      if can_react:
#          start_adding_reactions(
#              question, ReactionPredicate.YES_OR_NO_EMOJIS
#          )
#          pred = ReactionPredicate.yes_or_no(question, ctx.author)
#          event = "reaction_add"
#      else:
#          pred = MessagePredicate.yes_or_no(ctx)
#          event = "message"
#      try:
#          await ctx.bot.wait_for(event, check=pred, timeout=20)
#      except asyncio.TimeoutError:
#          await question.delete()
#          await ctx.send("Okay then :D")
#      if not pred.result:
#          await question.delete()
#          return await ctx.send("Timed out.")
#      else:
#          if can_react:
#              with suppress(discord.Forbidden):
#                  await question.clear_reactions()
#      await self.config.guild(ctx.guild).set_raw(modlog, value=None)
#      await ctx.send("Updates will no longer be sent to modlog.")

