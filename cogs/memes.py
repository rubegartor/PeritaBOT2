from discord.ext import commands
from run import Bot
from requests import get
from utils import funcs
import discord
import random

class Memes:
  def __init__(self, bot):
    self.bot = bot
    self.Bot = Bot()

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
      meme = funcs.toList(funcs.toFiles(self.Bot.memes_path))
      for k,v in meme:
        if not k in prefixes:
          prefixes.append(k)
      await self.bot.send_typing(ctx.message.channel)
      await self.bot.say('**__Aquí tienes una lista de los prefijos disponibles:__**\n' + ', '.join(prefixes))
    except Exception as e:
      print('Command memes prefixes: [{}] {}'.format(type(e).__name__, e))

  @memes.command(pass_context = True)
  async def push(self, ctx, URL, name):
    """Añade un meme a través de una URL"""
    try:
      if self.Bot.root_role in [y.name.lower() for y in ctx.message.author.roles]:
        data = funcs.toFiles(self.Bot.memes_path)
        memes = [x for x in data]
        if "_" in name:
          if name[len(name) - 3:] in ['png', 'jpg', 'gif']:
            if name in memes:
              await self.bot.send_typing(ctx.message.channel)
              await self.bot.say('Ya hay un meme con ese nombre (`{}`)'.format(name))
            else:
              with open(self.Bot.memes_path + name, 'wb') as file:
                file.write(get(URL).content)
                file.close()
              await self.bot.send_typing(ctx.message.channel)
              await self.bot.say(':white_check_mark: Nuevo meme añadido!')
          else:
            await self.bot.send_typing(ctx.message.channel)
            await self.bot.say('El nombre de la imagen necesita formato (ej: prefijo_nombre.png)')
        else:
          await self.bot.send_typing(ctx.message.channel)
          await self.bot.say('Necesitas especificar el prefijo en el nombre del meme')
      else:
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.say('`No tienes permiso para usar este comando`')
    except Exception as e:
      print('Command memes push: [{}] {}'.format(type(e).__name__, e))

  @memes.command(pass_context = True)
  async def show(self, ctx, prefix : str):
    """Muestra los memes por prefijo"""
    try:
      prefixes = funcs.toList(funcs.toFiles(self.Bot.memes_path))
      selected = [(x, y) for x, y in prefixes if x == prefix]

      await self.bot.send_file(ctx.message.channel, self.Bot.memes_path + random.choice(selected)[1])
    except Exception as e:
      if e.errno == 2:
        await self.bot.say('No existen memes con  el prefijo: `{}`'.format(prefix))
      else:
        print('Command memes show: [{}] {}'.format(type(e).__name__, e))

def setup(bot):
  bot.add_cog(Memes(bot))
