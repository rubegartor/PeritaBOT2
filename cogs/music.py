from discord.ext import commands
from run import Bot
import discord
import asyncio

class VoiceEntry:
  def __init__(self, message, player):
    self.requester = message.author
    self.channel = message.channel
    self.player = player

  def __str__(self):
    fmt = '{0.title}'
    duration = self.player.duration
    return fmt.format(self.player)

class VoiceState:
  def __init__(self, bot):
    self.current = None
    self.voice = None
    self.bot = bot
    self.play_next_song = asyncio.Event()
    self.songs = asyncio.Queue()
    self.skip_votes = set()
    self.audio_player = self.bot.loop.create_task(self.audio_player_task())

  def is_playing(self):
    if self.voice is None or self.current is None:
      return False

    player = self.current.player
    return not player.is_done()

  @property
  def player(self):
    return self.current.player

  def skip(self):
    self.skip_votes.clear()
    if self.is_playing():
      self.player.stop()

  def toggle_next(self):
    self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

  async def audio_player_task(self):
    while True:
      self.play_next_song.clear()
      self.current = await self.songs.get()
      await self.bot.send_message(self.current.channel, '```Reproduciendo: {}```'.format(str(self.current)))
      self.current.player.start()
      await self.play_next_song.wait()

class Music:
  def __init__(self, bot):
    self.bot = bot
    self.voice_states = {}

  def get_voice_state(self, server):
    state = self.voice_states.get(server.id)
    if state is None:
      state = VoiceState(self.bot)
      self.voice_states[server.id] = state

    return state

  async def create_voice_client(self, channel):
    voice = await self.bot.join_voice_channel(channel)
    state = self.get_voice_state(channel.server)
    state.voice = voice

  def __unload(self):
    for state in self.voice_states.values():
      try:
        state.audio_player.cancel()
        if state.voice:
          self.bot.loop.create_task(state.voice.disconnect())
      except:
        pass

  @commands.command(pass_context=True, no_pm=True)
  async def join(self, ctx, *, channel : discord.Channel):
    try:
      await self.create_voice_client(channel)
    except discord.ClientException:
      await self.bot.say('```Ya estoy en un canal de voz...```')
    except discord.InvalidArgument:
      await self.bot.say('```Esto no es un canal de voz...```')

  @commands.command(pass_context=True, no_pm=True)
  async def summon(self, ctx):
    try:
      summoned_channel = ctx.message.author.voice_channel
      if summoned_channel is None:
        await self.bot.say('```diff\n- Necesitas estar en un canal de voz```')
        return False

      state = self.get_voice_state(ctx.message.server)
      if state.voice is None:
        state.voice = await self.bot.join_voice_channel(summoned_channel)
      else:
        await state.voice.move_to(summoned_channel)

      return True
    except Exception as e:
      print(e)

  @commands.command(pass_context=True, no_pm=True)
  async def play(self, ctx, *, song : str):
    state = self.get_voice_state(ctx.message.server)
    opts = {
      'default_search': 'auto',
      'quiet': True,
    }

    if state.voice is None:
      success = await ctx.invoke(self.summon)
      if not success:
        return

    try:
      player = await state.voice.create_ytdl_player(song, ytdl_options=opts, after=state.toggle_next)
    except Exception as e:
      fmt = 'Se ha producido un error procesando la petición: ```py\n{}: {}\n```'
      await self.bot.send_message(ctx.message.channel, fmt.format(type(e).__name__, e))
    else:
      player.volume = 0.1
      entry = VoiceEntry(ctx.message, player)
      await self.bot.say('```Añadido: {}```'.format(str(entry)))
      await state.songs.put(entry)

  @commands.command(pass_context=True, no_pm=True)
  async def volume(self, ctx, value : int):

    state = self.get_voice_state(ctx.message.server)
    if state.is_playing():
      player = state.player
      player.volume = value / 100
      await self.bot.say("```py\nVolumen: '{:.0%}'```".format(player.volume))

  @commands.command(pass_context=True, no_pm=True)
  async def pause(self, ctx):
    state = self.get_voice_state(ctx.message.server)
    if state.is_playing():
      player = state.player
      player.pause()

  @commands.command(pass_context=True, no_pm=True)
  async def resume(self, ctx):
    state = self.get_voice_state(ctx.message.server)
    if state.is_playing():
      player = state.player
      player.resume()

  @commands.command(pass_context=True, no_pm=True)
  async def stop(self, ctx):
    server = ctx.message.server
    state = self.get_voice_state(server)

    if state.is_playing():
      player = state.player
      player.stop()

    try:
      state.audio_player.cancel()
      del self.voice_states[server.id]
      await state.voice.disconnect()
    except:
      pass

  @commands.command(pass_context=True, no_pm=True)
  async def skip(self, ctx):
    state = self.get_voice_state(ctx.message.server)
    if not state.is_playing():
      await self.bot.say('```No se esta reproduciendo nada en este momento...```')
      return

    voter = ctx.message.author
    if voter == state.current.requester:
      await self.bot.say('```Skipeando canción...```')
      state.skip()
    elif voter.id not in state.skip_votes:
      state.skip_votes.add(voter.id)
      total_votes = len(state.skip_votes)
      if total_votes >= 3:
        await self.bot.say('```Votación aceptada, skipeando canción...```')
        state.skip()
      else:
        await self.bot.say('Votación añadida [{}/3]'.format(total_votes))
    else:
      await self.bot.say('```Ya has votado para skipear la canción.```')

  @commands.command(pass_context=True, no_pm=True)
  async def playing(self, ctx):
    try:
      state = self.get_voice_state(ctx.message.server)
      if state.current is None:
        await self.bot.say('```No se esta reproduciendo nada.```')
      else:
        skip_count = len(state.skip_votes)
        e = discord.Embed(color = 0xf1c40f, title = str(state.current))
        e.set_thumbnail(url = 'https://i.imgur.com/OV2t4PC.png')
        e.add_field(name = 'Votación para pasar de canción', value = 'Skips: [{}/3]'.format(str(skip_count)))
        await self.bot.send_message(ctx.message.channel, embed = e)
    except Exception as e:
      print(e)

def setup(bot):
  bot.add_cog(Music(bot))
