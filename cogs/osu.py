import discord
from discord.ext import commands
from utils.settings import GlobalVars
import aiohttp
import json
import logging

globalVars = GlobalVars()
logging.getLogger('discord').setLevel(logging.CRITICAL)
logging.basicConfig(filename=globalVars.path + 'peritabot.log', level=logging.INFO, filemode='a', format='[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s', datefmt='%d-%m-%Y:%H:%M:%S')

class Osu(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  async def getUserInfo(self, username):
    try:
      async with aiohttp.ClientSession() as session:
        async with session.get('https://osu.ppy.sh/api/get_user?k={}&u={}'.format(globalVars.osu_token, username), headers={'User-Agent': 'Mozilla/5.0'}) as request_stats:
          stats = json.loads(await request_stats.text())
          e = discord.Embed(color = 0xFF92A4)
          e.set_thumbnail(url = 'http://up.ppy.sh/files/osu!logo4-0.png')
          e.add_field(name = 'Performance Points :parking:', value = stats[0]['pp_raw'], inline = True)
          e.add_field(name = 'Nivel :arrow_up:', value = round(float(stats[0]['level']), 2), inline = True)
          e.add_field(name = 'Accuracy :dart:', value = round(float(stats[0]['accuracy']), 3), inline = True)
          e.add_field(name = 'Ranking Global :earth_africa:', value = stats[0]['pp_rank'], inline = True)
          e.add_field(name = 'Ranking Local :first_place:', value = stats[0]['pp_country_rank'], inline = True)
          e.add_field(name = 'Horas jugadas :calendar:', value = round(int(stats[0]['total_seconds_played']) / 3600), inline = True)
          e.set_author(name = '{}'.format(username), icon_url = 'http://up.ppy.sh/files/osu!logo4-0.png', url = 'https://osu.ppy.sh/u/{}'.format(username))

      return e
    except Exception as e:
      logging.error('[ERROR] {}: {}'.format(type(e).__name__, e))

  @commands.command()
  async def osu(self, ctx, username):
    """Grupo de comandos para el comando osu, muestra información general sobre el usuario especificado"""
    try:
      e = await self.getUserInfo(username)
      await ctx.send(embed = e)
    except Exception as e:
      logging.error('[ERROR] {}: {}'.format(type(e).__name__, e))

def setup(bot):
  bot.add_cog(Osu(bot))