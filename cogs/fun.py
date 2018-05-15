from discord.ext import commands
from run import Bot
import discord
import random
import aiohttp

class Fun:
  def __init__(self, bot):
    self.bot = bot
    self.Bot = Bot()

  @commands.command(pass_context = True, aliases=['cats'])
  async def cat(self, ctx):
    """Imágenes aleatorias de gatos"""
    # New API //-> http://aws.random.cat/meow
    try:
      color = discord.Color.default()
      if ctx.message.server is not None:
        color = ctx.message.server.me.color
      embed = discord.Embed(title = 'Random Cat', color = color)
      cat = ''
      while True:
        async with aiohttp.get('http://aws.random.cat/meow', headers={'User-Agent': 'Mozilla/5.0'}) as r:
          if r.status == 200:
            js = await r.json()
            cat = js['file']
        if not cat.endswith('.mp4') and cat != '':
          break
      embed.set_image(url = cat)
      await self.bot.send_typing(ctx.message.channel)
      await self.bot.send_message(ctx.message.channel, embed = embed)
    except Exception as e:
      print('Command cat: [{}] {}'.format(type(e).__name__, e))

  @commands.command(pass_context = True, aliases=['dogs'])
  async def dog(self, ctx):
    """Imágenes aleatorias de perros"""
    try:
      color = discord.Color.default()
      if ctx.message.server is not None:
        color = ctx.message.server.me.color
      embed = discord.Embed(title = 'Random Dog', color = color)
      async with aiohttp.get('https://dog.ceo/api/breeds/image/random', headers={'User-Agent': 'Mozilla/5.0'}) as r:
        if r.status == 200:
          js = await r.json()
          dog = js['message']
      embed.set_image(url = dog)
      await self.bot.send_typing(ctx.message.channel)
      await self.bot.send_message(ctx.message.channel, embed = embed)
    except Exception as e:
      print('Command dog: [{}] {}'.format(type(e).__name__, e))

  @commands.command(pass_context = True, name = '8ball')
  async def _8ball(self, ctx):
    """Preguntale a la bola mágica"""
    try:
      responses = ['Si', 'No']
      question = ' '.join(ctx.message.content.split()[1:])
      if '?' == question[-1] and len(question) > 1:
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.say(random.choice(responses))
      else:
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.say(':thinking: ¿Eso es una pregunta?')
    except Exception as e:
      print('Command 8ball: [{}] {}'.format(type(e).__name__, e))

  @commands.command(pass_context = True)
  async def choose(self, ctx, *args):
    """El bot elige por ti"""
    try:
      await self.bot.send_typing(ctx.message.channel)
      await self.bot.say(random.choice(list(args)))
    except Exception as e:
      print('Command choose: [{}] {}'.format(type(e).__name__, e))

  @commands.command(pass_context = True, aliases = ['perita'])
  async def like(self, ctx):
    """Reacciona con un like al último mensaje del canal"""
    try:
      msg = []
      async for x in self.bot.logs_from(ctx.message.channel, limit = 2):
        msg.append(x)

      await self.bot.delete_message(msg[0])
      await self.bot.add_reaction(msg[1], '👌')
    except Exception as e:
      print('Command like: [{}] {}'.format(type(e).__name__, e))

  @commands.command(pass_context = True)
  async def se(self, ctx, emoji:discord.Emoji):
    """Muestra la imagen original del emoji"""
    try:
      color = discord.Color.default()
      if ctx.message.server is not None:
        color = ctx.message.server.me.color
      embed = discord.Embed(title = emoji.name, color = color)
      embed.set_image(url = emoji.url)
      await self.bot.send_typing(ctx.message.channel)
      await self.bot.send_message(ctx.message.channel, embed = embed)
    except Exception as e:
      print('Command se: [{}] {}'.format(type(e).__name__, e))

def setup(bot):
  bot.add_cog(Fun(bot))
