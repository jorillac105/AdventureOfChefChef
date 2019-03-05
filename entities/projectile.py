from base import Base
import driver
import game as chef
import math
import sdl

class Projectile: 
    def __init__(self, xPos, yPos, width, height, title, texture, renderer, degree, chefX, chefY):
      self.xPos = xPos
      self.yPos = yPos
      self.width = width
      self.height = height
      self.title = title
      self.base = Base(self.xPos, self.yPos, self.width, self.height, 0, 0) 
      self.texture = texture
      self.renderer = renderer
      self.projectileSpeed = 0.3
      self.currentTime = -1
      self.currentFrame = -1
      self.degree = degree
      self.chefY = chefY
      self.chefX = chefX  
      self.remove = False

    def getCollisionRect(self, xMin, yMin):
      return sdl.Rect((int(self.xPos) - int(xMin) + int(self.width / 4), int(self.yPos) - int(yMin) + int(self.height / 4), int(self.width / 2), int(self.height / 2)))

    def getCameraPos(self):
      return self.yPos + self.height

    # finds out what direction the projectile hits the enemy at to tell where to bump the enemy
    def getAttackingDirection(self, enemy):

      py = self.yPos + self.height/2
      px = self.xPos + self.width/2

      ey = enemy.yPos + enemy.height
      ex = enemy.xPos  + enemy.width/2

      yPosDiff = py - ey
      xPosDiff = px - ex

      if abs(yPosDiff) >= abs(xPosDiff * 1.5):
        if py > ey: atkDir = 'n'
        else: atkDir = 's'
      elif abs(xPosDiff) > abs(yPosDiff * 1.5): 
        if px > ex: atkDir = 'w'
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

    def updatePosition(self, dt):
      if self.title is 'green':
        self.projectileSpeed = 0.1
        self.yPos += dt *  self.projectileSpeed
      elif self.title is 'purple':
        self.projectileSpeed = 0.05
        self.yPos += dt *  self.projectileSpeed
      elif self.title is 'knife':
         self.projectileSpeed = 0.75
         self.yPos += dt * self.projectileSpeed * math.sin(self.degree) + int(self.chefY* dt)
         self.xPos += dt * self.projectileSpeed * math.cos(self.degree) + int(self.chefX* dt)
      elif self.title is 'fire':
         self.projectileSpeed = 0.15
         self.yPos += dt * self.projectileSpeed * math.sin(self.degree)
         self.xPos += dt * self.projectileSpeed * math.cos(self.degree) 
      elif self.title is 'fireSlow':
         self.projectileSpeed = 0.1
         self.yPos += dt * self.projectileSpeed * math.sin(self.degree)
         self.xPos += dt * self.projectileSpeed * math.cos(self.degree) 

    def updateBase(self):
      if self.title is 'purple':
        if self.currentFrame in [0,1]:
          self.base.topRight = [self.xPos + self.width - 100 , self.yPos + 100]
          self.base.bottomLeft = [self.xPos + 100, self.yPos + self.height - 100]
        elif self.currentFrame in [2, 3]:
          self.base.topRight = [self.xPos + self.width - 50 , self.yPos + 50]
          self.base.bottomLeft = [self.xPos + 50, self.yPos + self.height - 50]
        elif self.currentFrame in [2, 3, 4, 5]:
          self.base.topRight = [self.xPos + self.width, self.yPos + 30]
          self.base.bottomLeft = [self.xPos, self.yPos + self.height - 30]
      elif self.title is 'green':
        self.base.topRight = [self.xPos + self.width - 0 , self.yPos + 0]
        self.base.bottomLeft = [self.xPos + 0, self.yPos + self.height] 
      elif self.title is 'knife':
        self.base.topRight = [self.xPos + self.width - 0 , self.yPos + 0]
        self.base.bottomLeft = [self.xPos + 0, self.yPos + self.height] 

    def updateBasePvp(self):
       self.base.topRight = [self.xPos + self.width, self.yPos]
       self.base.bottomLeft = [self.xPos, self.yPos + self.height] 

    def getRect(self, xMin, yMin):
      if self.title is 'green':
        return sdl.Rect((int(self.xPos) - int(xMin), int(self.yPos) - int(yMin), 60, 60))
      elif self.title is 'purple':
        return sdl.Rect((int(self.xPos) - int(xMin), int(self.yPos)
       -  int(yMin), 400, 200))
      elif self.title is 'knife':
        return sdl.Rect((int(self.xPos) - int(xMin), int(self.yPos) - int(yMin), self.height, self.width))
      elif self.title is 'fire' or self.title is 'fireSlow':
        return sdl.Rect((int(self.xPos) - int(xMin), int(self.yPos) - int(yMin), self.width, self.height))

    def updateDegree(self, chef):
      yDiff = chef.yPos - self.yPos
      xDiff = chef.xPos - self.xPos
      self.degree =  math.atan2(yDiff, xDiff)

    def renderSelf(self, time, xMin, yMin):
      if self.title is 'green':
        currentFrame = ((int(time / 125)) % 6 )
        spriteFrame = sdl.Rect((currentFrame * 60, 0, 60, 60))
        sdl.renderCopy(self.renderer, self.texture, spriteFrame, self.getRect(xMin, yMin))
      elif self.title is 'purple':
        newTime = ((int(time / 400)) % 6 )
        if newTime is not self.currentTime:
          self.currentFrame += 1
        if self.currentFrame > 5:
          self.currentFrame = 5
        spriteFrame = sdl.Rect((self.currentFrame * 400, 0, 400, 200))
        sdl.renderCopy(self.renderer, self.texture, spriteFrame, self.getRect(xMin, yMin))  
      elif self.title is 'knife':
        tempRect =  self.getRect(xMin, yMin)
        sdl.renderCopyEx(self.renderer, self.texture, None, tempRect, math.degrees(self.degree) + 90, sdl.Point((tempRect.w//2, tempRect.h//2)), sdl.FLIP_NONE)
      elif self.title is 'fire' or self.title is 'fireSlow':
        currentFrame = ((int(time / 125)) % 4 )
        spriteFrame = sdl.Rect((currentFrame * 50, 0, 50, 150))
        tempRect =  self.getRect(xMin, yMin)
        sdl.renderCopyEx(self.renderer, self.texture, spriteFrame, tempRect, math.degrees(self.degree) - 90, sdl.Point((tempRect.w//2, tempRect.h//2)), sdl.FLIP_NONE)

    def renderLight(self, renderer, xMin, yMin):
      texture = driver.lightTextures[7]
      modX = 1
      modY = 1
      if self.title is 'green':
        texture = driver.lightTextures[6] # change to green
      elif self.title is 'purple':
        texture = driver.lightTextures[4] # change to purple
        modX = 1
        modY = 1
      elif self.title is 'knife':
        texture = driver.lightTextures[1] # change to green
        return
      textureW, textureH = chef.textureSize(texture)
      textureW = textureW / modX
      textureH = textureH / modY
      lightRect = sdl.Rect((0, 0, int(textureW), int(textureH)))
      sdl.setTextureBlendMode(texture, sdl.BLENDMODE_ADD)
      sdl.setTextureAlphaMod(texture, 128)
      posRect = sdl.Rect((int(self.xPos) - int(xMin) + int(self.width/2) - int(textureW/2) ,int(self.yPos) - int(yMin) + int(self.height/2) - int(textureH/2), int(textureW), int(textureH)))
      sdl.renderCopy(renderer, texture, None, posRect)