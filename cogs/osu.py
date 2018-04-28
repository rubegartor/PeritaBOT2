from discord.ext import commands
from run import Bot
import discord
import aiohttp
import json

class Osu:
  def __init__(self, bot):
    self.bot = bot
    self.Bot = Bot()

  @commands.command(pass_context = True)
  async def osu(self, ctx, username):
    """Estadísticas generales del usuario en osu!"""
    try:
      async with aiohttp.get('https://osu.ppy.sh/api/get_user?k={}&u={}'.format(self.Bot.osu_token, username), headers={'User-Agent': 'Mozilla/5.0'}) as request_stats:
        stats = json.loads(await request_stats.text())
        e = discord.Embed(color = 0xFF92A4)
        e.set_thumbnail(url = 'http://up.ppy.sh/files/osu!logo4-0.png')
        e.add_field(name = 'Performance Points 🅿', value = stats[0]['pp_raw'], inline = True)
        e.add_field(name = 'Nivel ⬆', value = round(float(stats[0]['level']), 2), inline = True)
        e.add_field(name = 'Accuracy 🎯', value = round(float(stats[0]['accuracy']), 3), inline = True)
        e.add_field(name = 'Ranking Global 🌍', value = stats[0]['pp_rank'], inline = True)
        e.add_field(name = 'Ranking Local 🥇', value = stats[0]['pp_country_rank'], inline = True)
        e.set_author(name = '{}'.format(username), icon_url = 'http://up.ppy.sh/files/osu!logo4-0.png', url = 'https://osu.ppy.sh/u/{}'.format(username))

        await self.bot.send_message(ctx.message.channel, embed = e)
    except Exception as e:
      await self.bot.send_typing(ctx.message.channel)
      await self.bot.say('No he podido encontrar al usuario `{}`'.format(username))

def setup(bot):
  bot.add_cog(Osu(bot))
