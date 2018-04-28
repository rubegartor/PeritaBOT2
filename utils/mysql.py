import pymysql
import configparser
from run import Bot

class Connect:
  def __init__(self):
    self.Bot = Bot()
    def getConfig(dict, key):
      config = configparser.ConfigParser()
      config.read(self.Bot.config + 'config.ini')
      return config[dict][key]

    self.db = pymysql.connect(getConfig('MySQL', 'host'), getConfig('MySQL', 'user'), getConfig('MySQL', 'password'), getConfig('MySQL', 'database'), charset='utf8mb4') # HOST | USER | PASSWORD | DATABASE

  def select(self, query):
      cursor = self.db.cursor()
      cursor.execute(query)
      return [row for row in cursor.fetchall()]

  def insert(self, query):
    try:
      cursor = self.db.cursor()
      cursor.execute(query)
      self.db.commit()
    except Exception as e:
      self.db.rollback()

  def update(self, query):
    try:
      cursor = self.db.cursor()
      cursor.execute(query)
      self.db.commit()
    except Exception as e:
      print(e)
      self.db.rollback()

  def delete(self, query):
    try:
      cursor = self.db.cursor()
      cursor.execute(query)
      self.db.commit()
    except Exception as e:
      self.db.rollback()

  def close(self):
    self.db.close()
