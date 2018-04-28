from discord.ext import commands
from run import Bot
from requests import get
import discord
import configparser
import random
import aiohttp
import json
import os

class Memes:
  def __init__(self, bot):
    self.bot = bot
    self.Bot = Bot()

    def getConfig(dict, key):
      config = configparser.ConfigParser()
      config.read(self.Bot.config + 'config.ini')
      return config[dict][key]

    self.path = getConfig('Memes', 'path')

  def toList(array):
    return [(x.split('_')[0], x) for x in array]

  def toFiles(path):
      return [x for x in os.listdir(path)]

  @commands.group(pass_context = True)
  async def memes(self, ctx):
    """memes info"""
    if ctx.invoked_subcommand is None:
      await self.bot.say('Prueba con: `{}memes help` para maś información'.format(self.Bot.prefix))

  @memes.command(pass_context = True)
  async def help(self, ctx):
    """Muestra el mensaje de ayuda"""
    await self.bot.send_typing(ctx.message.channel)
    color = discord.Color.default()
    if ctx.message.server is not None:
      color = ctx.message.server.me.color
    e = discord.Embed(color = color)
    e.add_field(name = '{}memes help'.format(self.Bot.prefix), value = 'Muestra el mensaje de ayuda para el comando {}memes'.format(self.Bot.prefix))
    e.add_field(name = '{}memes show <prefix>'.format(self.Bot.prefix), value = 'Busca tu meme perfecto')
    e.add_field(name = '{}memes prefixes'.format(self.Bot.prefix), value = 'Muestra una lista de los prefijos disponibles')
    e.add_field(name = '{}memes push [URL] [name]'.format(self.Bot.prefix), value = 'Añade un meme nuevo a la colección')
    e.set_thumbnail(url = 'https://i.imgur.com/u2ldGKI.jpg')
    await self.bot.send_message(ctx.message.channel, embed = e)

  @memes.command(pass_context = True, aliases = ['prefix'])
  async def prefixes(self, ctx):
    """Muestra los prefijos disponibles"""
    try:
      prefixes = []
      meme = Memes.toList(Memes.toFiles(self.path))
      for k,v in meme:
        if not k in prefixes:
          prefixes.append(k)
      await self.bot.send_typing(ctx.message.channel)
      await self.bot.say('**__Aquí tienes una lista de los prefijos disponibles:__**\n' + ', '.join(prefixes))
    except Exception as e:
      print('Command memes prefixes: {}'.format(e))

  @memes.command(pass_context = True)
  async def push(self, ctx, URL, name):
    """Añade un meme a través de una URL"""
    try:
      if self.Bot.root_role in [y.name.lower() for y in ctx.message.author.roles]:
        data = Memes.toFiles(self.path)
        memes = [x for x in data]
        if "_" in name:
          if name in memes:
            await self.bot.send_typing(ctx.message.channel)
            await self.bot.say('Ya hay un meme con ese nombre (`{}`)'.format(name))
          else:
            with open(self.path + name, 'wb') as file:
              file.write(get(URL).content)
              file.close()
            await self.bot.send_typing(ctx.message.channel)
            await self.bot.say(':white_check_mark: Nuevo meme añadido!')
        else:
          await self.bot.send_typing(ctx.message.channel)
          await self.bot.say('Necesitas especificar el prefijo en el nombre del meme')
      else:
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.say('`No tienes permiso para usar este comando`')
    except Exception as e:
      print('Command memes push: {}'.format(e))

  @memes.command(pass_context = True)
  async def show(self, ctx, prefix : str):
    """Muestra los memes por prefijo"""
    try:
      prefixes = Memes.toList(Memes.toFiles(self.path))
      selected = []

      for x, y in prefixes:
        if x == prefix:
          selected.append((x, y))

      await self.bot.send_file(ctx.message.channel, self.path + random.choice(selected)[1])
    except Exception as e:
      print('Command memes show: {}'.format(e))

def setup(bot):
  bot.add_cog(Memes(bot))
