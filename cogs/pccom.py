import discord
from discord.ext import commands
from bs4 import BeautifulSoup
from utils.settings import GlobalVars
import aiohttp
import logging
import time
import os

globalVars = GlobalVars()
logging.getLogger('discord').setLevel(logging.CRITICAL)
logging.basicConfig(filename=globalVars.path + 'peritabot.log', level=logging.INFO, filemode='a', format='[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s', datefmt='%d-%m-%Y:%H:%M:%S')

class PCCom():
  def __init__(self, bot):
    self.bot = bot

  def readLine(self, num):
    with open(globalVars.path + 'db/pccom.txt', 'r', encoding='utf-8') as _file:
      return _file.readlines()[num]

  def writeFile(self, filename, data):
    with open('upload/{}.txt'.format(filename), 'w', encoding='utf-8') as _file:
      _file.write(data)
      _file.close()

  def removeFile(self, filename):
    os.remove('upload/{}.txt'.format(filename))

  def getLines(self):
    return sum(1 for line in open(globalVars.path + 'db/pccom.txt'))

  async def generateListOfItem(self):
    try:
      finalList = []
      for i in range(self.getLines()):
        item = self.readLine(i).split('|')[0]
        finalList.append(item)

      return finalList
    except Exception as e:
      logging.error('[ERROR] {}: {}'.format(type(e).__name__, e))

  async def getURL(self, url):
    try:
      data = None
      async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
          print(resp.status)
          if resp.status == 206:
            data = await resp.text()

      return data
    except Exception as e:
      logging.error('[ERROR] {}: {}'.format(type(e).__name__, e))

  async def generatePage(self, page, filter, limit, order):
    """Genera una lista de productos segun los argumentos"""
    try:
      error = ''
      validFilter = False
      validLimit = False
      lines = self.getLines()
      counter = 0
      productList = []

      if filter != '':
        if filter.startswith('(') and filter.endswith(')'):
          validFilter = True
          filter_a = filter[1:-1]
          filter_b = filter_a.split(',')
          try:
            filter_min = float(filter_b[0])
            filter_max = float(filter_b[1])
          except ValueError:
            error = '[ERROR] El filtro solo puede contener valores numéricos'

      if limit != '':
        try:
          if limit.lower() != 'default':
            limit = int(limit)
          else:
            limit = 20 # Valor por defecto 20
          validLimit = True
        except ValueError:
          error = '[ERROR] El limite solo puede contener valores numéricos'

      for i in range(lines):
        item = self.readLine(i).split('|')
        if item[0].rstrip() == page:
          while True:
            url = item[1].rstrip().replace('*', str(counter))
            print('Obtaining page {} of {}'.format(counter, page))
            content = await self.getURL(url)
            if content != None:
              soup = BeautifulSoup(content, 'html.parser')
              a = soup.findAll('article')

              for tag in a:
                name = tag.get('data-name', None)
                price = tag.get('data-price', None)
                
                if validFilter:
                  if float(price) >= filter_min and float(price) <= filter_max:
                    productList.append({'name': name, 'price': price, 'type': page})
              counter += 1
            else:
              break

      if validLimit:
        if order.lower() == 'asc':
          productList = sorted(productList, key=lambda k: float(k['price'])) 
          productList = productList[:limit]
        elif order.lower() == 'desc':
          productList = sorted(productList, key=lambda k: float(k['price']), reverse = True)
          productList = productList[:limit]
        else:
          error = '[ERROR] El tipo de ordenación proporcionado no es válido (Usar: "ASC" / "DESC")'

      return (error, productList)
    except Exception as e:
      logging.error('[ERROR] {}: {}'.format(type(e).__name__, e))

  @commands.group()
  async def PCCom(self, ctx):
    pass

  @PCCom.command(name = 'help')
  async def ayuda(self, ctx):
    try:
      await ctx.send('Aquí tienes una lista con los comandos disponibles:\n```!PCCom show - Muestra más información sobre el subcomando\n!PCCom list - Muestra una lista de las paginas disponibles```')
    except Exception as e:
      logging.error('[ERROR] {}: {}'.format(type(e).__name__, e))

  @PCCom.command(name = 'list')
  async def lista(self, ctx):
    """Muestra la lista de páginas disponibles"""
    try:
      await ctx.send(', '.join(await self.generateListOfItem()))
    except Exception as e:
      logging.error('[ERROR] {}: {}'.format(type(e).__name__, e))

  @PCCom.command(name = 'show')
  async def show(self, ctx, page = '', filter = '', limit = '', order='desc'):
    """Muestra una lista de articulos filtrada"""
    try:
      if page != '':
        if page in await self.generateListOfItem():
          res = await self.generatePage(page, filter, limit, order)
          if res[0] != '':
            await ctx.send(res[0])
          else:
            result = ['{} - {}€'.format(el['name'], el['price']) for el in res[1]]
            data = '```{}```'.format('\n'.join(result))
            if len(data) > 2000:
              timestamp = time.time()
              self.writeFile(timestamp, '\n'.join(result))
              await ctx.send(':file_folder: No se ha podido mostrar el mensaje ya que excede los 2000 caracteres. Se ha creado el siguiente archivo con la información que has solicitado:')
              with open('upload/{}.txt'.format(timestamp), 'rb') as fp:
                await ctx.send(file=discord.File(fp, 'PCCom Data.txt'))
              self.removeFile(timestamp)
            else:
              await ctx.send(data)
        else:
          await ctx.send('No se encuentra la página: `{}`'.format('page'))
      else:
        await ctx.send('Necesitas especificar al menos una página.\n(**Uso:** `!PCCom show "pagina" (precioMin,precioMax) <limite> ASC/DESC`)\n**<pagina>** - Ayuda: `!PCCom list`\n**(precioMin,precioMax)** - Filtro de rango de precios\n**<limite>** - Limite de productos a mostrar (Por defecto: 20), Por defecto: sustituir por: "DEFAULT"\n**ASC/DESC** - ASC: Ordenación ascendente (__menor a mayor__), DESC: Ordenación descendente (__mayor a menor__)\n**Ejemplo:** `!PCCom show "Procesadores" (0,255.60) DEFAULT ASC`')
    except Exception as e:
      logging.error('[ERROR] {}: {}'.format(type(e).__name__, e))

def setup(bot):
  bot.add_cog(PCCom(bot))

