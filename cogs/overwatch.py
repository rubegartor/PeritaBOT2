from discord.ext import commands
from run import Bot
import discord
import aiohttp
import json

class Overwatch:
  def __init__(self, bot):
    self.bot = bot
    self.Bot = Bot()

  @commands.command(pass_context = True, aliases = ['ow'])
  async def overwatch(self, ctx, battletag):
    """Muestra las estadisticas generales del jugador indicado"""
    try:
      battletag = battletag.replace('#', '-')
      async with aiohttp.get('https://owapi.net/api/v3/u/{}/stats'.format(battletag), headers={'User-Agent': 'Mozilla/5.0'}) as request_stats:
        stats = json.loads(await request_stats.text())
        comp_rank = stats['eu']['stats']['competitive']['overall_stats']['comprank']
        comp_win_rate = stats['eu']['stats']['competitive']['overall_stats']['win_rate']
        comp_games = int(stats['eu']['stats']['competitive']['game_stats']['games_played'])
        comp_wins = int(stats['eu']['stats']['competitive']['game_stats']['games_won'])
        comp_loses = comp_games - comp_wins
        ow_avatar = stats['eu']['stats']['competitive']['overall_stats']['avatar']
        quick_games = stats['eu']['stats']['quickplay']['game_stats']['games_won']
        rank_image = stats['eu']['stats']['competitive']['overall_stats']['tier_image']
        lvl_prestige = int(stats['eu']['stats']['competitive']['overall_stats']['prestige'])
        lvl = int(stats['eu']['stats']['competitive']['overall_stats']['level'])
        final_lvl = (lvl_prestige * 100) + lvl

        await self.bot.send_typing(ctx.message.channel)

        if comp_rank == None:
          comp_rank = 'No posicionado'
          comp_win_rate = 'No posicionado'

        e = discord.Embed(color=0xf1c40f)
        e.add_field(name = 'Rank', value = comp_rank)
        e.add_field(name = 'Win Rate', value = comp_win_rate)
        e.add_field(name = 'User Level', value = final_lvl)
        e.add_field(name = 'Ranked Games', value = comp_games)
        e.add_field(name = 'Ranked Wins', value = comp_wins)
        e.add_field(name = 'Ranked Loses', value = comp_loses)
        e.add_field(name = 'Quickplay Wins', value = int(quick_games))
        e.set_thumbnail(url = ow_avatar)
        if rank_image != None:
          e.set_author(name = battletag, icon_url = rank_image)

        await self.bot.send_typing(ctx.message.channel)
        await self.bot.send_message(ctx.message.channel, embed = e)
    except Exception as e:
      await self.bot.send_typing(ctx.message.channel)
      await self.bot.say('El usuario {} no existe o no se puede obtener la información en este momento'.format(battletag))

def setup(bot):
  bot.add_cog(Overwatch(bot))
