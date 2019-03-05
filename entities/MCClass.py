import sdl
import math
import game as chef
import driver
import levelZero
from emitter import Emitter
from structure import Structure
from base import Base

class Chef:
    def __init__(self, xPos, yPos, width, height, direction, speed, velX, velY,
  accX, accY, textures, canBeHit, canBeHitTime, dizzyTime, health, cursor, floorTile):
        self.xPos = xPos
        self.yPos = yPos
        self.width = width
        self.height = height
        self.direction = direction
        self.speed = speed
        self.velX = velX
        self.velY = velY
        self.accX = accX
        self.accY = accY
        # [idle, walk up, walk right, walk down, walk left, dizzy, heart]
        self.textures = textures
        self.canBeHit = canBeHit
        self.canBeHitTime = canBeHitTime
        self.dizzyTime = dizzyTime
        self.dizzy = False
        self.weapons = []
        self.collision = False
        self.health = health
        self.attacking = False
        self.attackingTime = 0
        self.placingBomb = False
        self.currentTime = -1
        self.currentFrame = -1
        self.changeInHp = 0
        self.cursor = cursor
        self.camera = None
        self.energy = 8
        self.energyRegenTime = 0
        self.hasKey = False
        self.emitters = []
        self.floorTile = floorTile
        self.graters = False
        self.items = []
        self.score = 0
        self.base = Base(self.xPos, self.yPos, self.width, self.height, 13, 60)
        self.degree = 0
        self.degreePress = False #True if a or s or d or w is being pressed or held down
        self.knifeAttacking = False
        self.knifeAttackingTime = 0
        self.knifeDelay = 200
        self.projectiles = []
        self.title = None
        self.gottenItems = []
        self.dead = False
        self.dying = False

    def updateBase(self):
      self.base.topRight = [self.xPos + self.width - 13, self.yPos + 60]
      self.base.bottomLeft = [self.xPos + 13, self.yPos + self.height]

    def updateBasePvp(self):
       self.base.topRight = [self.xPos + self.width, self.yPos]
       self.base.bottomLeft = [self.xPos, self.yPos + self.height]

    def resetChef(self):
        self.canBeHit = True
        self.canBeHitTime = 10000
        self.dizzyTime = 0
        self.dizzy = False
        self.weapon = 'none'
        self.health = 3
        self.attacking = False
        self.attackingTime = 0
        self.changeInHp = 0
        self.cursor = False
        self.camera = None
        self.energy = 8
        self.energyRegenTime = 0
        self.hasKey = False
        self.emitters = []
        self.floorTile = [1]
        self.graters = False
        self.items = []
        self.score = 0
        self.weapons = []
        self.projectiles = []
        self.title = None
        self.xPos = 250
        self.yPos = 250
        self.velX = 0
        self.velY = 0
        self.dead = False
        self.dying = False

    def updateDegrees(self, value):
      self.degree += value
      if self.degree > 2 * math.pi:
        self.degree -= 2 * math.pi
      elif self.degree < 0:
        self.degree += 2 * math.pi

    def updateTitle(self, title):
      self.title = title

    def addEmitter(self):
      emit = Emitter(self.xPos, self.yPos, None, 3000)
      self.emitters.append(emit)
      emit.emit(50)

    def addItem(self, item):
      self.items.append(item)

    def addWeapon(self, weapon):
      self.weapons.append(weapon)

    def removeItem(self, item):
      if item not in self.items:
        print("Cannot remove item that does not exist!")
      else:
        self.items.remove(item)

    def renderEmitters(self, renderer, xMin, yMin):
      for emitter in self.emitters:
        emitter.renderSelf(renderer, xMin, yMin)

    def updateEmitters(self, dt):
      for emitter in self.emitters:
        emitter.update(dt)
        if emitter.empty():
          self.emitters.remove(emitter)

    # THE CHEFS CONTACT AREA WITH THE GROUND IS HIS FEET
    def intersects(self, other):
      self.updateBase()
      other.updateBase()
      # True if there's a collision.
      return not (self.base.topRight[0] < other.base.bottomLeft[0] or
         self.base.bottomLeft[0] > other.base.topRight[0] or
         self.base.topRight[1] > other.base.bottomLeft[1] or
         self.base.bottomLeft[1] < other.base.topRight[1])

    # checks to see if the chef runs into any of the objects on the screen
    def checkCollisions(self, immediateSurroundings, map):
      gameWidth = len(map[0]) * 50
      gameHeight = len(map) * 50
      if self.xPos <= 0:
        self.xPos = 0
      elif self.xPos + self.width >= gameWidth:
        self.xPos = gameWidth - self.width
      if self.yPos <= 0:
        self.yPos = 0
      elif self.yPos + self.height >= gameHeight:
         self.yPos = gameHeight - self.height

      collisions = False
      for structure in immediateSurroundings:
        if self.intersects(structure):
          collisions = True
      return collisions

    def addCamera(self, camera):
      self.camera = camera

    def updateX(self, xPos):
      if self.title is None:
        self.camera.updateChefX(xPos)
      else:
        self.camera.updateChef2X(xPos)


    def updateY(self, yPos):
      if self.title is None:
        if self.cursor is False:
          self.camera.updateChefY(yPos)
        else:
          self.yPos = yPos
      else:
        if self.cursor is False:
          self.camera.updateChef2Y(yPos)
        else:
          self.yPos = yPos


    def updateSize(self, size):
      self.size = size

    def updateAccX(self, acc):
       self.accX = acc

    def updateAccY(self, acc):
       self.accY = acc

    def setCanBeHit(self, bool):
       self.canBeHit = bool

    def setDizzy(self, bool):
       self.dizzy = bool

    def setCanBeHitTime(self, time):
       self.canBeHitTime = time

    def setDizzyTime(self, time):
        self.dizzyTime = time

    def setAttacking(self, bool):
        self.attacking = bool
        #self.addEmitter()

    def setAttackingTime(self, time):
        self.attackingTime = time

    def setEnergyRegenTime(self, time):
        self.energyRegenTime = time

    def setPlacingBomb(self, b):
      self.placingBomb = b

    def setGottenItems(self, item):
      self.gottenItems.append(item)

    def updateDirection(self, up, down, left, right):
        if not self.dizzy and not self.placingBomb:
          if (up and down) or (left and right): self.direction = 'none'
          elif up and right: self.direction = 'ne'
          elif down and right: self.direction = 'se'
          elif down and left: self.direction = 'sw'
          elif up and left: self.direction = 'nw'
          elif up: self.direction = 'n'
          elif left: self.direction = 'w'
          elif down: self.direction = 's'
          elif right: self.direction = 'e'
          else: self.direction = 'none'
        else:
          self.direction = 'none' #IF HE IS HIT INPUT DOESN'T REGISTER

    def updateVelX(self, vel):
       self.velX= vel

    def updateVelY(self, vel):
       self.velY= vel

    # returns true if a collidable object is within the 8 tiles around it
    def getImmediateSurroundings(self, map):
      surroundings = []
      xTile = int(int(self.xPos + 13) / 50) # + 13 is for the base width correction
      yTile = int(int(self.yPos + 65) / 50) # + 65 is for the height width correction
      for y in range(3):
        for x in range(3):
          # to prevent us from checking map blocks that dont exist
          if ((yTile - 1 + y) < len(map) and
    (yTile - 1 + y) >= 0 and
    (xTile -1 + x) < len(map[0]) and
    (xTile -1 + x) >= 0):
            value = map[yTile - 1 + y][xTile -1 + x]
            floor = False
            for i in range(len(self.floorTile)):
              if value is self.floorTile[i]:
                floor = True

            if not floor:
                surroundings.append(Structure(value,  (xTile -1 + x) *50, (yTile - 1 + y) *50, None, False, None))
      return surroundings

    def bump(self, direction):
      if "n" in direction:
        self.velY = -.4
      elif "s" in direction:
        self.velY = .4
      if "e" in direction:
        self.velX = .4
      elif "w" in direction:
        self.velX = -.4

    # finds out what direction the chef hits the enemy at to tell where to bump the enemy
    def getAttackingDirection(self, enemy):

      cy = self.yPos + self.height
      cx = self.xPos + self.width/2

      ey = enemy.yPos + enemy.height
      ex = enemy.xPos  + enemy.width/2

      yPosDiff = cy - ey
      xPosDiff = cx - ex

      if abs(yPosDiff) >= abs(xPosDiff * 1.5):
        if cy > ey: atkDir = 'n'
        else: atkDir = 's'
      elif abs(xPosDiff) > abs(yPosDiff * 1.5):
        if cx > ex: atkDir = 'w'
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

    def updatePosition(self, dt, map, keyPress):
          #self.updateEmitters(dt)
          oldY = self.yPos
          oldX = self.xPos
          oldVelX = self.velX
          oldVelY = self.velY
          oldAccX = self.accX
          oldAccY = self.accY

          if self.direction == "none" or keyPress is False:
            if abs(self.velY) < 0.02: self.velY = 0
            else:
              if self.velY > 0:  self.velY -= self.accY * dt
              else: self.velY += self.accY * dt
            if abs(self.velX) < 0.02: self.velX = 0
            else:
              if self.velX > 0: self.velX -= self.accX * dt
              else: self.velX += self.accX * dt
          elif self.direction == "n":
            if abs(self.velX) < 0.02: self.velX = 0
            else:
              if self.velX > 0: self.velX -= self.accX * dt
              else: self.velX += self.accX * dt
            self.velY -= self.accY * dt
          elif self.direction == "e":
            if abs(self.velY) < 0.02: self.velY = 0
            else:
              if self.velY > 0:  self.velY -= self.accY * dt
              else: self.velY += self.accY * dt
            self.velX += self.accX * dt
          elif self.direction == "s":
            if abs(self.velX) < 0.02: self.velX = 0
            else:
              if self.velX > 0: self.velX -= self.accX * dt
              else: self.velX += self.accX * dt
            self.velY += self.accY * dt
          elif self.direction == "w":
            if abs(self.velY) < 0.02: self.velY = 0
            else:
              if self.velY > 0:  self.velY -= self.accY * dt
              else: self.velY += self.accY * dt
            self.velX -= self.accX * dt
          elif self.direction == "ne":
            self.velY -= self.accY * dt
            self.velX += self.accX* dt
          elif self.direction == "nw":
            self.velY -= self.accY * dt
            self.velX -= self.accX * dt
          elif self.direction == "se":
            self.velY += self.accY * dt
            self.velX += self.accX * dt
          elif self.direction == "sw":
            self.velY += self.accY * dt
            self.velX -= self.accX * dt

          #limit the max velocity
          if self.velY > 0:
            if self.velY > 0.4: self.velY = 0.4
          else:
            if self.velY < -0.4: self.velY = -0.4
          if self.velX > 0:
            if self.velX > 0.4: self.velX = 0.4
          else:
            if self.velX < -0.4: self.velX = -0.4

          if self.velY is not 0:
            newY = int(round(self.yPos + int(self.velY* dt)))
            self.updateY(newY)

          # if there is a collision dont update the y pos
          if self.checkCollisions(self.getImmediateSurroundings(map), map):
              self.updateY(oldY)
              self.velY = -self.velY * .1

          if self.velX is not 0:
            newX = int(round(self.xPos + int(self.velX* dt)))
            self.updateX(newX)

          # if there is a collision dont update the x pos
          if self.checkCollisions(self.getImmediateSurroundings(map), map):
              self.updateX(oldX)
              self.velX = -self.velX * .1

    def getRect(self, xMin, yMin):
      return sdl.Rect((int(self.xPos) - int(xMin) ,int(self.yPos) - int(yMin), self.width, self.height))

    def getRectAttack(self, xMin, yMin):
      return sdl.Rect((int(self.xPos - 9) - int(xMin), int(self.yPos) - int(yMin), self.width + 19, self.height))

    def getRectDying(self, xMin, yMin):
        return sdl.Rect((int(self.xPos) - int(xMin) - 50, int(self.yPos) - int(yMin) - 50, 86, 137))

    def getTexture(self):
      return self.textures

    def getDirection(self):
      return self.direction

    def getCanBeHit(self):
      return self.canBeHit

    def getCanBeHitTime(self):
      return self.canBeHitTime

    def getDizzy(self):
      return self.dizzy

    def getDizzyTime(self):
     return self.dizzyTime

    def getVelX(self):
      return self.velX

    def getVelY(self):
      return self.velY

    def getAttacking(self):
        return self.attacking

    def getAttackingTime(self):
        return self.attackingTime

    def getEnergyRegenTime(self):
        return self.energyRegenTime

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

    def updateEnergy(self, value):
      self.energy += value

    def getEnergy(self):
      return self.energy

    def getCameraPos(self):
      return self.yPos + self.height

    def getNumBombs(self):
      num = 0
      for obj in self.weapons:
        if obj == 'bombObject':
          num += 1
      return num

    def getNode(self, navGraph):
      x = (self.xPos + (self.width//2)) //50
      y = (self.yPos + self.height)//50

      node = navGraph.getNode(x, y)
      if node is None:
        print("node is None at x = ", x,", y = ", y)
      return node

    def inGottenItems(self, item):
      if item in self.gottenItems:
        return True
      return False

    def renderSelf(self, time, renderer, xMin, yMin, keyPress):
      xMin = xMin
      yMin = yMin
      self.renderDamage(renderer, xMin, yMin)

      time1 = ((int(time / 125)) % 4)  #fast
      time3 = ((int(time / 100)) % 6)  #faster
      time2 = ((int(time / 500)) % 4) #slow
      if self.dead:
        return
      if self.dying:
        frameTime = time1
        spriteFrame = sdl.Rect((self.currentFrame * 161, 0, 161, 274))
        if self.currentTime is not frameTime:
            self.currentFrame += 1
            self.currentTime = frameTime
            if self.currentFrame is 15:
              self.currentFrame = -1
              self.dead = True
        sdl .renderCopy(renderer, self.textures[0][13], spriteFrame, self.getRectDying(xMin, yMin))
      elif not self.dizzy and not self.placingBomb:
        if self.knifeAttacking:
          spriteFrame = sdl.Rect((time1 * 67, 0, 67, 80))
          sdl .renderCopy(renderer, self.textures[0][12], spriteFrame, self.getRectAttack(xMin, yMin))
        elif not self.attacking:
          spriteFrame = sdl.Rect((time1 * 48, 0, 48, 80))
          spriteFrame2 = sdl.Rect((time2 * 48, 0, 48, 80))
          if self.direction == 'none':
            sdl.renderCopy(renderer, self.textures[0][0], spriteFrame2, self.getRect(xMin, yMin))
          elif self.direction == 'n' or self.direction == 'ne' or self.direction == 'nw':
            if keyPress is True:
              sdl .renderCopy(renderer, self.textures[0][1], spriteFrame, self.getRect(xMin, yMin))
            else:
              sdl .renderCopy(renderer, self.textures[0][11], spriteFrame2, self.getRect(xMin, yMin))
          elif self.direction == 's' or self.direction == 'se' or self.direction == 'sw':
            if keyPress is True:
              sdl .renderCopy(renderer, self.textures[0][3], spriteFrame, self.getRect(xMin, yMin))
            else:
              sdl .renderCopy(renderer, self.textures[0][0], spriteFrame2, self.getRect(xMin, yMin))
          elif self.direction == 'e':
            if keyPress is True:
              sdl .renderCopy(renderer, self.textures[0][2], spriteFrame, self.getRect(xMin, yMin))
            else:
              sdl .renderCopy(renderer, self.textures[0][10], spriteFrame2, self.getRect(xMin, yMin))
          elif self.direction == 'w':
            if keyPress is True:
              sdl .renderCopy(renderer, self.textures[0][4], spriteFrame, self.getRect(xMin, yMin))
            else:
              sdl .renderCopy(renderer, self.textures[0][9], spriteFrame2, self.getRect(xMin, yMin))
        else: # if attacking
          spriteFrame = sdl.Rect((time1 * 67, 0, 67, 80))
          if 'graters' in self.weapons:
            sdl .renderCopy(renderer, self.textures[0][7], spriteFrame, self.getRectAttack(xMin, yMin))
          else:
            sdl .renderCopy(renderer, self.textures[0][6], spriteFrame, self.getRectAttack(xMin, yMin))
      elif self.dizzy:
          spriteFrame3 = sdl.Rect((time3 * 48, 0, 48, 80))
          sdl .renderCopy(renderer, self.textures[0][5], spriteFrame3, self.getRect(xMin, yMin))
      elif self.placingBomb:

          if self.currentTime is not time1:
            self.currentFrame += 1
            self.currentTime = time1
            spriteFrame = sdl.Rect((self.currentTime  * 48, 0, 48, 80))
            sdl .renderCopy(renderer, self.textures[0][8], spriteFrame, self.getRect(xMin, yMin))

          # once the animation for attacking runs through, set him back to not attacking
          # and reset the current frame to -1 (so it starts at frame 0 next run)
          if self.currentFrame is 4:
            self.currentFrame = -1
            self.currentTime = -1
            self.setPlacingBomb(False)
          else:
            self.currentTime = time1
            spriteFrame = sdl.Rect((self.currentTime  * 48, 0, 48, 80))
            sdl .renderCopy(renderer, self.textures[0][8], spriteFrame, self.getRect(xMin, yMin))

    def renderLight(self, renderer, xMin, yMin):
      return
      textureW, textureH = chef.textureSize(driver.lightTextures[1])
      lightRect = sdl.Rect((0, 0, textureW, textureH))
      sdl.setTextureBlendMode(driver.lightTextures[1], sdl.BLENDMODE_ADD)
      if 'carrot' not in driver.chef.items:
        posRect = sdl.Rect((int(self.xPos) - int(xMin) + int(self.width/2) - int(textureW/2) ,int(self.yPos) - int(yMin) + int(self.height/2) - int(textureH/2), textureW, textureH))
      else:
        posRect = sdl.Rect((int(self.xPos) - int(xMin) + int(self.width/2) - int(textureW) ,int(self.yPos) - int(yMin) + int(self.height/2) - int(textureH), textureW*2, textureH*2))
      sdl.renderCopy(renderer, driver.lightTextures[1], lightRect, posRect)

    def renderHealth(self, renderer):
      for i in range(self.health):
        spot = sdl.Rect((10 + i*55, 10, 50, 50))
        sdl.renderCopy(renderer, self.textures[1][0], None, spot)

    def renderHealthPvp(self, renderer):
      if self.title is None:
        for i in range(self.health):
          spot = sdl.Rect((10 + i*55, 10, 50, 50))
          sdl.renderCopy(renderer, self.textures[1][0], None, spot)
      else:
        for i in range(self.health):
          spot = sdl.Rect(((16 * 50) - 65 - i*55, 10, 50, 50))
          sdl.renderCopy(renderer, self.textures[1][0], None, spot)

    def renderEnergy(self, renderer, top):
      if top:
        spot = sdl.Rect((800 -130, 480, 120, 120))
      else:
        spot = sdl.Rect((800 -130, 10, 120, 120))
      sdl.renderCopy(renderer, self.textures[2][self.energy], None, spot)

    def updateHealth(self, dh):
      self.health += dh
      self.changeInHp = dh
      if self.health <= 0:
          self.dying = True

    def getHealth(self):
      return self.health

    def resetDamageChange(self):
      self.changeInHp = 0

    def renderDamage(self, renderer, xMin, yMin):

      #if there has been any change in health
      if (self.changeInHp != 0):
        #create the string
        stringDamage = str(self.changeInHp)
        #make it red
        color = sdl.Color((255,0,0)).cdata[0]
        #but if the "damage" is positive (ie, healing)
        if (self.changeInHp > 0):
          #show that it is positive
          stringDamage = "+" + str(self.changeInHp)
          #and make it green
          color = sdl.Color((0,255,0)).cdata[0]

        dmgSurf = sdl.ttf.renderText_Solid(driver.scoreFont, stringDamage, color)
        dmgTexture = renderer.createTextureFromSurface(dmgSurf)
        textureW, textureH = chef.textureSize(dmgTexture)
        dmgRect = sdl.Rect()
        dmgRect.x = int(self.xPos + textureW//6 - xMin)
        dmgRect.y = int(self.yPos - textureH - yMin)
        dmgRect.w = textureW
        dmgRect.h = textureH
        dmgRect.x = int(dmgRect.x)
        dmgRect.y = int(dmgRect.y)
        sdl.renderCopy(renderer, dmgTexture, None, dmgRect)
        sdl.freeSurface(dmgSurf)
        sdl.destroyTexture(dmgTexture)

    def renderItems(self, renderer):
      for x in range(len(self.items)):
        spot = sdl.Rect((10 + x*55, 65, 50, 50))
        if self.items[x] is 'key':
          sdl.renderCopy(renderer, self.textures[1][1], None, spot)
        elif self.items[x] is 'carrot':
          sdl.renderCopy(renderer, self.textures[1][2], None, spot)

    def renderWeapons(self, renderer):
      for x in range(len(self.weapons)):
        spot = sdl.Rect((10 + x*55, 120, 50, 50))
        if self.weapons[x] is 'ladles':
          sdl.renderCopy(renderer, self.textures[1][3], None, spot)
        if self.weapons[x] is 'graters':
          sdl.renderCopy(renderer, self.textures[1][4], None, spot)
        if self.weapons[x] is 'bomb':
          sdl.renderCopy(renderer, self.textures[1][5], None, spot)
        if self.weapons[x] is 'knives':
          sdl.renderCopy(renderer, self.textures[1][9], None, spot)

    def renderEnergyMessage(self, renderer, xMin, yMin):
      textureW, textureH = chef.textureSize(self.textures[2][9])
      message = sdl.Rect((240, 500, textureW, textureH))
      sdl.renderCopy(renderer, self.textures[2][9], None, message)

    def renderNoWepMessage(self, renderer, xMin, yMin):
      textureW, textureH = chef.textureSize(self.textures[2][14])
      message = sdl.Rect((240, 500, textureW, textureH))
      sdl.renderCopy(renderer, self.textures[2][14], None, message)
