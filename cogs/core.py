from discord.ext import commands
from utils import funcs
from run import Bot
import discord
import random
import time
import datetime
import json
import aiohttp
import calendar

class Core:
  def __init__(self, bot):
    self.bot = bot
    self.Bot = Bot()

  @commands.command(pass_context = True)
  async def ping(self, ctx):
    """Devuelve el ping (ms) del bot"""
    try:
      t1 = time.perf_counter()
      await self.bot.send_typing(ctx.message.channel)
      t2 = time.perf_counter()
      await self.bot.say(':ping_pong: Pong! **{}ms**'.format(round((t2-t1)*1000)))
    except Exception as e:
      print('Command ping: [{}] {}'.format(type(e).__name__, e))

  @commands.command(pass_context = True)
  async def info(self, ctx):
    """Muestra información sobre el bot"""
    try:
      elapsed_time = time.gmtime(time.time() - self.Bot.start_time)
      formated_time = str(elapsed_time[7] - 1) + " día(s), " + str(elapsed_time[3]) + " hrs, " + str(elapsed_time[4]) + " min"
      active_guilds = len(self.bot.servers)
      total_users = sum(1 for i in self.bot.get_all_members())
      discord_version = discord.__version__
      bot_name = self.bot.user.name
      owner = ctx.message.server.owner
      server_icon_url = ctx.message.server.icon_url
      date_server = ctx.message.server.created_at
      date_server = '{}-{}-{} {}:{}'.format(date_server.day, date_server.month, date_server.year, date_server.hour, date_server.minute)
      region_server = ctx.message.server.region

      color = discord.Color.default()
      if ctx.message.server.me.color:
        color = ctx.message.server.me.color

      e = discord.Embed(color = color, title = 'PeritaBOT 2 Estadísticas', description = 'Made by **@rubegator** - https://github.com/rubegartor/PeritaBOT2')
      e.add_field(name = '> Tiempo activo', value = formated_time)
      e.add_field(name = '> Guilds activas', value = active_guilds)
      e.add_field(name = '> Número de usuarios', value = total_users)
      e.add_field(name = '> Versión discord', value = discord_version)
      e.add_field(name = '> Nombre del bot', value = bot_name)
      e.add_field(name = '> Creación del Servidor', value = date_server)
      e.add_field(name = '> Región del Servidor', value = region_server)
      e.add_field(name = '> Propietario del Servidor', value = owner)
      e.set_thumbnail(url = server_icon_url)
      await self.bot.send_typing(ctx.message.channel)
      await self.bot.say(embed = e)
    except Exception as e:
      print('Command info: [{}] {}'.format(type(e).__name__, e))

  @commands.command(pass_context = True)
  async def react(self, ctx, *args):
    """Reacciona con emojis al último mensaje con el texto que se proporcione"""
    try:
      allowed = 'abcdefghijklmnopqrstuvwxyz'
      data = json.loads(funcs.readFile(self.Bot.config + 'db/emojis.json'))
      args = ''.join(args).lower()
      msg = []
      async for x in self.bot.logs_from(ctx.message.channel, limit = 2):
        msg.append(x)

      await self.bot.delete_message(msg[0])

      for a in args:
        if a not in allowed:
          args = args.replace(a, '')

      for i in args:
        await self.bot.add_reaction(msg[1], data[0][i])

    except Exception as e:
      print('Command react: [{}] {}'.format(type(e).__name__, e))

  @commands.command(pass_context = True)
  async def avatar(self, ctx):
    """Muestra el avatar de los usuarios mencionados"""
    try:
      for user in ctx.message.mentions:
        if user.avatar_url != "":
          embed = discord.Embed(title = '@{} avatar'.format(user.name), color = user.color)
          embed.set_image(url = user.avatar_url)
          await self.bot.send_typing(ctx.message.channel)
          await self.bot.send_message(ctx.message.channel, embed = embed)
        else:
          await self.bot.send_typing(ctx.message.channel)
          await self.bot.say(':exclamation: El usuario {} no tiene avatar'.format(user.name))
    except Exception as e:
      print('Command avatar: [{}] {}'.format(type(e).__name__, e))

  @commands.command(pass_context = True, aliases = ['rnd'])
  async def random(self, ctx, number : int):
    """Muestra un numero random"""
    try:
      await self.bot.send_typing(ctx.message.channel)
      await self.bot.say('Tu numero es: `{}`'.format(random.randint(0, number)))
    except Exception as e:
      print('Command random: [{}] {}'.format(type(e).__name__, e))

  @commands.command(pass_context = True)
  async def space(self, ctx, num, word):
    """Añade num espacios entre las letras del texto"""
    try:
      if num.isdigit():
        if int(num) >= 1 and int(num) <= 20:
          spaces = ' ' * int(num)
          await self.bot.send_typing(ctx.message.channel)
          await self.bot.say(spaces.join(list(word)))
        else:
          await self.bot.send_typing(ctx.message.channel)
          await self.bot.say('El número de espacios debe ser un número del 1 al 20')
      else:
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.say('El primer argumento debe ser un número del 1 al 20')
    except Exception as e:
      print('Command space: [{}] {}'.format(type(e).__name__, e))

  @commands.command(pass_context = True)
  async def reverse(self, ctx):
    """Da la vuelta al contenido del mensaje"""
    try:
      if len(ctx.message.mentions) == 0 and len(ctx.message.channel_mentions) == 0 and len(ctx.message.role_mentions) == 0:
        end = ''
        string = ' '.join(ctx.message.content.split()[1:])
        if string != '':
          for i in range(len(string), 0, -1):
            end += string[i - 1]
          await self.bot.send_typing(ctx.message.channel)
          await self.bot.say(end)
        else:
          await self.bot.send_typing(ctx.message.channel)
          await self.bot.say('Necesitas especificar un mensaje para utilizar el comando')
      else:
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.say('```No puedes hacer eso con el comando {}reverse```'.format(self.Bot.prefix))
    except Exception as e:
      print('Command reverse: [{}] {}'.format(type(e).__name__, e))

  @commands.command(pass_context = True)
  async def invite(self, ctx):
    """Muestra el enlace para invitar a PeritaBOT 2 a tu servidor"""
    try:
      await self.bot.send_typing(ctx.message.channel)
      await self.bot.say('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot'.format(self.bot.user.id))
    except Exception as e:
      print('Command invite: [{}] {}'.format(type(e).__name__, e))

  @commands.command(pass_context = True, aliases = ['update'])
  async def updates(self, ctx):
    """Muestra si hay actualizaciones disponibles"""
    try:
      async with aiohttp.get('https://raw.githubusercontent.com/rubegartor/PeritaBOT2/master/version', headers={'User-Agent': 'Mozilla/5.0'}) as r:
        if r.status == 200:
          response = await r.text()
          git_version = response.replace('.', '')

          read = funcs.readFile(self.Bot.config + 'version').rstrip()
          local_version = read.replace('.', '')

          if int(git_version) > int(local_version):
            await self.bot.send_typing(ctx.message.channel)
            await self.bot.say('```diff\n+ Hay nuevas actualizaciones para PeritaBOT 2```')
          else:
            await self.bot.send_typing(ctx.message.channel)
            await self.bot.say('```No hay actualizaciones disponibles para PeritaBOT 2```')
    except Exception as e:
      print('Command updates: [{}] {}'.format(type(e).__name__, e))

  @commands.command(pass_context = True)
  async def calendar(self, ctx):
    """Muestra el calendatio del mes actual"""
    try:
      now = datetime.datetime.now()
      await self.bot.send_typing(ctx.message.channel)
      await self.bot.say('`{}`'.format(calendar.month(now.year, now.month)))
    except Exception as e:
      print('Command calendar: [{}] {}'.format(type(e).__name__, e))

  @commands.command(pass_context = True)
  async def github(self, ctx):
    """Muestra el repositorio en GitHub de PeritaBOT 2"""
    try:
      await self.bot.send_typing(ctx.message.channel)
      await self.bot.say('https://github.com/rubegartor/PeritaBOT2')
    except Exception as e:
      print('Command github: [{}] {}'.format(type(e).__name__, e))


def setup(bot):
  bot.add_cog(Core(bot))
