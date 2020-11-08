import os, IPython
from PIL import Image, ImageDraw, ImageFont
import random

from logging import getLogger
logger = getLogger(__name__)

try:
  from apng import APNG
except ModuleNotFoundError:
  logger.error(f'!pip install APNG  を忘れないで')

colors = '#de9610,#c93a40,#fff001,#d06d8c,#65ace4,#a0c238,#56a764,#d16b16,#cc528b,#9460a0,#f2cf01,#0074bf'.split(',')

def random_color(i=None):
  if i is None:
    i = random.randint(0, len(colors)-1)
  if isinstance(i, int):
    return colors[i % len(colors)]
  return i

class ASubject(object):
  parent: object

  def setParent(self, parent):
    self.parent = parent

  def theme_color(self, c=None):
    if isinstance(c, int) or c is None:
      return random_color(c)
    return c

  def taken(self, draw):
    logger.warning(f'TODO: taken(draw) in {self.__class__.__name__}')
    pass

class AComposite(object):
  width: int
  height: int
  subjects: list # 被写体のリスト

  def __init__(self, width=400, height=400, color='white'):
    self.width = width
    self.height = height
    self.color = color
    self.subjects = []

  def add(self, subject):
    subject.setParent(self)
    self.subjects.append(subject)

  def taken(self, draw):
    for subject in self.subjects:
      subject.taken(draw)

class AStudio(AComposite):
  files: list # 撮影した写真ファイルのリスト
  def __init__(self, width=400, height=400, background='white'):
    super().__init__(width, height, background)
    self.files = []

  def take(self):
    canvas = Image.new('RGBA', (self.width, self.height), self.color)
    draw = ImageDraw.Draw(canvas)
    self.taken(draw)
    index = len(self.files)
    filename = f'frame{index}.png'
    canvas.save(filename)
    self.files.append(filename)

  def create(self, filename='anime.png', delay=100):
    APNG.from_files(self.files, delay=delay).save(filename)
    for image in self.files:
      os.remove(image) # 不要なファイルは消す
    self.files = []
    return filename

class Rectangle(ASubject):
  def __init__(self, x, y, width, height, color=None):
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.color = self.theme_color(color)

  def taken(self, draw):
    x, y = self.x, self.y
    dx = self.width // 2
    dy = self.height // 2
    draw.rectangle((x-dx, y-dy, x+dx, y+dx), fill=self.color)