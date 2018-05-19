from discord.ext import commands
from itertools import groupby, chain
import discord
import random

white = '⚪'
black = '⚫'
red = '🔴'

def diagonalsPos (matrix, cols, rows):
  """Check bottom-left to top-right"""
  for di in ([(j, i - j) for j in range(cols)] for i in range(cols + rows -1)):
    yield [matrix[i][j] for i, j in di if i >= 0 and j >= 0 and i < cols and j < rows]

def diagonalsNeg (matrix, cols, rows):
  """Check top-left to bottom-right"""
  for di in ([(j, i - cols + j + 1) for j in range(cols)] for i in range(cols + rows - 1)):
    yield [matrix[i][j] for i, j in di if i >= 0 and j >= 0 and i < cols and j < rows]

class Game:
  def __init__(self, bot, cols = 7, rows = 6, requiredToWin = 4):
    self.bot = bot
    self.cols = cols
    self.rows = rows
    self.win = requiredToWin
    self.is_started = False
    self.endgame = False
    self.board = [[white] * rows for _ in range(cols)]

  @commands.command(pass_context = True)
  async def game(self, ctx, user : discord.User):
    """Start game command"""
    try:
      if self.is_started == False:
        self.is_started = True
        self.endgame = False
        self.board = [[white] * self.rows for _ in range(self.cols)]
        turn = red
        reduser = ctx.message.author
        blackuser = user
        player = None
        message = None
        player_msg = None
        reaction_dic = {'1⃣':1, '2⃣':2, '3⃣':3, '4⃣':4, '5⃣':5, '6⃣':6, '7⃣':7}

        while self.endgame != True:
          if player_msg == None:
            player_msg = await self.bot.say('\n**Turno del jugador ({}) [__{}__]**\n'.format(red, reduser))

          if turn == red:
            color = red
            await self.bot.edit_message(player_msg, '\n**Turno del jugador ({}) [__{}__]**\n'.format(red, reduser))
            player = reduser
          else:
            color = black
            await self.bot.edit_message(player_msg, '\n**Turno del jugador ({}) [__{}__]**\n'.format(black, blackuser))
            player = blackuser

          if message == None:
            message = await self.bot.say(await self.printBoard())
            sorted_react_dic = sorted(reaction_dic.keys())
            for reaction in sorted_react_dic:
              await self.bot.add_reaction(message, reaction)
          else:
            await self.bot.edit_message(message, await self.printBoard())
          while True:
            res = await self.bot.wait_for_reaction(sorted_react_dic, message=message)
            if res.user != self.bot.user:
              if res.user == player:
                await self.put(reaction_dic[res.reaction.emoji] - 1, color)
                await self.bot.remove_reaction(message, res.reaction.emoji, res.user)
                break
              else:
                await self.bot.remove_reaction(message, res.reaction.emoji, res.user)
          turn = black if turn == red else red
        await self.bot.edit_message(message, await self.printBoard()) #printBoard when the player wins (self.endgame = True)
      else:
        await self.bot.say('Ya hay una partida en curso!')
    except Exception as e:
      print('Command game: [{}] {}'.format(type(e).__name__, e))

  async def put(self, column, color):
    """Place circle on the board"""
    c = self.board[column]
    if c[0] != white:
      await self.bot.say('La columna {} está llena, has perdido tu turno'.format(str(column + 1)))

    i = -1
    while c[i] != white:
      i -= 1
    c[i] = color

    await self.checkWin()

  async def printBoard(self):
    """Show board game"""
    message = ''
    for y in range(self.rows):
      message += ' '.join(str(self.board[x][y]) for x in range(self.cols))
      message += '\n'
    return message

  async def checkComplete(self):
    """Check if board is complete"""
    columns = [self.board[c][0] for c in range(self.cols)]
    if not white in columns:
      await self.bot.say('EMPATE!')
      self.endgame = True
      self.is_started = False

  async def checkWin(self):
    """Check Win movement"""
    await self.checkComplete()
    w = await self.getWinner()
    if w:
      self.endgame = True
      self.is_started = False
      await self.bot.say('{} ha ganado!'.format(w))

  async def getWinner(self):
    """Get winner player"""
    lines = (
      self.board, # columns
      zip(*self.board), # rows
      diagonalsPos(self.board, self.cols, self.rows), # positive diagonals
      diagonalsNeg(self.board, self.cols, self.rows) # negative diagonals
    )

    for line in chain(*lines):
      for color, group in groupby(line):
        if color != white and len(list(group)) >= self.win:
          return color

def setup(bot):
  bot.add_cog(Game(bot))
