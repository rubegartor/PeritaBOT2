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
  async def deletethis(self, ctx):
    """Se realiza una votación para eliminar el último mensaje del canal"""
    try:
      message = ctx.message
      res_count = 0
      poll_time = 60
      results = [0, 0]
      to_remove = []

      async for x in self.bot.logs_from(ctx.message.channel, limit = 2):
        to_remove.append(x)

      await self.bot.add_reaction(message, '✅')
      await self.bot.add_reaction(message, '🚫')
      await self.bot.send_typing(message.channel)
      alert_msg = await self.bot.say('¡Quedan {} segundos para que acabe la votación!'.format(poll_time))
      to_remove.append(alert_msg)

      await self.bot.send_message(to_remove[1].author, '¡Hey! Uno de tus mensajes quiere ser eliminado')

      for i in range(0, poll_time):
        await asyncio.sleep(1)
        poll_time -= 1
        await self.bot.edit_message(alert_msg, '¡Quedan {} segundos para que acabe la votación!'.format(poll_time))
      for emoji in message.reactions:
        if res_count < 2:
          res_count += 1
          results[res_count - 1] = emoji.count
        else:
          break

      if results[0] > results[1]:
        await self.bot.delete_messages(to_remove)
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.say(":white_check_mark: Votación aceptada")
      elif results[0] < results[1]:
        to_remove.remove(to_remove[1])
        await self.bot.delete_messages(to_remove)
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.say(":no_entry_sign: Votacion rechazada")
      else:
        to_remove.remove(to_remove[1])
        await self.bot.delete_messages(to_remove)
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.say(":interrobang: Votación nula")
    except Exception as e:
      print('Command deletethis: {}'.format(e))

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
          await self.bot.say(''.join(msg))
          await asyncio.sleep(1)
    except Exception as e:
      print('Command spam: {}'.format(e))

def setup(bot):
  bot.add_cog(Moderation(bot))
