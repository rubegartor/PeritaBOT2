from discord.ext import commands
from run import Bot
import discord
import logging
import asyncio

class Moderation:
  def __init__(self, bot):
    self.bot = bot
    self.Bot = Bot()

  @commands.command(pass_context = True)
  async def prune(self, ctx, num):
    """Elimina una lista de mensajes"""
    try:
      if self.Bot.root_role in [y.name.lower() for y in ctx.message.author.roles]:
        msg = []
        if int(num) <= 99 and int(num) != 0:
          async for x in self.bot.logs_from(ctx.message.channel, limit = int(num) + 1):
            msg.append(x)
          await self.bot.delete_messages(msg)
        else:
          await self.bot.send_typing(ctx.message.channel)
          await self.bot.say('El rango de mensajes es de: `1 - 99`')
      else:
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.say('`No tienes permiso para usar este comando`')
    except Exception as e:
      print('Command prune: {}'.format(e))

  @commands.command(pass_context = True)
  async def mute(self, ctx, member : discord.Member):
    """Mutea al usuario indicado del canal de voz"""
    try:
      if self.Bot.root_role in [y.name.lower() for y in ctx.message.author.roles]:
        if member.voice_channel != None:
          await self.bot.server_voice_state(member, mute = True)
          await self.bot.send_typing(ctx.message.channel)
          await self.bot.say(':no_entry_sign: El usuario `{}` ha sido muteado por `{}`'.format(member.name, ctx.message.author.name))
        else:
          await self.bot.send_typing(ctx.message.channel)
          await self.bot.say(':thinking: El usuario `{}` no esta en ningun canal de voz'.format(member.name))
      else:
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.say('`No tienes permiso para usar este comando`')
    except Exception as e:
      print('Command mute: {}'.format(e))

  @commands.command(pass_context = True)
  async def unmute(self, ctx, member : discord.Member):
    """Desmutea al usuario indicado del canal de voz"""
    try:
      if self.Bot.root_role in [y.name.lower() for y in ctx.message.author.roles]:
        if member.voice_channel != None:
          await self.bot.server_voice_state(member, mute = False)
          await self.bot.send_typing(ctx.message.channel)
          await self.bot.say(':white_check_mark: El usuario `{}` ha sido desmutado por `{}`'.format(member.name, ctx.message.author.name))
        else:
          await self.bot.send_typing(ctx.message.channel)
          await self.bot.say(':thinking: El usuario `{}` no esta en ningun canal de voz'.format(member.name))
      else:
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.say('`No tienes permiso para usar este comando`')
    except Exception as e:
      print('Command unmute: {}'.format(e))

  @commands.command(pass_context = True)
  async def ban(self, ctx, user):
    try:
      if self.Bot.root_role in [y.name.lower() for y in ctx.message.author.roles]:
        for user in ctx.message.mentions:
          await self.bot.ban(user, delete_message_days = 0)
      else:
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.say('`No tienes permiso para usar este comando`')
    except Exception as e:
      print('Command ban: {}'.format(e))

  @commands.command(pass_context = True)
  async def ban_list(self, ctx):
    try:
      if self.Bot.root_role in [y.name.lower() for y in ctx.message.author.roles]:
        data = [banned.name for banned in await self.bot.get_bans(ctx.message.server)]
        if len(data) > 0:
          await self.bot.send_typing(ctx.message.channel)
          await self.bot.say(' ,'.join(data))
        else:
          await self.bot.send_typing(ctx.message.channel)
          await self.bot.say('No se han encontrado usuarios baneados')
      else:
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.say('`No tienes permiso para usar este comando`')
    except Exception as e:
      print('Command ban_list: {}'.format(e))

  @commands.command(pass_context = True)
  async def unban(self, ctx, user):
    try:
      if self.Bot.root_role in [y.name.lower() for y in ctx.message.author.roles]:
        for banned in await self.bot.get_bans(ctx.message.server):
          if user == banned.name:
            print('{} - {}'.format(user, banned))
            await self.bot.unban(ctx.message.server, banned)
      else:
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.say('`No tienes permiso para usar este comando`')
    except Exception as e:
      print('Command unban: {}'.format(e))

  @commands.command(pass_context = True)
  async def spam(self, ctx):
    try:
      if self.Bot.root_role in [y.name.lower() for y in ctx.message.author.roles]:
        for i in range(10):
          msg = ctx.message.content.split()[1:]
          await self.bot.say(' '.join(msg))
          await asyncio.sleep(1)
    except Exception as e:
      print('Command spam: {}'.format(e))

def setup(bot):
  bot.add_cog(Moderation(bot))
