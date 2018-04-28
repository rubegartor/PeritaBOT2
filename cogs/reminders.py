from discord.ext import commands
from run import Bot
from utils import mysql
import discord
import datetime

class Reminders:
  def __init__(self, bot):
    self.bot = bot
    self.Bot = Bot()
    self.mySQL = mysql.Connect()

  @commands.group(pass_context = True, aliases = ['reminder'])
  async def reminders(self, ctx):
    """Reminders info"""
    if ctx.invoked_subcommand is None:
      await self.bot.say('Prueba con: `{}reminders help` para maś información'.format(self.Bot.prefix))

  @reminders.command(pass_context = True)
  async def help(self, ctx):
    """Muestra el mensaje de ayuda"""
    await self.bot.send_typing(ctx.message.channel)
    color = discord.Color.default()
    if ctx.message.server is not None:
      color = ctx.message.server.me.color
    e = discord.Embed(color = color)
    e.add_field(name = '{}reminders help'.format(self.Bot.prefix), value = 'Muestra el mensaje de ayuda para el comando {}reminders'.format(self.Bot.prefix))
    e.add_field(name = '{}reminders show'.format(self.Bot.prefix), value = 'Muestra todo tu calendario de recordatorios')
    e.add_field(name = '{}reminders remove [id]'.format(self.Bot.prefix), value = 'Elimina un recordatorio por su id')
    e.add_field(name = '{}reminders add'.format(self.Bot.prefix), value = 'Añade un nuevo recordarotio')
    e.set_thumbnail(url = 'https://i.imgur.com/e4AhEc2.png')
    await self.bot.send_message(ctx.message.channel, embed = e)

  @reminders.command(pass_context = True)
  async def add(self, ctx):
    """Añade un recordatorio a tu lista"""
    def validate(date):
      try:
        if len(date) == 10:
          datetime.datetime.strptime(date, '%d-%m-%Y')
          return True
        else:
          return False
      except ValueError:
        return False

    def previous(date):
      set = datetime.datetime.strptime(date, '%d-%m-%Y')
      today = datetime.datetime.strptime(datetime.datetime.now().strftime("%d-%m-%Y"), "%d-%m-%Y")
      if set >= today:
        return True
      else:
        return False

    try:
      if(ctx.message.server == None):
        passed = 1
        await self.bot.send_message(ctx.message.author, '➡ Titulo del recordatorio:')
        title = await self.bot.wait_for_message(author=ctx.message.author)
        while passed != 0:
          await self.bot.send_message(ctx.message.author, '➡ Fecha del recordatorio (d-m-Y) | Ejemplo: 01-03-2018')
          date = await self.bot.wait_for_message(author=ctx.message.author)
          if validate(date.content):
            if previous(date.content):
              break
            else:
              await self.bot.send_message(ctx.message.author, '🚫 La fecha tiene que ser posterior al día de hoy ({})'.format(datetime.datetime.now().strftime("%d-%m-%Y")))
          else:
            await self.bot.send_message(ctx.message.author, '🚫 Formato de fecha no valido, utiliza el siguiente formato: d-m-Y | Ejemplo: 01-03-2018')
        try:
          self.mySQL.insert('INSERT INTO reminders VALUES(NULL, "{}", "{}", "{}", "{}")'.format(str(ctx.message.author.id), str(ctx.message.author), str(title.content), str(date.content)))
          await self.bot.send_message(ctx.message.author, '✅ Recordatorio creado con éxito')
        except Exception as e:
          await self.bot.say('`No se ha podido guardar el recordatorio`')
      else:
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.say('Ejecuta el comando en un mensaje directo a PeritaBOT ;)')
        await self.bot.send_message(ctx.message.author, '😜 Hey! Estoy aquí!')
    except Exception as e:
      print('Command reminders add: {}'.format(e))

  @reminders.command(pass_context = True)
  async def show(self, ctx):
    """Muestra todos tus recordatorios"""
    try:
      if(ctx.message.server == None):
        msg = '**Formato:** ID | [FECHA] Contenido del recordatorio\n```'
        mySQL = mysql.Connect()
        data = mySQL.select('SELECT * FROM reminders WHERE user_id="{}"'.format(ctx.message.author.id))
        if data != []:
          for reminder in data:
            msg += '{} | [{}] {}\n'.format(reminder[0], reminder[4], reminder[3])
          msg += '```'
          await self.bot.send_message(ctx.message.author, msg)
        else:
          await self.bot.send_message(ctx.message.author, 'No se han encontrado recordatorios en tu colección')
      else:
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.say('Ejecuta el comando en un mensaje directo a PeritaBOT ;)')
        await self.bot.send_message(ctx.message.author, '😜 Hey! Estoy aquí!')
    except Exception as e:
      print('Command reminders show: {}'.format(e))

  @reminders.command(pass_context = True)
  async def remove(self, ctx, id):
    """Elimina un recordatorio """
    try:
      if(ctx.message.server == None):
        mySQL = mysql.Connect()
        data = mySQL.select('SELECT * FROM reminders WHERE id="{}"'.format(id))
        if data != []:
          if data[0][1] == str(ctx.message.author.id):
            mySQL.delete('DELETE FROM reminders WHERE id={}'.format(id))
            await self.bot.send_message(ctx.message.author, '✅ Recordatorio eliminado con éxito')
          else:
            await self.bot.send_message(ctx.message.author, '🚫 El id introducido no es correcto!')
        else:
          await self.bot.send_message(ctx.message.author, '🚫 El id introducido no es correcto!')
      else:
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.say('Ejecuta el comando en un mensaje directo a PeritaBOT ;)')
        await self.bot.send_message(ctx.message.author, '😜 Hey! Estoy aquí!')
    except Exception as e:
      print('Command reminders delete: {}'.format(e))

def setup(bot):
  bot.add_cog(Reminders(bot))
