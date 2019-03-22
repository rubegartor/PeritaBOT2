import discord
from discord.ext import commands
from utils.settings import GlobalVars
import logging

globalVars = GlobalVars()
logging.getLogger('discord').setLevel(logging.CRITICAL)
logging.basicConfig(filename=globalVars.path + 'peritabot.log', level=logging.INFO, filemode='a', format='[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s', datefmt='%d-%m-%Y:%H:%M:%S')

class Mod(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @commands.command()
  @commands.has_role(globalVars.root_role)
  async def prune(self, ctx, num):
    """Elimina una lista de mensajes"""
    try:
      if int(num) <= 99 and int(num) != 0:
        messages = await ctx.channel.history(limit=int(num) + 1).flatten()

        await ctx.channel.delete_messages(messages)
      else:
        await ctx.send('El rango de mensajes es de: `1 - 99`')
    except discord.Forbidden:
      await ctx.send('El bot no tiene los permisos necesarios para eliminar mensajes')
    except discord.HTTPException:
      await ctx.send('No se pueden eliminar los mensajes con más de 14 días de antigüedad')
    except ValueError:
      await ctx.send('El argumento para el comando `prune` no es válido')
    except Exception as e:
      logging.error('[ERROR] {}: {}'.format(type(e).__name__, e))

  @commands.command()
  @commands.has_role(globalVars.root_role)
  async def mute(self, ctx, member : discord.Member):
    """Mutea/Desmutea el usuario especificado"""
    try:
      if member.voice != None:
        if member.voice.mute:
          await member.edit(mute = False)
        else:
          await member.edit(mute = True)
      else:
        await ctx.send(':exclamation: El usuario: `{}` no se encuentra en ningún canal de voz'.format(member))
    except Exception as e:
      logging.error('[ERROR] {}: {}'.format(type(e).__name__, e))

  @commands.command()
  @commands.has_role(globalVars.root_role)
  async def deaf(self, ctx, member : discord.Member):
    try:
      if member.voice != None:
        if member.voice.deaf:
          await member.edit(deaf = False)
        else:
          await member.edit(deaf = True)
      else:
        await ctx.send(':exclamation: El usuario: `{}` no se encuentra en ningún canal de voz'.format(member))
    except Exception as e:
      logging.error('[ERROR] {}: {}'.format(type(e).__name__, e))

def setup(bot):
  bot.add_cog(Mod(bot))