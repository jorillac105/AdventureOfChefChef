import driver
import MCClass
import rats
import bossRat
import random
import math
import sdl
import object
import operator
import game

class Camera():

	def __init__(self, chef, chef2, mapOf, mapTextures, objects, enemies, emitters, width, height, ratTextures, structures, level, boss, bossTextures):
		self.chef = chef
		self.chef2 = chef2
		self.chef.addCamera(self)
		self.objects = objects
		self.enemies = enemies
		self.map  = mapOf
		self.mapTextures = mapTextures
		self.xShift = 0.0
		self.yShift = 0
		self.xMin = 0.0 #left most camera screen pos
		self.yMin = 0.0
		self.width = width
		self.height = height
		self.ratTextures = ratTextures
		self.structures = structures
		self.top = False
		self.level =  level
		self.emitters = emitters
		self.shake = False
		self.shakeTime = 0
		self.shakeIntensityX = 20
		self.shakeIntensityY = 20
		if level is 2:
			cmSurf = sdl.image.load("graphics/messages/carrot_message.png")
			self.cmTexture = driver.renderer.createTextureFromSurface(cmSurf)
			sdl.freeSurface(cmSurf)
		self.bossTextures = bossTextures
		self.boss = boss
		if level > 0:
			#self.blackScreenTexture = driver.renderer.createTextureFromSurface(sdl.image.load('graphics/ui/light.png'))
			#self.blackScreenTexture = driver.renderer.createTextureFromSurface(sdl.image.load('graphics/colors/black.png'))
			# self.blackScreenTexture = driver.renderer.createTextureFromSurface(sdl.image.load('graphics/ui/blueDark.png'))
			self.blackScreenTexture = driver.renderer.createTextureFromSurface(sdl.image.load('graphics/colors/darkGo.png'))
			sdl.setTextureBlendMode(self.blackScreenTexture, sdl.BLENDMODE_MOD)
			#sdl.setTextureAlphaMod(self.blackScreenTexture, 255)

	def updateChefX(self, xPos):
		self.chef.xPos = xPos
		if (self.chef.xPos >= 300) and (self.chef.xPos + self.chef.width < len(self.map[0]) * 50 - 300):
			if self.chef.xPos < self.xMin + 300:
				self.xMin = self.chef.xPos - 300
			if self.chef.xPos + self.chef.width > self.xMin + 500:
				self.xMin = self.chef.xPos + self.chef.width - 500

		if self.chef.xPos < self.xMin + 300:
			self.xMin = self.chef.xPos - 300
		if self.chef.xPos + self.chef.width > self.xMin + 500:
			self.xMin = self.chef.xPos + self.chef.width - 500

		if self.chef.xPos < 300:
			self.xMin = 0.0
		elif self.chef.xPos + self.chef.width >= len(self.map[0]) * 50 - 300:
			self.xMin = len(self.map[0]) * 50 - 810 * 1.0

	def updateChef2X(self, xPos):
		self.chef2.xPos = xPos
		if (self.chef2.xPos >= 300) and (self.chef2.xPos + self.chef2.width < len(self.map[0]) * 50 - 300):
			if self.chef2.xPos < self.xMin + 300:
				self.xMin = self.chef2.xPos - 300
			if self.chef2.xPos + self.chef2.width > self.xMin + 500:
				self.xMin = self.chef2.xPos + self.chef2.width - 500

		if self.chef2.xPos < self.xMin + 300:
			self.xMin = self.chef2.xPos - 300
		if self.chef2.xPos + self.chef2.width > self.xMin + 500:
			self.xMin = self.chef2.xPos + self.chef2.width - 500

		if self.chef2.xPos < 300:
			self.xMin = 0.0
		elif self.chef2.xPos + self.chef2.width >= len(self.map[0]) * 50 - 300:
			self.xMin = len(self.map[0]) * 50 - 810 * 1.0

	def updateChefY(self, yPos):
		self.chef.yPos = yPos
		if self.chef.yPos >= 200 and self.chef.yPos + self.chef.height < len(self.map) * 50 - 200:
			self.top = False
			if self.chef.yPos < self.yMin + 200:
				self.yMin = self.chef.yPos - 200
			if self.chef.yPos + self.chef.height > self.yMin + 400:
				self.yMin = self.chef.yPos + self.chef.height - 400
		elif self.chef.yPos < 200:
			self.top = True
			self.yMin = 0
		elif self.chef.yPos + self.chef.height >= len(self.map) * 50 - 200:
			self.top = False
			self.yMin = len(self.map) * 50 - 610

	def updateChef2Y(self, yPos):
		self.chef2.yPos = yPos
		if self.chef2.yPos >= 200 and self.chef2.yPos + self.chef2.height < len(self.map) * 50 - 200:
			self.top = False
			if self.chef2.yPos < self.yMin + 200:
				self.yMin = self.chef2.yPos - 200
			if self.chef2.yPos + self.chef2.height > self.yMin + 400:
				self.yMin = self.chef2.yPos + self.chef2.height - 400
		elif self.chef2.yPos < 200:
			self.top = True
			self.yMin = 0
		elif self.chef2.yPos + self.chef2.height >= len(self.map) * 50 - 200:
			self.top = False
			self.yMin = len(self.map) * 50 - 610

	def activateShake(self, time, shakingtime, Xintensity, Yintensity):
		self.shakeTime = time + shakingtime
		self.shake = True
		self.shakeIntensityX = Xintensity
		self.shakeIntensityY = Yintensity

	def overlayblack(self):
		if 'carrot' not in driver.chef.items:
			blackRect = sdl.Rect((int(self.chef.xPos - 800) - int(self.xMin), (self.chef.yPos - 600) - int(self.yMin), 1600, 1200))
		else:
			blackRect = sdl.Rect((int(self.chef.xPos - 1200) - int(self.xMin), (self.chef.yPos - 900) - int(self.yMin), 2400, 1800))
		if self.level is 5:
			blackRect = sdl.Rect((int(self.chef.xPos - 1800) - int(self.xMin), (self.chef.yPos - 1350) - int(self.yMin), 3600, 2700))
		sdl.renderCopy(driver.renderer, self.blackScreenTexture, None, blackRect)

	def display(self, currentTime, dt, keyPress, globalTime):
		overlay = True
		if currentTime > self.shakeTime:
			self.shake = False


		if self.boss is not None:
			if self.level is 3: 
				if self.boss.dying and not self.boss.dead:
					self.xMin = int((len(self.map[0]) * 50) - 801)
					self.yMin = 1
					overlay = False
			elif self.level is 5:
				if self.boss.dying and not self.boss.dead:
					self.xMin = int((self.boss.xPos + 75  - 400))
					self.yMin = int((self.boss.yPos + 95  - 300))
					if self.xMin < 0: self.xMin = 0 
					elif self.xMin > len(self.map[0]) * 50 - 800: self.xMin = len(self.map[0]) * 50 - 801
					if self.yMin < 0: self.yMin = 0 
					elif self.yMin > len(self.map) * 50 - 600: self.yMin = len(self.map) * 50 - 601
					overlay = False
				elif self.boss.transforming and not self.boss.transformed:
					self.xMin = int((self.boss.xPos + 75  - 400))
					self.yMin = int((self.boss.yPos + 95  - 300))
					if self.xMin < 0: self.xMin = 0 
					elif self.xMin > len(self.map[0]) * 50 - 800: self.xMin = len(self.map[0]) * 50 - 801
					if self.yMin < 0: self.yMin = 0 
					elif self.yMin > len(self.map) * 50 - 600: self.yMin = len(self.map) * 50 - 601
					overlay = False

				

		oldxMin = self.xMin
		oldyMin = self.yMin
		if self.shake:
			#self.xMin += math.sin(random.random() * math.pi * 2) * self.shakeIntensityX
			#self.xMin += math.sin(currentTime/10) * self.shakeIntensityX
			self.xMin += random.randint(0, int(self.shakeIntensityX))
			if self.xMin <  0: self.xMin = -self.xMin
			if self.xMin + 800 >= (len(self.map[0])) * 50: self.xMin = self.xMin - 50
			#self.yMin += math.sin(random.random() * math.pi * 2) * self.shakeIntensityY
			#self.yMin += math.sin(currentTime/10) * self.shakeIntensityY
			self.yMin += random.randint(0, int(self.shakeIntensityY))
			if self.yMin <  0: self.yMin = -self.yMin
			if self.yMin + 600 >= (len(self.map)) * 50: self.yMin = self.yMin - 50


		sdl.renderClear(driver.renderer)
		tilesPlaced = 0
		tileValue = 0
		for i in range(13):  # RIGHT NOW ITS FOR 12 ROW AND 16 COLLUMS
			for j in range(17): # AKA THE 600 x 800 PIXELS OF OUR SCREEEN
				tileValue = self.map[i + int(self.yMin / 50)][j + int(self.xMin / 50)]
				tileRect = sdl.Rect((int(50 * j) - int(self.xMin % 50) , int(50 * i) - int(self.yMin % 50), 50, 50))
				sdl.renderCopy(driver.renderer, self.mapTextures[tileValue - 1], None, tileRect)

		#Sorting experiment:

		renderArray = []
		renderArray.extend(self.enemies)
		renderArray.extend(self.structures)
		renderArray.extend(self.objects)
		renderArray.extend(self.emitters)
		renderArray.append(self.chef)
		if self.chef2 is not None:
			renderArray.append(self.chef2)
		if self.boss is not None:
			renderArray.append(self.boss)

		sortedArray = sorted(renderArray, key=operator.methodcaller('getCameraPos'))

		for obj in sortedArray:
			if (type(obj).__name__ == "Enemy"):
				obj.renderSelf(currentTime, driver.renderer, self.xMin, self.yMin, self.ratTextures)
			elif (type(obj).__name__ == "BossRat"):
				obj.renderSelf(currentTime, driver.renderer, self.xMin, self.yMin, self.bossTextures)
			elif (type(obj).__name__ == "Emitter"):
				obj.renderSelf(driver.renderer, self.xMin, self.yMin, dt)
				if (obj.getTime() <= currentTime):
					self.emitters.remove(obj)
			elif (type(obj).__name__ == "Chef"):
				obj.renderSelf(currentTime, driver.renderer, self.xMin, self.yMin, keyPress)
			else:
				obj.renderSelf(currentTime, driver.renderer, self.xMin, self.yMin)

		if self.boss is not None:
			if len(self.boss.projectiles) is not 0:
				for projectile in self.boss.projectiles:
					if projectile.title is 'green' or projectile.title is 'purple' or projectile.title is 'knife' or projectile.title is 'fire' or projectile.title is 'fireSlow':
						projectile.renderSelf(currentTime, self.xMin, self.yMin)
		if len(self.chef.projectiles) is not 0:
			for projectile in self.chef.projectiles:
				if projectile.title is 'green' or projectile.title is 'purple' or projectile.title is 'knife':
					projectile.renderSelf(currentTime, self.xMin, self.yMin)
		if self.chef2 is not None:
			if len(self.chef2.projectiles) is not 0:
				for projectile in self.chef2.projectiles:
					if projectile.title is 'green' or projectile.title is 'purple' or projectile.title is 'knife':
						projectile.renderSelf(currentTime, self.xMin, self.yMin)

		if self.level >= 2:
			if overlay:
				self.overlayblack()
			lightArray = []
			lightArray.append(self.chef)
			lightArray.extend(self.enemies)
			lightArray.extend(self.structures)
			lightArray.extend(self.emitters)
			if self.boss is not None and not self.boss.dead:
				lightArray.extend(self.boss.projectiles)
				lightArray.append(self.boss)
			lightArray.extend(self.chef.projectiles)

			for lightSource in lightArray:
				lightSource.renderLight(driver.renderer, self.xMin, self.yMin)



		#render in messages LAST
		for pantry in self.structures:
			if pantry.getVisible():
				pantry.renderMessage(driver.renderer, self.xMin, self.yMin)

		if self.chef.getEnergy() == 0:
			self.chef.renderEnergyMessage(driver.renderer, self.xMin, self.yMin)

		if self.level is 1 and len(self.chef.weapons) is 0:
			self.chef.renderNoWepMessage(driver.renderer, self.xMin, self.yMin)

		if self.level is not 6:
			driver.scoreBoard.renderScore(driver.renderer)
			self.chef.renderHealth(driver.renderer)
			self.chef.renderEnergy(driver.renderer, self.top)
			if len(self.chef.items) is not 0:
				self.chef.renderItems(driver.renderer)
			if len(self.chef.weapons) is not 0:
				self.chef.renderWeapons(driver.renderer)
		else:
			self.chef.renderHealthPvp(driver.renderer)
			self.chef2.renderHealthPvp(driver.renderer)

                # displaying the ranged weapon arrows ##### NOT A THING FOR NOW JUST IGNORE
		#if self.chef.degreePress or globalTime < self.chef.updateDegreeTime + 250:
		#		xDiff = 400 - (int(self.chef.xPos) - int(self.xMin)) - int(self.chef.width / 2)
		#		yDiff = 300 - (int(self.chef.yPos) - int(self.yMin)) - int(self.chef.height / 2)
		#		tileRect = sdl.Rect((240 - xDiff, 140 - yDiff, 320, 320))
		#		#sdl.renderCopy(driver.renderer, self.chef.textures[2][13], None, tileRect)
		#		sdl.renderCopyEx(driver.renderer, self.chef.textures[2][13], None, tileRect, math.degrees(self.chef.degree) + 90, sdl.Point((tileRect.w//2, tileRect.h//2)), sdl.FLIP_NONE)

		if self.level is 6:
			for object in self.objects:
				if object.title is 'blackScreen':
					object.renderSelf(currentTime, driver.renderer, self.xMin, self.yMin)


		self.xMin = oldxMin
		self.yMin = oldyMin
