import os, IPython
from PIL import Image, ImageDraw, ImageFont
from kolab.anime.color import ColorTheme
from apng import APNG

from logging import getLogger
logger = getLogger(__name__)

DefaultColorTheme = ColorTheme()

class ASubject(object):
  parent: object

  def taken(self, draw):
    logger.warning(f'TODO: taken(draw) in {self.__class__.__name__}')
    pass

  def isVisible(self):
    return True

  def autoColor(self, c=None):
    return DefaultColorTheme.color(c)

  def setParent(self, parent):
    self.parent = parent

  def removed(self):
    if self.parent is not None:
      self.parent.remove(self)
      self.parent = None


class AComposite(ASubject):
  width: int
  height: int
  subjects: list # 被写体のリスト

  def __init__(self, width=400, height=400):
    self.width = width
    self.height = height
    self.subjects = []

  def add(self, *subjects):
    for subject in subjects:
      subject.setParent(self)
      self.subjects.append(subject)

  def remove(self, subject):
    if subject in self.subjects:
      self.subjects.remove(subject)

  def taken(self, draw):
    for subject in self.subjects:
      if subject.isVisible():
        subject.taken(draw)

class AStudio(AComposite):
  background: object
  files: list # 撮影した写真ファイルのリスト

  def __init__(self, width=400, height=400, background='white', theme=None):
    global DefaultColorTheme
    super().__init__(width, height)
    self.background = background
    self.files = []
    DefaultColorTheme = ColorTheme(theme)

  def take(self):
    canvas = Image.new('RGBA', (self.width, self.height), self.background)
    draw = ImageDraw.Draw(canvas)
    self.taken(draw)
    index = len(self.files)
    filename = f'frame{index}.png'
    canvas.save(filename)
    self.files.append(filename)

  def create(self, filename='anime.png', delay=200):
    APNG.from_files(self.files, delay=delay).save(filename)
    for image in self.files:
      os.remove(image) # 不要なファイルは消す
    self.files = []
    return filename

# 被写体

class Rectangle(ASubject):
  def __init__(self, cx, cy, width, height=None, color=None):
    self.cx = cx
    self.cy = cy
    self.width = width
    self.height = width if height is None else height
    self.color = self.autoColor(color)

  def setPosition(self, cx, cy):
    self.cx = cx
    self.cy = cy

  def magnify(self, xscale, yscale):
    self.width *= xscale
    self.height *= yscale

  def taken(self, draw):
    cx = self.cx
    cy = self.cy
    dx = self.width // 2
    dy = self.height // 2
    draw.rectangle((cx-dx, cy-dy, cx+dx, cy+dx), fill=self.color)

class Circle(Rectangle):
  def __init__(self, cx, cy, width, height=None, color=None):
    Rectangle.__init__(self, cx, cy, width, height, color)    

  def taken(self, draw):
    cx = self.cx
    cy = self.cy
    dx = self.width // 2
    dy = self.height // 2
    draw.ellipse((cx-dx, cy-dy, cx+dx, cy+dx), fill=self.color)

def totext(f):  #  変数も文字列に変更する
  try:
    return str(f())
  except:
    return str(f)

class Caption(ASubject):
  def __init__(self, text, x, y, fontsize=40, color=None):
    self.text = text
    self.x = x
    self.y = y 
    self.text = text
    self.font = ImageFont.truetype('/usr/share/fonts/truetype/humor-sans/Humor-Sans.ttf', fontsize)
    self.color = self.autoColor(color)

  def taken(self, draw): 
    text = totext(self.text)
    draw.text((self.x, self.y), text, font=self.font, fill=self.color)