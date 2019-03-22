import discord
from utils.settings import GlobalVars, Funcs
from discord.ext import commands
import json
import random
import logging

globalVars = GlobalVars()
logging.getLogger('discord').setLevel(logging.CRITICAL)
logging.basicConfig(filename=globalVars.path + 'peritabot.log', level=logging.INFO, filemode='a', format='[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s', datefmt='%d-%m-%Y:%H:%M:%S')

class Core():
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def react(self, ctx, *args):
    """Reacciona con emojis al último mensaje"""
    try:
      allowed = 'abcdefghijklmnopqrstuvwxyz'
      data = json.loads(Funcs().readFile(globalVars.path + 'db/emojis.json'))
      args = ''.join(args).lower()
      msg = await ctx.channel.history(limit=2).flatten()

      await msg[0].delete()

      for a in args:
        if a not in allowed:
          args = args.replace(a, '')

      for i in args:
        await msg[1].add_reaction(data[0][i])
    except Exception as e:
      logging.error('[ERROR] {}: {}'.format(type(e).__name__, e))

  @commands.command()
  async def avatar(self, ctx):
    """Muestra el avatar de los usuarios mencionados"""
    try:
      for user in ctx.message.mentions:
        if user.avatar_url != "":
          embed = discord.Embed(title = '@{} avatar'.format(user.name), color = user.color)
          embed.set_image(url = user.avatar_url)
          await ctx.send(embed = embed)
        else:
          await ctx.send(':exclamation: El usuario {} no tiene avatar'.format(user.name))
    except Exception as e:
      logging.error('[ERROR] {}: {}'.format(type(e).__name__, e))

  @commands.command(name='8ball')
  async def _8ball(self, ctx):
    """Preguntale a la bola mágica"""
    try:
      answers = ['Si', 'No']
      question = ' '.join(ctx.message.content.split()[1:])
      if '?' == question[-1] and len(question) > 1:
        await ctx.channel.send(random.choice(answers))
      else:
        await ctx.channel.send(':thinking: ¿Eso es una pregunta?')
    except IndexError:
      await ctx.channel.send('Preguntame algo...')
    except Exception as e:
      logging.error('[ERROR] {}: {}'.format(type(e).__name__, e))

  @commands.command()
  async def se(self, ctx, emoji:discord.Emoji):
    """Muestra la imagen original del emoji"""
    try:
      color = discord.Color.default()
      if ctx.message.guild is not None:
        color = ctx.message.guild.me.color
      embed = discord.Embed(title = emoji.name, color = color)
      embed.set_image(url = emoji.url)
      await ctx.channel.send(embed = embed)
    except Exception as e:
      logging.error('[ERROR] {}: {}'.format(type(e).__name__, e))

def setup(bot):
  bot.add_cog(Core(bot))