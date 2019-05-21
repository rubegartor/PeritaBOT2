import discord
from discord.ext import commands
from utils.settings import GlobalVars, Funcs
import os
import sys
import json
import logging

globalVars = GlobalVars()
logging.getLogger('discord').setLevel(logging.CRITICAL)
logging.basicConfig(filename=globalVars.path + 'peritabot.log', level=logging.INFO, filemode='a', format='[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s', datefmt='%d-%m-%Y:%H:%M:%S')

class PeritaBOT(commands.Bot):
  def __init__(self):
    self.prefix = globalVars.prefix
    super().__init__(command_prefix=self.prefix)
    self.remove_command('help')

    for cog in globalVars.cogs:
      self.load_extension(cog)
      print('[INFO] {} loaded'.format(cog))

  async def on_ready(self):
    print('[INFO] PeritaBOT loaded')

  async def on_message(self, message):
    if message.author == self.user:
      return
    elif message.content.startswith('{}help'.format(self.prefix)):
      data = json.loads(Funcs().readFile(GlobalVars().path + 'db/commands.json'))
      msg = '```'
      for item in range(len(data)):
        msg += '{}{} - {}\n'.format(self.prefix, data[item]['command'], data[item]['info'])
      msg += '```'
      await message.channel.send(msg)
    else:
      await self.process_commands(message)

  async def on_command_error(self, ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
      await ctx.send('El comando `{}` no existe!'.format(ctx.message.content.split()[0]))
    elif isinstance(error, commands.errors.MissingRequiredArgument):
      await ctx.send('El comando `{}` requiere argumentos'.format(ctx.message.content.split()[0]))

bot = PeritaBOT()
bot.run(globalVars.token)