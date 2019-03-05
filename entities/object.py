import sdl
import game
import driver
from base import Base

class Object:
  def __init__(self, x, y, w, h, title, texture):
    self.xPos = x
    self.yPos = y
    self.width = w
    self.height = h
    self.title = title
    self.used = False
    self.currentTime = -1 
    self.currentFrame = 0
    self.texture = texture
    self.alpha = 0
    self.base = Base(self.xPos, self.yPos, self.width, self.height, 0, 0) 

  def updateAlpha(self,  dt):
    if self.alpha < 255:
      self.alpha += dt * 2
    if self.alpha >= 255:
      self.alpha = 255

  def updateBase(self):
      self.base.topRight = [self.xPos + self.width - 0, self.yPos + 0]
      self.base.bottomLeft = [self.xPos + 0, self.yPos + self.height] 

  def getRect(self, xMin, yMin):
    return sdl.Rect((int(self.xPos) - int(xMin), int(self.yPos) - int(yMin), self.width, self.height))

  def getTitle(self):
    return self.title

  def getCameraPos(self):
    return self.yPos + self.height

      #for bombs, to tell the direction of the explosion
  def getAttackingDirection(self, entity):

      by = self.yPos + self.height
      bx = self.xPos + self.width/2

      ey = entity.yPos + entity.height
      ex = entity.xPos  + entity.width/2

      yPosDiff = by - ey
      xPosDiff = bx - ex

      if abs(yPosDiff) >= abs(xPosDiff * 1.5):
        if by > ey: atkDir = 'n'
        else: atkDir = 's'
      elif abs(xPosDiff) > abs(yPosDiff * 1.5): 
        if bx > ex: atkDir = 'w'
        else: atkDir = 'e'
      elif yPosDiff >= 0 and xPosDiff >= 0:
        atkDir = 'nw'
      elif yPosDiff < 0 and xPosDiff >= 0:
        atkDir = 'sw'
      elif yPosDiff >=0 and xPosDiff < 0:
        atkDir = 'ne'
      elif yPosDiff < 0 and xPosDiff < 0:
        atkDir = 'se'
      return atkDir

  def renderSelf(self, time, renderer, xMin, yMin):
       if (self.xPos  + self.width - xMin < 0) or (self.yPos + self.height - yMin < 0):
          return
       elif (self.xPos > xMin + 800) or (self.yPos > yMin + 600):
          return 
       if self.title is 'pizza' or self.title is 'heart' or self.title is 'carrot' or self.title is 'bombObject':
          time1 = ((int(time / 250)) % 4)  #slowish
          spriteFrame = sdl.Rect((time1 * 50, 0, 50, 50))
          sdl .renderCopy(renderer, self.texture, spriteFrame, self.getRect(xMin, yMin))
       elif self.title is 'explosion':
          time1 = ((int(time / 250)) % 8) 
          if time1 is not self.currentTime: 
            self.currentFrame += 1
            spriteFrame = sdl.Rect((self.currentFrame * 200, 0, 200, 200))
            sdl.renderCopy(renderer, self.texture, spriteFrame, self.getRect(xMin, yMin))
            if self.currentFrame is 8:
              self.used = True
            self.currentTime = time1 
          else:
            spriteFrame = sdl.Rect((self.currentFrame * 200, 0, 200, 200))
            sdl.renderCopy(renderer, self.texture, spriteFrame, self.getRect(xMin, yMin))
       elif self.title is 'blackScreen':
         self.updateAlpha(1)
         sdl.setTextureAlphaMod(self.texture, int(self.alpha))
         sdl.renderCopy(renderer, self.texture, None, self.getRect(xMin, yMin))
       else:  
         sdl .renderCopy(renderer, self.texture, None, self.getRect(xMin, yMin))
         


