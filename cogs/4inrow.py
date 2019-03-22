import discord
from discord.ext import commands
from utils.settings import GlobalVars
from itertools import groupby, chain
import logging
import random

globalVars = GlobalVars()
logging.getLogger('discord').setLevel(logging.CRITICAL)
logging.basicConfig(filename=globalVars.path + 'peritabot.log', level=logging.INFO, filemode='a', format='[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s', datefmt='%d-%m-%Y:%H:%M:%S')

white = '⚪'
black = '⚫'
red = '🔴'

class FourInRow(commands.Cog):
  def __init__(self, bot, cols = 7, rows = 6, requiredToWin = 4):
    self.bot = bot
    self.cols = cols
    self.rows = rows
    self.win = requiredToWin

  def diagonalsPos (self, matrix, cols, rows):
    """Check bottom-left to top-right"""
    for di in ([(j, i - j) for j in range(cols)] for i in range(cols + rows -1)):
      yield [matrix[i][j] for i, j in di if i >= 0 and j >= 0 and i < cols and j < rows]

  def diagonalsNeg (self, matrix, cols, rows):
    """Check top-left to bottom-right"""
    for di in ([(j, i - cols + j + 1) for j in range(cols)] for i in range(cols + rows - 1)):
      yield [matrix[i][j] for i, j in di if i >= 0 and j >= 0 and i < cols and j < rows]

  async def createChannel(self, ctx, name):
    """Crea un canal customizado para la partida, puede ser publica o privada"""
    try:
      if '4InRow' not in [c.name for c in ctx.guild.categories]:
        await ctx.guild.create_category('4InRow')

      overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=True)
      }

      category = next((c for c in ctx.guild.categories if c.name == '4InRow'), None)

      channel = await ctx.guild.create_text_channel(name, overwrites=overwrites, category=category)

      return channel
    except Exception as e:
      logging.error('[ERROR] {}: {}'.format(type(e).__name__, e))

  async def printBoard(self, board):
    """Mostrar el tablero del juego"""
    message = ''
    for y in range(self.rows):
      message += ' '.join(str(board[x][y]) for x in range(self.cols))
      message += '\n'
    return message

  async def randomizePlayer(self, players):
    """Devuelve un jugador de la lista: players"""
    return random.choice(players)

  async def put(self, board, column, color):
    """Place circle on the board"""
    c = board[column]
    if c[0] != white:
      await self.bot.say('La columna {} está llena, has perdido tu turno'.format(str(column + 1)))

    i = -1
    while c[i] != white:
      i -= 1
    c[i] = color

  async def checkComplete(self, board):
    """Check if board is complete"""
    columns = [board[c][0] for c in range(self.cols)]
    if not white in columns:
      return True

  async def checkWin(self, board):
    """Check Win movement"""
    w = await self.getWinner(board)
    if w: return w

  async def getWinner(self, board):
    """Get winner player"""
    lines = (
      board, # columns
      zip(*board), # rows
      self.diagonalsPos(board, self.cols, self.rows), # positive diagonals
      self.diagonalsNeg(board, self.cols, self.rows) # negative diagonals
    )

    for line in chain(*lines):
      for color, group in groupby(line):
        if color != white and len(list(group)) >= self.win:
          return color

  @commands.command()
  async def game(self, ctx, opponent:discord.Member):
    """Comando principal para empezar el juego con otra persona"""
    try:
      board = [[white] * self.rows for _ in range(self.cols)]
      playerMessage = None
      playerTurn = None
      mainMessage = None
      players = None
      reaction_dic = {'1⃣':1, '2⃣':2, '3⃣':3, '4⃣':4, '5⃣':5, '6⃣':6, '7⃣':7}
      sorted_react_dic = sorted(reaction_dic.keys())
      gameName = '{}-{}'.format(ctx.message.author, '{}#{}'.format(opponent.name, opponent.discriminator))
      channel = await self.createChannel(ctx, 'game_{}'.format(gameName))

      if playerMessage == None:
        playerTurn = await self.randomizePlayer([ctx.message.author, opponent])

        if playerTurn.id == opponent.id:
          secondPlayer = ctx.message.author
        else:
          secondPlayer = opponent

        players = {'{}#{}'.format(playerTurn.name, playerTurn.discriminator): {'obj': playerTurn, 'color': ''}, '{}#{}'.format(secondPlayer.name, secondPlayer.discriminator): {'obj': secondPlayer, 'color': ''}}

        chooseMessage = await channel.send('<@{}> Empiezas tu, elige el color de tu ficha:'.format(playerTurn.id))
        for reaction in [red, black]:
          await chooseMessage.add_reaction(reaction)

        while True:
          def checkColor(reaction, user):
            if user != self.bot.user and reaction.message.id == chooseMessage.id:
              return user and str(reaction.emoji) in [red, black]

          reaction, user = await self.bot.wait_for('reaction_add', check = checkColor)

          if user.id != playerTurn.id:
            await chooseMessage.remove_reaction(reaction.emoji, user)
          else:
            if reaction.emoji == red:
              players['{}#{}'.format(playerTurn.name, playerTurn.discriminator)]['color'] = red
              players['{}#{}'.format(secondPlayer.name, secondPlayer.discriminator)]['color'] = black
              break
            elif reaction.emoji == black:
              players['{}#{}'.format(playerTurn.name, playerTurn.discriminator)]['color'] = black
              players['{}#{}'.format(secondPlayer.name, secondPlayer.discriminator)]['color'] = red
              break


        await chooseMessage.delete()
        playerMessage = await channel.send('\n**Turno del jugador ({}) [__{}__]**\n'.format(players['{}#{}'.format(playerTurn.name, playerTurn.discriminator)]['color'], playerTurn))

      if mainMessage == None:
        mainMessage = await channel.send(await self.printBoard(board))
        for reaction in sorted_react_dic:
          await mainMessage.add_reaction(reaction)
      else:
        await mainMessage.edit(content = await self.printBoard(board))

      while True:
        def checkPos(reaction, user):
          if user != self.bot.user and reaction.message.id == mainMessage.id:
            return user and str(reaction.emoji) in sorted_react_dic

        reaction, user = await self.bot.wait_for('reaction_add', check = checkPos)

        if user == playerTurn:
          playerColor = players['{}#{}'.format(playerTurn.name, playerTurn.discriminator)]['color']

          await self.put(board, reaction_dic[reaction.emoji] - 1, playerColor)

          await mainMessage.remove_reaction(reaction.emoji, playerTurn)

          completeBoard = await self.checkComplete(board)

          if not completeBoard:
            winner = await self.checkWin(board)
            await mainMessage.edit(content = await self.printBoard(board))
            if not winner:
              if playerTurn.id == opponent.id:
                playerTurn = ctx.message.author
              else:
                playerTurn = opponent

              await playerMessage.edit(content = '\n**Turno del jugador ({}) [__{}__]**\n'.format(players['{}#{}'.format(playerTurn.name, playerTurn.discriminator)]['color'], playerTurn))
            else:
              await channel.send(':drum: :drum: **EL GANADOR ES: <@{}> ({})**'.format(playerTurn.id, players['{}#{}'.format(playerTurn.name, playerTurn.discriminator)]['color']))
              await mainMessage.clear_reactions()
              break
          else:
            await channel.send('<@{}>, <@{}> El juego ha terminado en empate!'.format(players[ctx.message.author]['obj'].id, players['{}#{}'.format(opponent.name, opponent.discriminator)]['obj'].id)) #TERMINAR
            await mainMessage.clear_reactions()
            break
        else:
          await mainMessage.remove_reaction(reaction.emoji, user)

    except Exception as e:
      logging.error('[ERROR] {}: {}'.format(type(e).__name__, e))

def setup(bot):
  bot.add_cog(FourInRow(bot))