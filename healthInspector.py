import sys
sys.path.insert(0, '/../')
import sdl
import math
import game as chef
import random
import driver
import navGraph
from entity import Entity
from structure import Structure
from base import Base
from projectile import Projectile

class HealthInspector(Entity):
    def __init__(self, time, bossTextures):
        self.xPos =  600
        self.yPos = 200
        self.width = 75
        self.height = 140
        self.direction = 'e'
        self.previousDirection = 'e'
        self.speed = 0.05
        self.health = 20
        self.hurt = False
        self.hurtTime = 0
        self.changeInHp = 0
        self.attacking = 0 # 0 = not, 1 = up, 2 = right, 3 = down, 4 = down
        self.attackingTime = 0
        self.floorTile = 3
        self.base = Base(self.xPos, self.yPos, self.width, self.height, 0, 0)
        self.pathTime = time
        self.pathTimeUpdateRate = 1000
        self.directions = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']
        self.currentFrame = -1
        self.currentTime = -1
        self.projectiles = []
        self.dying = False
        self.dead = False
        self.bossTextures = bossTextures
        self.axis = 1  #vertical axis is 1, horizontal is 2
        self.transformed = False
        self.transforming = False
        self.spinning = False
        self.summoning = False
        self.currentTime = -1
        self.currentFrame = 0
        self.nextProjectileTime = 0
        self.ballWidth = 150
        self.ballHeight = 190 
        self.swarmType = 1
        self.phase = 1

    def updateBase(self):
      self.base.topRight = [self.xPos + self.width - 10, self.yPos + 30]
      self.base.bottomLeft = [self.xPos + 10, self.yPos + self.height]

    def intersects(self, other):
      self.updateBase()
      other.updateBase()
      # True if there's a collision.
      return not (self.base.topRight[0] < other.base.bottomLeft[0] or
				 self.base.bottomLeft[0] > other.base.topRight[0] or
				 self.base.topRight[1] > other.base.bottomLeft[1] or
				 self.base.bottomLeft[1] < other.base.topRight[1])




    def updateX(self, xPos):
      self.xPos = xPos

    def getXPos(self):
      return self.xPos

    def getYPos(self):
      return self.yPos

    def getHeight(self):
      return self.height

    def getWidth(self):
      return self.width

    def updateSize(self, size):
      self.size = size

    def updateDirection(self, direction):
      self.direction = direction

    def updateSpeed(self, speed):
      self.speed = speed

    def setHurt(self, bool):
      self.hurt = bool

    def setHurtTime(self, time):
       self.hurtTime = time

    def setAttacking(self, value):
      self.attacking = value

    def setAttackingTime(self, time):
       self.attackingTime = time

    def addProjectile(self, renderer):
        self.projectiles.append(Projectile(int(self.xPos) + 37, int(self.yPos) + 75, 50, 150, 'fire', self.bossTextures[12], renderer, math.radians(90), 0, 0))

    def swarm(self, renderer, chef): #a bunch of projectiles comming at ya at once 
      if self.swarmType is 1: 
        
        self.projectiles.append(Projectile(int(chef.xPos), int(chef.yPos) - 600, 50, 150, 'fireSlow', self.bossTextures[12], renderer, math.radians(90), 0, 0))
        self.projectiles.append(Projectile(int(chef.xPos), int(chef.yPos) + 600, 50, 150, 'fireSlow', self.bossTextures[12], renderer, math.radians(-90), 0, 0))
        self.projectiles.append(Projectile(int(chef.xPos) - 600, int(chef.yPos), 50, 150, 'fireSlow', self.bossTextures[12], renderer, math.radians(0), 0, 0))
        self.projectiles.append(Projectile(int(chef.xPos) + 600, int(chef.yPos), 50, 150, 'fireSlow', self.bossTextures[12], renderer, math.radians(180), 0, 0))
        self.swarmType = 2
      elif self.swarmType is 2: 
        self.projectiles.append(Projectile(int(chef.xPos) - 600, int(chef.yPos) - 600, 50, 150, 'fireSlow', self.bossTextures[12], renderer, math.radians(45), 0, 0))
        self.projectiles.append(Projectile(int(chef.xPos) - 600, int(chef.yPos) + 600, 50, 150, 'fireSlow', self.bossTextures[12], renderer, math.radians(-45), 0, 0))
        self.projectiles.append(Projectile(int(chef.xPos) + 600, int(chef.yPos) + 600, 50, 150, 'fireSlow', self.bossTextures[12], renderer, math.radians(225), 0, 0))
        self.projectiles.append(Projectile(int(chef.xPos) + 600, int(chef.yPos) - 600, 50, 150, 'fireSlow', self.bossTextures[12], renderer, math.radians(135), 0, 0))
        self.swarmType = 1
      #self.getDegrees(chef)

    # finds out what direction the boss hits the chef at to tell where to bump the chef
    def getAttackingDirection(self, chef):

      by = self.yPos + self.height
      bx = self.xPos + self.width/2

      cy = chef.yPos + chef.height
      cx = chef.xPos  + chef.width/2

      yPosDiff = by - cy
      xPosDiff = bx - cx

      if abs(yPosDiff) >= abs(xPosDiff * 1.5):
        if by > cy: atkDir = 'n'
        else: atkDir = 's'
      elif abs(xPosDiff) > abs(yPosDiff * 1.5): 
        if bx > cx: atkDir = 'w'
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



    def getDegrees(self, xPos, yPos, chef):
      yDiff = chef.yPos - yPos
      xDiff = chef.xPos - xPos
      self.degree =  math.atan2(yDiff, xDiff)

    def updatePosition(self, dt, map, chef, renderer):
        if self.yPos > 1195 and self.yPos < 1205 and self.axis is 1 and (chef.xPos > 850 or chef.xPos < 450):
          self.axis = 2
        elif self.xPos > 645 and self.xPos < 655 and self.axis is 2 and (chef.yPos > 1400 or chef.yPos < 1100):
          self.axis = 1

        if self.axis is 1:
          self.xPos = 655
          if self.yPos < chef.yPos:
            self.direction = 's'
            self.yPos += 0.05 * dt
          elif self.yPos > chef.yPos:
            self.direction = 'n'
            self.yPos -= 0.05 * dt
        if self.axis is 2:
          self.yPos = 1205
          if self.xPos < chef.xPos:
            self.direction = 'e'
            self.xPos += 0.05 * dt
          elif self.xPos > chef.xPos:
            self.direction = 'w'
            self.xPos -= 0.05 * dt

    def changeDirectionRandom(self):
      self.direction = self.directions[random.randint(0,7)]

    def changeDirection(self, targetNode, time):
         pass

    def getRect(self, xMin, yMin):
        return sdl.Rect((int(self.xPos) - int(xMin), int(self.yPos) - int(yMin), self.width, self.height))

    def getRect2(self, xMin, yMin): #when a ball
          return sdl.Rect((int(self.xPos - 37) - int(xMin), int(self.yPos - 37) - int(yMin), 150, 180))

    def getRect3(self, xMin, yMin): #when a ball
          return sdl.Rect((int(self.xPos - 37) - int(xMin), int(self.yPos - 37) - int(yMin), 150, 190))

    def getRect4(self, xMin, yMin):
          return sdl.Rect((int(self.xPos) - int(xMin) - 25, int(self.yPos) - int(yMin) - 30, 125, 170))

    def getRect3(self, xMin, yMin): #when a ball
       return sdl.Rect((int(self.xPos - 37) - int(xMin), int(self.yPos - 37) - int(yMin), int(self.ballWidth), int(self.ballHeight)))

    def getRect5(self, xMin, yMin): #when a ball
       if self.ballWidth > 10:
          self.ballWidth = self.ballWidth - 5
       if self.ballHeight > 10:
          self.ballHeight = self.ballHeight - (5 * (190.0 / 150.0))  
       return sdl.Rect((int(self.xPos - 37) + int((150.0 - self.ballWidth) / 2) - int(xMin), int(self.yPos - 37) + int((150.0 - self.ballHeight) / 2) - int(yMin), int(self.ballWidth), int(self.ballHeight)))

    def deathSize(self): #true if small enough to be considered dead
       if self.ballWidth <= 10 and self.ballHeight <= 10:
         return True
       else:
         return False 

    def getTexture(self):
      return self.texture

    def getHurt(self):
      return self.hurt

    def getHurtTime(self):
       return self.hurtTime

    def getAttacking(self):
      return self.attacking

    def getAttackingTime(self):
      return self.attackingTime

    def getCameraPos(self):
      return self.yPos + self.height - 40

    def goOppositeDirection(self):
      if self.direction =='w': self.direction = 'e'
      elif self.direction == 'e': self.direction = 'w'

    def renderSelf(self, time, renderer, xMin, yMin):
      frameTime = ((int(time / 250)) % 4)
      spriteFrame = sdl.Rect((frameTime * 75, 0, 75, 140))
      if self.dead:
        return
      if self.dying:
        frameTime = ((int(time / 125)) % 4 )
        if self.phase is 1:
          #frameTime = ((int(time / 125)) % 4 )
          if self.currentTime is not frameTime:
            self.currentFrame += 1
            self.currentTime = frameTime
            spriteFrame = sdl.Rect((1200 - (self.currentFrame * 150), 0, 150, 185))
            sdl .renderCopy(renderer, self.bossTextures[5], spriteFrame, self.getRect2(xMin, yMin))

            # once the animation for attacking runs through, set him back to not attacking
            # and reset the current frame to -1 (so it starts at frame 0 next run)
            if self.currentFrame >= 8:
              self.phase = 2
              self.currentFrame = -1
              self.currentTime = -1
          else:
            self.currentTime = frameTime
            spriteFrame = sdl.Rect((1200 - (self.currentFrame * 150), 0, 150, 185))
            sdl .renderCopy(renderer, self.bossTextures[5], spriteFrame, self.getRect2(xMin, yMin))
        elif self.phase is 2:
          if self.currentTime is not frameTime:
            self.currentFrame += 1
            self.currentTime = frameTime
            spriteFrame = sdl.Rect((self.currentFrame * 75, 0, 75, 140))
            sdl .renderCopy(renderer, self.bossTextures[14], spriteFrame, self.getRect(xMin, yMin))

            # once the animation for attacking runs through, set him back to not attacking
            # and reset the current frame to -1 (so it starts at frame 0 next run)
            if self.currentFrame >= 15:
              self.dead = True
              self.currentFrame = -1
              self.currentTime = -1
          else:
            self.currentTime = frameTime
            spriteFrame = sdl.Rect((self.currentFrame * 75, 0, 75, 140))
            sdl .renderCopy(renderer, self.bossTextures[14], spriteFrame, self.getRect(xMin, yMin))
      elif self.transforming:
           frameTime = ((int(time / 500)) % 4 )
           if self.currentTime is not frameTime:
             self.currentFrame += 1
             self.currentTime = frameTime
             spriteFrame = sdl.Rect((self.currentFrame * 150, 0, 150, 185))
             sdl .renderCopy(renderer, self.bossTextures[5], spriteFrame, self.getRect2(xMin, yMin))

             # once the animation for attacking runs through, set him back to not attacking
             # and reset the current frame to -1 (so it starts at frame 0 next run)
             if self.currentFrame >= 7:
               self.transforming = False
               self.transformed = True
               self.summoning = False 
               self.currentFrame = -1
               self.currentTime = -1
           else:
             self.currentTime = frameTime
             spriteFrame = sdl.Rect((self.currentFrame * 150, 0, 150, 185))
             sdl .renderCopy(renderer, self.bossTextures[5], spriteFrame, self.getRect2(xMin, yMin))
      elif self.hurt:
                frameTime = ((int(time /125)) % 4 )
                spriteFrame = sdl.Rect((frameTime * 75, 0, 75, 140))
                sdl .renderCopy(renderer, self.bossTextures[13], spriteFrame, self.getRect(xMin, yMin))
      elif self.transformed is False and not self.transforming:
          if self.summoning is True: 
               frameTime = ((int(time / 500)) % 4 )
               if self.currentTime is not frameTime:
                 self.currentFrame += 1
                 self.currentTime = frameTime
                 spriteFrame = sdl.Rect((self.currentFrame * 125, 0, 125, 170))
                 sdl .renderCopy(renderer, self.bossTextures[4], spriteFrame, self.getRect4(xMin, yMin))

                 # once the animation for attacking runs through, set him back to not attacking
                 # and reset the current frame to -1 (so it starts at frame 0 next run)
                 if self.currentFrame >= 8:
                   self.currentFrame = -1
                   self.summoning = False
                   self.currentTime = -1
               else:
                 self.currentTime = frameTime
                 spriteFrame = sdl.Rect((self.currentFrame * 125, 0, 125, 170))
                 sdl .renderCopy(renderer, self.bossTextures[4], spriteFrame, self.getRect4(xMin, yMin))
          elif self.summoning is False:
            if self.direction == 'e':
              sdl .renderCopy(renderer, self.bossTextures[0], spriteFrame, self.getRect(xMin, yMin))   #right
            elif self.direction == 'w':
              sdl .renderCopy(renderer, self.bossTextures[1], spriteFrame, self.getRect(xMin, yMin))   #left
            elif self.direction == 's':
              sdl .renderCopy(renderer, self.bossTextures[3], spriteFrame, self.getRect(xMin, yMin))   #down
            elif self.direction == 'n':
              sdl .renderCopy(renderer, self.bossTextures[2], spriteFrame, self.getRect(xMin, yMin))
      elif self.transformed is True:
        if not self.spinning:
          spriteFrame = sdl.Rect((frameTime * 150, 0, 150, 190))
          if self.direction == 'e':
            sdl .renderCopy(renderer, self.bossTextures[6], spriteFrame, self.getRect3(xMin, yMin))   #right
          elif self.direction == 'w':
            sdl .renderCopy(renderer, self.bossTextures[7], spriteFrame, self.getRect3(xMin, yMin))   #left
          elif self.direction == 's':
            sdl .renderCopy(renderer, self.bossTextures[9], spriteFrame, self.getRect3(xMin, yMin))   #down
          elif self.direction == 'n':
            sdl .renderCopy(renderer, self.bossTextures[8], spriteFrame, self.getRect3(xMin, yMin))   #up
        elif self.spinning:
               frameTime = ((int(time / 125)) % 4 )
               if self.currentTime is not frameTime:
                 self.currentFrame += 1
                 self.currentTime = frameTime
                 spriteFrame = sdl.Rect((self.currentFrame * 150, 0, 150, 190))
                 sdl .renderCopy(renderer, self.bossTextures[10], spriteFrame, self.getRect3(xMin, yMin))
                 if self.currentFrame >= 3:
                   self.currentFrame = -1
                   self.spinning = False
                   self.currentTime = -1
               else:
                 self.currentTime = frameTime
                 spriteFrame = sdl.Rect((self.currentFrame * 150, 0, 150, 190))
                 sdl .renderCopy(renderer, self.bossTextures[10], spriteFrame, self.getRect3(xMin, yMin))
                      
      self.renderHealth(renderer, xMin, yMin)


    def renderLight(self, renderer, xMin, yMin):
      # textureW, textureH = chef.textureSize(driver.lightTextures[1])
      # lightRect = sdl.Rect((0, 0, textureW, textureH))
      # sdl.setTextureBlendMode(driver.lightTextures[1], sdl.BLENDMODE_ADD)
      # sdl.setTextureAlphaMod(driver.lightTextures[1], 128)
      # posRect = sdl.Rect((int(self.xPos) - int(xMin) + int(self.width/2) - int(textureW/2) ,int(self.yPos) - int(yMin) + int(self.height/2) - int(textureH/2), textureW, textureH))
      # sdl.renderCopy(renderer, driver.lightTextures[1], lightRect, posRect)

      mod = 1
      texture = driver.lightTextures[5] # default blue
      if self.hurt:
        texture = driver.lightTextures[7] # change to red
        sdl.setTextureAlphaMod(texture, 255)
      elif self.summoning:
        texture = driver.lightTextures[6] # change to green
        sdl.setTextureAlphaMod(texture, 64)
        mod = 10
      elif self.transforming:
        texture = driver.lightTextures[3] # change to orange
        sdl.setTextureAlphaMod(texture, 64)
      elif self.transformed:
        texture = driver.lightTextures[7] # change to red
        sdl.setTextureAlphaMod(texture, 64)
      
      if self.dying:
        color = (self.currentFrame % 5) + 3
        texture = driver.lightTextures[color]
        sdl.setTextureAlphaMod(texture, 255)
        if color is 6:
          mod = 10

      textureW, textureH = chef.textureSize(texture)
      textureW *= mod
      textureH *= mod
      lightRect = sdl.Rect((0, 0, textureW, textureH))
      sdl.setTextureBlendMode(texture, sdl.BLENDMODE_ADD)
      
      posRect = sdl.Rect((int(self.xPos) - int(xMin) + int(self.width/2) - int(textureW/2) ,int(self.yPos) - int(yMin) + int(self.height/2) - int(textureH/2), textureW, textureH))
      sdl.renderCopy(renderer, texture, lightRect, posRect)


    def renderHealth(self, renderer, xMin, yMin):
       for i in range(self.health):
         spot = sdl.Rect((int(self.xPos) - int(xMin) + 14*i - int(14*(self.health/2)) + int(self.width/2), int(self.yPos) - int(yMin) + int(self.height) - 10, 12, 12))
         sdl.renderCopy(renderer, self.bossTextures[11], None, spot)

    def updateHealth(self, dh):
      self.health += dh
      self.changeInHp = dh
      if self.health <= 0:
          if self.transformed is False:
              self.transforming = True
              self.health = 30
          elif self.transformed is True:
              self.dying = True



    def resetDamageChange(self):
      self.changeInHp = 0
