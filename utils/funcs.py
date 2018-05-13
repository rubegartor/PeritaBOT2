import os

class Funcs:
  def readFile(self, file):
    with open(file, encoding='utf-8') as _file:
      return _file.read()

  def toList(self, array):
    return [(x.split('_')[0], x) for x in array]

  def toFiles(self, path):
      return [x for x in os.listdir(path)]
