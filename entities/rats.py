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

class Enemy(Entity):
    def __init__(self, xPos, yPos, width, height, direction, speed, health, floorTile, time, navGraph):
        self.xPos = xPos
        self.yPos = yPos
        self.width = width
        self.height = height 
        self.direction = direction
        self.speed = speed
        self.health = health 
        self.hurt = False 
        self.hurtTime = 0
        self.changeInHp = 0
        self.attacking = 0 # 0 = not, 1 = up, 2 = right, 3 = down, 4 = down
        self.attackingTime = 0 
        self.floorTile = floorTile
        self.base = Base(self.xPos, self.yPos, self.width, self.height, 10, 30)
        self.pathTime = time
        self.pathTimeUpdateRate = 1000
        self.directions = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']
        self.navGraph = navGraph
        self.angleX = 0.0
        self.angleY = 0.0
        self.dirChangeTime = time
        self.bumpDir = "n"

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

    def updateY(self, yPos):
      self.yPos = yPos

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

    # finds out what direction the rats hits the guy at and changes the 
    # attacking animation accordingly 
    def getAttackingDirection(self, character):

       ry = self.yPos + self.height
       rx = self.xPos + self.width/2

       cy = character.yPos + character.height
       cx = character.xPos  + character.width/2

       yPosDiff = ry - cy
       xPosDiff = rx - cx

       if abs(yPosDiff) >= abs(xPosDiff * 1.5):
          if ry > cy:
            self.attacking = 1
            atkDir = 'n'
          else:
            self.attacking = 3
            atkDir = 's'
       elif abs(xPosDiff) > abs(yPosDiff * 1.5): 
          if rx > cx:
            self.attacking = 4
            atkDir = 'w'
          else:
            self.attacking = 2
            atkDir = 'e'
       elif yPosDiff >= 0 and xPosDiff >= 0:
          self.attacking = 1
          atkDir = 'nw'
       elif yPosDiff < 0 and xPosDiff >= 0:
          self.attacking = 3
          atkDir = 'sw'
       elif yPosDiff >=0 and xPosDiff < 0:
          self.attacking = 1
          atkDir = 'ne'
       elif yPosDiff < 0 and xPosDiff < 0:
          self.attacking = 3
          atkDir = 'se'
       return atkDir

    # 1=N 2=E 3=S 4=W 0=not bumping
    def bump(self, direction):
      self.bumpDir = direction


    def getNode(self):
        xRat = int(self.xPos + self.width//2)//50
        yRat = int(self.yPos + self.height - 1)//50

        return self.navGraph.getNode(xRat, yRat)

    def initialNavigation(self, chefNode):
        ratNode = self.getNode()
        self.path = self.navGraph.navigate(ratNode, ratNode)
        #self.path = self.navGraph.navigate(ratNode, chefNode)

    def updatePosition(self, dt, map, navGraph, chefNode, time):

	# if the rats are off the screen place them back on 
      gameWidth = self.navGraph.getWidth()
      gameHeight = self.navGraph.getHeight()

      if self.xPos <= 0:
        self.xPos = 1
        self.changeDirection(chefNode, time, chefNode) 
      elif self.xPos + self.width >= gameWidth:
        self.xPos = gameWidth - self.width - 1
        self.changeDirection(chefNode, time, chefNode) 
      if self.yPos <= 0:
        self.yPos = 1
        self.changeDirection(chefNode, time, chefNode) 
      elif self.yPos + self.height >= gameHeight:
        self.yPos = gameHeight - self.height -1
        self.changeDirection(chefNode, time, chefNode)  

      oldX = self.xPos
      oldY = self.yPos

      ratNode = self.getNode()
      rx, ry = ratNode.getPos()
      cx, cy = chefNode.getPos()

      dist = math.sqrt((rx - cx)**2 + (ry-cy)**2)


      # to prevent lots of pathing rats at the same time
      if navGraph.getLevel() is 4:
        dist += 5
      elif navGraph.getLevel() is 5:
        dist -= 10

      if dist < 11:

        self.speed = .1

        if self.pathTime <= time:

          self.path = navGraph.navigate(ratNode, chefNode)
          #if the rat is closer to the chef, update the path more often
          self.pathTime = time + len(self.path)*250

        if len(self.path) is 0:
          if ratNode is chefNode:
            self.goOppositeDirection(time)
          else:
            self.path = navGraph.navigate(ratNode, chefNode)
            self.pathTime = time + len(self.path)*500
        else:
          targetX, targetY = self.path[0].getPos()
          n = self.path[0]
          nx, ny = n.getPos()
          dist = math.sqrt((self.xPos + self.width//2 - (targetX * 50 + 25))**2 + (self.yPos + self.height - (targetY*50 + 35))**2)

          if dist <= 50 and dist > 10:
            self.changeDirection(self.path[0], time, chefNode)
          elif dist <= 10 and dist > 5:
            self.changeDirection(self.path[0], time, chefNode)
          elif dist <= 5:
            self.path.pop(0)
            if len(self.path) is not 0:
              self.changeDirection(self.path[0], time, chefNode)

        if not self.attacking:
          if not self.hurt: # if not recently damaged or currently attacking
            self.updateX(self.xPos - round(self.speed * (math.cos(self.angleX)) * dt))
            self.updateY(self.yPos + round(self.speed * (math.sin(self.angleY)) * dt))
          else:
            bumpSpeed = .4 - math.sqrt(1000000 - (self.getHurtTime() - time)**2) / 2500
            if "n" in self.bumpDir:
              self.updateY(int(self.yPos - bumpSpeed* dt))
            elif "s" in self.bumpDir:
              self.updateY(int(self.yPos + bumpSpeed* dt))
            if "e" in self.bumpDir:
              self.updateX(int(self.xPos + bumpSpeed* dt))
            elif "w" in self.bumpDir:
              self.updateX(int(self.xPos - bumpSpeed* dt))

        if self.checkCollisions(self.getImmediateSurroundings(map)):  #if there was a collision don't update pos
          self.yPos = oldY
          self.xPos = oldX

          self.path.insert(0, self.getNode())
          nx, ny = self.path[0].getPos()
          # print ("COLLISION:")
          # print ("current node : x = ",self.xPos + self.width//2, " y = ", self.yPos + self.height)
          # print ("recentered node : x = ", nx*50 + 25, " y = ", ny*50+35)

          self.xPos = nx*50 + 25 - self.width//2
          self.yPos = ny*50 + 35 - self.height

          self.goOppositeDirection(time)

      else:
        self.speed = .05
        if self.pathTime <= time:
          self.pathTime = time + random.randint(1000,2000)
          self.changeDirectionRandom()


        if not self.hurt and not self.attacking: # if not recently damaged or currently attacking
          if self.direction == "n":
            self.updateY(int(self.yPos - self.speed* dt)) 
          elif self.direction == "e":
            self.updateX(int(self.xPos + self.speed* dt)) 
          elif self.direction == "s":
            self.updateY(int(self.yPos + self.speed* dt))    
          elif self.direction == "w":
            self.updateX(int(self.xPos - self.speed* dt))     
          elif self.direction == "ne":
            self.updateY(int(self.yPos - self.speed* dt))  
            self.updateX(int(self.xPos + self.speed* dt)) 
          elif self.direction == "nw":
            self.updateY(int(self.yPos - self.speed* dt))  
            self.updateX(int(self.xPos - self.speed* dt)) 
          elif self.direction == "se":
            self.updateY(int(self.yPos + self.speed* dt))  
            self.updateX(int(self.xPos + self.speed* dt)) 
          elif self.direction == "sw":
            self.updateY(int(self.yPos + self.speed* dt))  
            self.updateX(int(self.xPos - self.speed* dt))

        if self.checkCollisions(self.getImmediateSurroundings(map)):  #if there was a collision don't update pos
          self.yPos = oldY
          self.xPos = oldX
          self.changeDirectionRandom()

    def changeDirectionRandom(self):
      self.direction = self.directions[random.randint(0,7)]

    def changeDirection(self, targetNode, time, chefNode):
              targetX , targetY = targetNode.getPos()
              targetX *= 50
              targetX += 25
              targetY *= 50
              targetY += 35

              yPosDiff = -(self.yPos + self.height - targetY)
              xPosDiff = self.xPos + self.width//2 - targetX
              dist = math.sqrt((xPosDiff)**2 + (yPosDiff)**2)

              if dist <= 1.0:
                dist = 1.0

              self.angleX = math.acos(xPosDiff/dist)
              self.angleY = math.asin(yPosDiff/dist)

              if self.dirChangeTime <= time:
                #self.dirChangeTime = time + 500
                cx, cy = chefNode.getPos()
                rx, ry = self.getNode().getPos()

                yPosDiff = ry - cy
                xPosDiff = rx - cx
 
                if abs(yPosDiff) >= abs(xPosDiff * 2):
                  if ry > cy: self.direction = 'n'
                  else: self.direction = 's'
                elif abs(xPosDiff) > abs(yPosDiff * 2): 
                  if rx > cx: self.direction = 'w'
                  else: self.direction = 'e'
                elif yPosDiff >= 0 and xPosDiff >= 0:
                  self.direction = 'nw'
                elif yPosDiff < 0 and xPosDiff >= 0:
                  self.direction = 'sw'
                elif yPosDiff >=0 and xPosDiff < 0:
                  self.direction = 'ne'
                elif yPosDiff < 0 and xPosDiff < 0:
                  self.direction = 'se'

              targetY -= 35
              targetY /= 50
              targetX -= 25
              targetX /= 50
          
         
    def getRect(self, xMin, yMin):
      return sdl.Rect((int(self.xPos) - int(xMin), int(self.yPos) - int(yMin), self.width, self.height))

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
      return self.yPos + self.height
   
    def goOppositeDirection(self, time):

      ratNode = self.getNode()
      rx, ry = ratNode.getPos()

      x = random.randint(-3,3)
      y = random.randint(-3,3)

      while not self.navGraph.nodeExists(rx + x, ry + y):
        x = random.randint(-3,3)
        y = random.randint(-3,3)


      targetNode = self.navGraph.getNode(rx + x, ry + y)

      self.path = self.navGraph.navigate(ratNode, targetNode)
      self.pathTime = time + len(self.path)*250

      # if self.direction == 'n': self.direction = 's'
      # elif self.direction == 's': self.direction = 'n' 
      # elif self.direction =='w': self.direction = 'e' 
      # elif self.direction == 'e': self.direction = 'w'
      # elif self.direction =='ne': self.direction = 'sw'
      # elif self.direction == 'nw': self.direction = 'se'
      # elif self.direction == 'se': self.direction = 'nw'
      # elif self.direction == 'sw': self.direction = 'ne'     

    def renderSelf(self, time, renderer, xMin, yMin, ratTextures):
      if (self.xPos  + self.width - xMin < 0) or (self.yPos + self.height - yMin < 0):
        return
      elif (self.xPos > xMin + 800) or (self.yPos > yMin + 600):
        return 
      time = ((int(time / 125)) % 4) 
      spriteFrame = sdl.Rect((time * 50, 0, 50, 60))
      if not self.hurt: # if not hurt
        if self.attacking is 0: # if not attacking
          if self.direction == 'n' or self.direction == 'ne' or self.direction == 'nw':
            sdl .renderCopy(renderer, ratTextures[1], spriteFrame, self.getRect(xMin, yMin))   
          elif self.direction == 's' or self.direction == 'se' or self.direction == 'sw':
            sdl .renderCopy(renderer, ratTextures[3], spriteFrame, self.getRect(xMin, yMin))   
          elif self.direction == 'e':
            sdl .renderCopy(renderer, ratTextures[2], spriteFrame, self.getRect(xMin, yMin))   
          elif self.direction == 'w':
            sdl .renderCopy(renderer, ratTextures[4], spriteFrame, self.getRect(xMin, yMin))   
        else:  # if attacking
         if self.attacking == 1: 
           sdl .renderCopy(renderer, ratTextures[5], spriteFrame, self.getRect(xMin, yMin))
         if self.attacking == 2: 
           sdl .renderCopy(renderer, ratTextures[6], spriteFrame, self.getRect(xMin, yMin))
         if self.attacking == 3: 
           sdl .renderCopy(renderer, ratTextures[7], spriteFrame, self.getRect(xMin, yMin))
         if self.attacking == 4: 
           sdl .renderCopy(renderer, ratTextures[8], spriteFrame, self.getRect(xMin, yMin))
      elif self.hurt:   # if hurt
         sdl .renderCopy(renderer, ratTextures[0], spriteFrame, self.getRect(xMin, yMin)) 
      self.renderHealth(renderer, xMin, yMin, ratTextures)
      #self.renderLight(renderer, xMin, yMin, ratTextures[10])

    def renderLight(self, renderer, xMin, yMin):
      if 'carrot' in driver.chef.items:
        textureW, textureH = chef.textureSize(driver.lightTextures[0])
        lightRect = sdl.Rect((0, 0, textureW, textureH))
        sdl.setTextureBlendMode(driver.lightTextures[0], sdl.BLENDMODE_ADD)
        sdl.setTextureAlphaMod(driver.lightTextures[0], 128)
        posRect = sdl.Rect((int(self.xPos) - int(xMin) + int(self.width/2) - int(textureW/2) ,int(self.yPos) - int(yMin) + int(self.height/2) - int(textureH/2), textureW, textureH))
        sdl.renderCopy(renderer, driver.lightTextures[0], lightRect, posRect)

    def renderHealth(self, renderer, xMin, yMin, ratTextures):
      for i in range(self.health):
        spot = sdl.Rect((int(self.xPos) - int(xMin) + 14*i, int(self.yPos) - int(yMin) - 14, 12, 12))
        sdl.renderCopy(renderer, ratTextures[9], None, spot)

    def updateHealth(self, dh):
      self.health += dh
      self.changeInHp = dh

    def resetDamageChange(self):
      self.changeInHp = 0 
