from discord.ext import commands
import discord
import time
import asyncio
import datetime
import configparser

cogs = ['cogs.core', 'cogs.overwatch', 'cogs.fun', 'cogs.moderation', 'cogs.memes', 'cogs.music', 'cogs.osu']

class Bot():
  def __init__(self):
    self.config = ''

    def getConfig(dict, key):
      config = configparser.ConfigParser()
      config.read(self.config + 'config.ini')
      return config[dict][key]

    self.token = getConfig('PeritaBOT', 'token')
    self.osu_token = getConfig('Osu', 'osu')
    self.chrono_channel_id = getConfig('ChronoGG', 'channel')
    self.chrono_hour = int(getConfig('ChronoGG', 'hour'))
    self.root_role = getConfig('PeritaBOT', 'rootRole')
    self.prefix = getConfig('PeritaBOT', 'prefix')
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
      print('[INFO] Bot ID: {}'.format(self.bot.user.id))

    @self.bot.event
    async def on_message(message):
      if message.author == self.bot.user:
        return
      elif message.content.startswith('{}help'.format(self.prefix)):
        help_cmd = ':gear: __**LISTA DE COMANDOS: **__\n'
        help_cmd += '```ini\n{}8ball [question] - La bola mágica responde a tu pregunta\n'.format(self.prefix)
        help_cmd += '{}memes help - Más información sobre el grupo de comandos\n'.format(self.prefix)
        help_cmd += '{}aww - Fotos de animalitos <3\n'.format(self.prefix)
        help_cmd += '{}avatar [usernames] - Obtiene la foto de perfil de los usuarios mencionado\n'.format(self.prefix)
        help_cmd += '{}ping - Muestra la latencia (ms) del bot\n'.format(self.prefix)
        help_cmd += '{}overwatch [username#id] - Información sobre el jugador en Overwatch\n'.format(self.prefix)
        help_cmd += '{}random [max_num] - Devuelve un numero aleatorio\n'.format(self.prefix)
        help_cmd += '{}space [num] [word] - Añade num espacios entre las letras de la palabra\n'.format(self.prefix)
        help_cmd += '{}reverse [text] - Da la vuelta al contenido del mensaje\n'.format(self.prefix)
        help_cmd += '{}react [text] - Reacciona al último mensaje del canal en forma de emojis\n'.format(self.prefix)
        help_cmd += '{}choose [options] - Elige una opcion entre todas\n'.format(self.prefix)
        help_cmd += '{}cat - Muestra una foto aleatoria de gatos\n'.format(self.prefix)
        help_cmd += '{}help - Muestra este mensaje\n'.format(self.prefix)
        help_cmd += '{}spamvoice - Spamea el canal de voz en el que estes\n'.format(self.prefix)
        help_cmd += '{}info - Muestra información sobre el servidor y el Bot```\n'.format(self.prefix)
        help_cmd += ':musical_note: __**COMANDOS MUSIC BOT: **__\n'.format(self.prefix)
        help_cmd += '```ini\n{}summon - Une al bot a tu canal de voz\n'.format(self.prefix)
        help_cmd += '{}join [channel] - Une al bot al canal de voz especificado\n'.format(self.prefix)
        help_cmd += '{}playing - Muestra la cancion que se esta reproduciendo\n'.format(self.prefix)
        help_cmd += '{}skip - Peticion para saltar la cancion actual\n'.format(self.prefix)
        help_cmd += '{}play [url] o [title] - Reproduce/agrega la cancion especificada\n'.format(self.prefix)
        help_cmd += '{}pause - Pausa la cancion actual\n'.format(self.prefix)
        help_cmd += '{}resume - Continua la cancion pausada\n'.format(self.prefix)
        help_cmd += '{}volume [0-100] - Establece el volumen para la cancion\n'.format(self.prefix)
        help_cmd += '{}stop - Kickea el bot del canal de voz```\n'.format(self.prefix)
        help_cmd += ':robot: __**COMANDOS ADMINISTRATIVOS: **__\n'.format(self.prefix)
        help_cmd += '```ini\n{}mute [username] - Mutea al usuario del canal de voz\n'.format(self.prefix)
        help_cmd += '{}unmute [username] - Desmutea al usuario del canal de voz\n'.format(self.prefix)
        help_cmd += '{}ban [username] - Banea al usuario del servidor\n'.format(self.prefix)
        help_cmd += '{}unban [name] - Desbanea al usuario del servidor (requiere invitación)\n'.format(self.prefix)
        help_cmd += '{}ban_list - Muestra la lista de usuarios baneados en el servidor\n'.format(self.prefix)
        help_cmd += '{}spam [msg] - Spammea un mensaje 10 veces por un canal de texto\n'.format(self.prefix)
        help_cmd += '{}prune [num] - Elimina num de mensajes (Max. 99)```'.format(self.prefix)
        await self.bot.send_message(message.author, help_cmd)
        await self.bot.delete_message(message)
      else:
        try:
          print('[{}] {} #> {}'.format(message.server.name, message.author, message.content))
        except Exception as e:
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
      now_done = 0
      while not self.bot.is_closed:
        try:
          now = datetime.datetime.now()
          if now.hour == self.chrono_hour and now_done == 0:
            e = discord.Embed(title='ChronoGG Time!', description="ChronoGG BOT Notificator", color=0x4C0B5F)
            e.set_thumbnail(url='https://chrono.gg/assets/images/favicon/favicon-196x196.4e111a55.png')
            e.add_field(name="Canjea las monedas de ChronoGG:", value='https://chrono.gg', inline=True)

            await self.bot.send_typing(discord.Object(id = channel))
            await self.bot.send_message(discord.Object(id = channel), '@everyone')
            await self.bot.send_message(discord.Object(id = channel), embed = e)
            now_done = 1
          if now.hour == self.chrono_hour + 1  and now.minute == 0 and now_done == 1:
            now_done = 0
          await asyncio.sleep(5)
        except Exception as e:
          print('async chrono_notifier: [{}] {}'.format(type(e).__name__, e))

    self.bot.loop.create_task(chrono_notifier(self.chrono_channel_id))
    print('[INFO] chrono_notifier task created')
    self.bot.run(self.token)

if __name__ == '__main__':
  Bot().run()
