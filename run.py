from discord.ext import commands
from utils.funcs import Funcs
import discord
import time
import asyncio
import datetime
import configparser
import os
import sys
import json

cogs = ['cogs.core', 'cogs.overwatch', 'cogs.fun', 'cogs.moderation', 'cogs.memes', 'cogs.music', 'cogs.osu']

class Bot():
  def __init__(self):
    self.config = ''

    def getConfig(dict, key):
      if os.path.exists(self.config + 'config.ini'):
        config = configparser.ConfigParser()
        config.read(self.config + 'config.ini')
        return config[dict][key]
      else:
        print('[ERROR] Cant read version file')
        sys.exit()

    def getVersion():
      if os.path.exists(self.config + 'version'):
        return Funcs().readFile(self.config + 'version').rstrip()
      else:
        print('[ERROR] Cant read version file')
        sys.exit()

    self.token = getConfig('PeritaBOT', 'token')
    self.osu_token = getConfig('Osu', 'osu')
    self.chrono_channel_id = getConfig('ChronoGG', 'channel')
    self.chrono_hour = int(getConfig('ChronoGG', 'hour'))
    self.root_role = getConfig('PeritaBOT', 'rootRole')
    self.prefix = getConfig('PeritaBOT', 'prefix')
    self.memes_path = getConfig('Memes', 'path')
    self.version = getVersion()
    self.bot = commands.Bot(command_prefix = self.prefix, description = 'PeritaBOT 2.0')
    self.start_time = time.time()

  def run(self):
    for cog in cogs:
      try:
        self.bot.load_extension(cog)
        print('[INFO] Loaded {}'.format(str(cog)))
      except Exception as e:
        print('{}: {}'.format(type(e).__name__, e))

    if not discord.opus.is_loaded():
      discord.opus.load_opus('opus')

    @self.bot.event
    async def on_ready():
      await self.bot.change_presence(status=discord.Status.online, game=discord.Game(name='!help • {} Guilds'.format(len(self.bot.servers))))
      print('[INFO] PeritaBOT Ready!')
      print('-----------------------------------')
      print('[INFO] discord.py version: {}'.format(discord.__version__))
      print('[INFO] Bot Username: {}'.format(self.bot.user.name))
      print('[INFO] Bot ID: {}'.format(self.bot.user.id))
      print('[INFO] PeritaBOT 2 Version: {}'.format(self.version))
      print('-----------------------------------')

    @self.bot.event
    async def on_message(message):
      if message.author == self.bot.user:
        return
      elif message.content.startswith('{}help'.format(self.prefix)):
        data = json.loads(Funcs().readFile(self.config + 'db/commands.json'))
        msg = '```'
        for item in range(len(data)):
          msg += '{}{} - {}\n'.format(self.prefix, data[item]['command'], data[item]['info'])
        msg += '```'
        await self.bot.send_message(message.author, msg)
        await self.bot.delete_message(message)
      else:
        try:
          if message.content == '':
            print('[{}] {} #> {}'.format(message.server.name, message.author, message.attachments[0]['url']))
          else:
            print('[{}] {} #> {}'.format(message.server.name, message.author, message.content))
        except Exception as e:
          print('{} - {}'.format(type(e).__name__, e))
          pass
        await self.bot.process_commands(message)

    @self.bot.event
    async def on_server_join(server):
      await self.bot.change_presence(game=discord.Game(name='!help • {} Guilds'.format(len(self.bot.servers))), status=discord.Status.online)

    @self.bot.event
    async def on_server_remove(server):
      await self.bot.change_presence(game=discord.Game(name='!help • {} Guilds'.format(len(self.bot.servers))), status=discord.Status.online)

    @self.bot.event
    async def on_command_error(error, ctx):
      if isinstance(error, commands.errors.CommandNotFound):
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.send_message(ctx.message.channel, 'El comando `{}` no existe!'.format(ctx.message.content.split(' ')[0]))
      elif isinstance(error, commands.errors.MissingRequiredArgument):
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.send_message(ctx.message.channel, 'El comando `{}` requiere argumentos'.format(ctx.message.content.split(' ')[0]))

    async def chrono_notifier(channel):
      await self.bot.wait_until_ready()
      done = 0
      while not self.bot.is_closed:
        try:
          now = datetime.datetime.now()
          if now.hour == self.chrono_hour and done == 0:
            e = discord.Embed(title='ChronoGG Time!', description="ChronoGG BOT Notificator", color=0x4C0B5F)
            e.set_thumbnail(url='https://chrono.gg/assets/images/favicon/favicon-196x196.4e111a55.png')
            e.add_field(name="Canjea las monedas de ChronoGG:", value='https://chrono.gg', inline=True)

            await self.bot.send_typing(discord.Object(id = channel))
            await self.bot.send_message(discord.Object(id = channel), '@everyone')
            await self.bot.send_message(discord.Object(id = channel), embed = e)
            done = 1
          if now.hour == self.chrono_hour + 1  and now.minute == 0 and done == 1:
            done = 0
          await asyncio.sleep(5)
        except CancelledError:
          pass
        except Exception as e:
          print('async chrono_notifier: [{}] {}'.format(type(e).__name__, e))

    self.bot.loop.create_task(chrono_notifier(self.chrono_channel_id))
    print('[INFO] chrono_notifier task created')
    self.bot.run(self.token)

if __name__ == '__main__':
  Bot().run()
