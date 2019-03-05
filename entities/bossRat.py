import sys
sys.path.insert(0, '/../')
import sdl
import math
import game as chef
import random
import driver
from entity import Entity
from structure import Structure
from base import Base 
from projectile import Projectile

class BossRat(Entity):
    def __init__(self, time):
        self.xPos =  1195
        self.yPos = -50
        self.width = 300
        self.height = 400 
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
        self.base = Base(self.xPos, self.yPos, self.width, self.height, 50, 200)
        self.pathTime = time
        self.pathTimeUpdateRate = 1000
        self.directions = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']
        self.currentFrame = -1 
        self.currentTime = -1
        self.projectiles = [Projectile(0,0,0,0, 'none', 0, 0, 0, 0, 0)]
        self.dying = False
        self.dead = False
        self.endOfOrange = False

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

    # checks to see if the rat runs into any of the objects on the screen
    def checkCollisions(self, immediateSurroundings):
      collisions = False
      for structure in immediateSurroundings:
        if self.intersects(structure): 
          collisions = True 
      return collisions

    def getImmediateSurroundings(self, map):
      surroundings = []
      xTile = int(int(self.xPos + 10) / 50) # + 10 is for the base width correction
      yTile = int(int(self.yPos + 30) / 50) # + 30 is for the hight width correction 
      for y in range(3):
        for x in range(3):
          # to prevent us from checking map blocks that dont exist
          if ((yTile - 1 + y) < len(map) and 
		(yTile - 1 + y) >= 0 and
		(xTile -1 + x) < len(map[0]) and
		(xTile -1 + x) >= 0): 
            value = map[yTile - 1 + y][xTile -1 + x]
            if value is not self.floorTile: 
              surroundings.append(Structure(value,  (xTile -1 + x) *50, (yTile - 1 + y) *50, None, False, None))
      return surroundings

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

    def updatePosition(self, dt, map, character, time):
      if not self.hurt and not self.attacking: # if not recently damaged or currently attacking
        if self.direction == "e":
          self.updateX(int(self.xPos + self.speed* dt))     
        elif self.direction == "w":
          self.updateX(int(self.xPos - self.speed* dt))     

        if self.xPos > 1250:
          self.direction = 'w'
        elif self.xPos < 900:
          self.direction = 'e' 

        if abs((self.xPos + (self.width/2)) - (character.xPos + (character.width / 2))) < 50: 
          self.direction = 's' 
        elif self.direction is not 'w' and self.direction is not 'e': 
          x = random.randint(1,2)
          if x is 1:
            self.direction = 'e'
          else:
            self.direction = 'w'

    def getRect(self, xMin, yMin):
      if self.attacking is not 2:
        return sdl.Rect((int(self.xPos) - int(xMin), int(self.yPos) - int(yMin), self.width, self.height))
      else: 
        return sdl.Rect((int(self.xPos - 200) - int(xMin), int(self.yPos - 200) - int(yMin), self.width + 400, self.height + 400))

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

    def renderSelf(self, time, renderer, xMin, yMin, bossTextures):
      if (self.xPos  + self.width - xMin < 0) or (self.yPos + self.height - yMin < 0):
        return
      elif (self.xPos > xMin + 800) or (self.yPos > yMin + 600):
        return 
      frameTime = ((int(time / 125)) % 4) 
      spriteFrame = sdl.Rect((frameTime * 300, 0, 300, 400))
      if self.dead:
        return
      if self.dying:
        frameTime = ((int(time / 500)) % 4 )
        if self.currentTime is not frameTime:
          self.currentFrame += 1
          self.currentTime = frameTime
          spriteFrame = sdl.Rect((self.currentFrame * 300, 0, 300, 400))
          sdl .renderCopy(renderer, bossTextures[9], spriteFrame, self.getRect(xMin, yMin))

          # once the animation for attacking runs through, set him back to not attacking
          # and reset the current frame to -1 (so it starts at frame 0 next run)
          if self.currentFrame is 10: 
            self.currentFrame = -1
            self.attacking = 0
            self.currentTime = -1
            self.dead = True
            self.dying = False
        else:
          self.currentTime = frameTime
          spriteFrame = sdl.Rect((self.currentFrame * 300, 0, 300, 400))
          sdl .renderCopy(renderer, bossTextures[9], spriteFrame, self.getRect(xMin, yMin)) 
      
      elif not self.hurt: # if not hurt
        if self.attacking is 0: # if not attacking
          if self.direction == 'e':
            sdl .renderCopy(renderer, bossTextures[1], spriteFrame, self.getRect(xMin, yMin))   #right
          elif self.direction == 'w':
            sdl .renderCopy(renderer, bossTextures[2], spriteFrame, self.getRect(xMin, yMin))   #left
          elif self.direction == 's':
            sdl .renderCopy(renderer, bossTextures[8], spriteFrame, self.getRect(xMin, yMin))   #idle
        else:  # if attacking
         if self.attacking == 1:  # GREEN ATTACK
           frameTime = ((int(time / 125)) % 4 )
           if self.currentTime is not frameTime:
             self.currentFrame += 1
             self.currentTime = frameTime
             spriteFrame = sdl.Rect((self.currentFrame * 300, 0, 300, 400))
             sdl .renderCopy(renderer, bossTextures[3], spriteFrame, self.getRect(xMin, yMin))
             if self.currentFrame is 4: 
               self.projectiles.append(Projectile(int(self.xPos) + 100, int(self.yPos) + 400, 60, 60, 'green', bossTextures[4], renderer, 0, 0, 0))

             # once the animation for attacking runs through, set him back to not attacking
             # and reset the current frame to -1 (so it starts at frame 0 next run)
             if self.currentFrame >= 6: 
               self.currentFrame = -1
               self.attacking = 0
               self.currentTime = -1 
           else:
             self.currentTime = frameTime
             spriteFrame = sdl.Rect((self.currentFrame * 300, 0, 300, 400))
             sdl .renderCopy(renderer, bossTextures[3], spriteFrame, self.getRect(xMin, yMin)) 
            
         elif self.attacking == 2:  # ORANGE ATTACK
           frameTime = ((int(time / 125)) % 4 )
           if self.currentTime is not frameTime:
             self.currentFrame += 1
             self.currentTime = frameTime
             spriteFrame = sdl.Rect((self.currentFrame * 700, 0, 700, 800))
             sdl .renderCopy(renderer, bossTextures[5], spriteFrame, self.getRect(xMin, yMin))

             # once the animation for attacking runs through, set him back to not attacking
             # and reset the current frame to -1 (so it starts at frame 0 next run)
             if self.currentFrame >= 8: 
               self.currentFrame = -1
               self.attacking = 0
               self.currentTime = -1
               self.endOfOrange = True;
           else:
             self.currentTime = frameTime
             spriteFrame = sdl.Rect((self.currentFrame * 700, 0, 700, 800))
             sdl .renderCopy(renderer, bossTextures[5], spriteFrame, self.getRect(xMin, yMin)) 

         elif self.attacking == 3:  # PURPLE ATTACK
           frameTime = ((int(time / 125)) % 4 )
           if self.currentTime is not frameTime:
             self.currentFrame += 1
             self.currentTime = frameTime
             spriteFrame = sdl.Rect((self.currentFrame * 300, 0, 300, 400))
             sdl .renderCopy(renderer, bossTextures[6], spriteFrame, self.getRect(xMin, yMin))

             if self.currentFrame is 4: 
               self.projectiles.append(Projectile(int(self.xPos) - 100, int(self.yPos) + 400, 400, 200, 'purple', bossTextures[7], renderer, 0, 0, 0))

             # once the animation for attacking runs through, set him back to not attacking
             # and reset the current frame to -1 (so it starts at frame 0 next run)
             if self.currentFrame >= 6: 
               self.currentFrame = -1
               self.attacking = 0
               self.currentTime = -1
           else:
             self.currentTime = frameTime
             spriteFrame = sdl.Rect((self.currentFrame * 300, 0, 300, 400))
             sdl .renderCopy(renderer, bossTextures[6], spriteFrame, self.getRect(xMin, yMin)) 

         if self.attacking == 4: 
           sdl .renderCopy(renderer, bossTextures[8], spriteFrame, self.getRect(xMin, yMin))
      elif self.hurt:   # if hurt
         sdl .renderCopy(renderer, bossTextures[0], spriteFrame, self.getRect(xMin, yMin))
      self.renderHealth(renderer, xMin, yMin, bossTextures[10])

    def renderLight(self, renderer, xMin, yMin):
      mod = 1
      texture = driver.lightTextures[7] # default red
      if self.attacking is 1:
        texture = driver.lightTextures[6] # change to green
        sdl.setTextureAlphaMod(texture, 64)
        mod = 10
      elif self.attacking is 2:
        texture = driver.lightTextures[3] # change to orange
        sdl.setTextureAlphaMod(texture, 64)
      elif self.attacking is 3:
        texture = driver.lightTextures[4] # change to purple
        sdl.setTextureAlphaMod(texture, 64)
      if self.hurt:
        texture = driver.lightTextures[5] # change to blue
        sdl.setTextureAlphaMod(texture, 64)
      if self.dying:
        color = (self.currentFrame % 5) + 3
        texture = driver.lightTextures[color] # change to self.currentFrame % len(driver.lightTextures)
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


    def renderHealth(self, renderer, xMin, yMin, texture):
       for i in range(self.health):
         spot = sdl.Rect((int(self.xPos) - int(xMin) + 14*i, int(self.yPos) - int(yMin) + int(self.height) - 30, 12, 12))
         sdl.renderCopy(renderer, texture, None, spot)

    def updateHealth(self, dh):
      self.health += dh
      self.changeInHp = dh
      if self.health <= 0:
        self.dying = True
      self.currentFrame = -1

    def resetDamageChange(self):
      self.changeInHp = 0 
