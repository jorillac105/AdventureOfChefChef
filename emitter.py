import driver
import sdl
import random
from particle import Particle

class Emitter():

	def __init__(self, xPos, yPos, typeOf, number, lifeTime):
		self.xPos = xPos
		self.yPos = yPos
		self.type = typeOf
		self.num = number
		self.particles = []
		self.lifeTime = lifeTime
		if self.type is "rat":
			self.tex = sdl.createTextureFromSurface(driver.renderer, sdl.image.load("graphics/colors/red.png"))
		elif self.type is "explosion":
			self.tex1 = sdl.createTextureFromSurface(driver.renderer, sdl.image.load("graphics/colors/red.png"))
			self.tex2 = sdl.createTextureFromSurface(driver.renderer, sdl.image.load("graphics/colors/orange.png"))
			self.tex3 = sdl.createTextureFromSurface(driver.renderer, sdl.image.load("graphics/colors/white.png"))
			self.expLight = sdl.createTextureFromSurface(driver.renderer, sdl.image.load("graphics/colors/letsGo2.png"))
			sdl.setTextureBlendMode(self.expLight, sdl.BLENDMODE_ADD)


	def emit(self):
		#figure out number
		random.seed()

		if self.type is "rat":
			halfLife = 500
		elif self.type is "explosion":
			halfLife = 1000
		for x in range(self.num):
			#find rand number
			xShift = random.randint(-10, 10)
			yShift = random.randint(-10, 10)
			#find random direction
			direction = random.randint(1, 360)
			#add particle
			self.particles.append(Particle(None, halfLife, xShift + self.xPos, yShift + self.yPos, direction, random.random()))


	def empty(self):
		if len(self.particles) is 0:
			return True
		else:
			return False

	def update(self, dt):
		for particle in self.particles:
			particle.update(dt)
			if not particle.isAlive():
				self.particles.remove(particle)
				if self.type is "rat":
					sdl.destroyTexture(self.tex)
					sdl.destroyTexture(self.expLight)
				elif self.type is "explosion":
					sdl.destroyTexture(self.tex3)
					sdl.destroyTexture(self.tex2)
					sdl.destroyTexture(self.tex1)
					sdl.destroyTexture(self.expLight)

	def getTime(self):
		return self.lifeTime

	def getCameraPos(self):
		return self.yPos

	def renderLight(self, renderer, xMin, yMin):
		for particle in self.particles:
			if self.type is "explosion":
				if not particle.isAlive():
					self.particles.remove(particle)
				else:
					expRect = sdl.Rect((0, 0, 10, 10))
					pixSize = particle.getTimeFraction()
					pixSize = (pixSize**3) // 2 
					sdl.renderCopy(renderer, self.expLight, None, sdl.Rect((int(particle.xPos) - int(xMin) - int(pixSize/2), int(particle.yPos) - int(yMin) - int(pixSize/2), int(pixSize), int(pixSize))))



	def renderSelf(self, renderer, xMin, yMin, dt): 
		for particle in self.particles:
			if self.type is "rat":
				particle.update(dt)
				if not particle.isAlive():
					self.particles.remove(particle)
				else:
					pixSize = particle.getTimeFraction()
					sdl.renderCopy(renderer, self.tex, None, sdl.Rect((int(particle.xPos) - int(xMin), int(particle.yPos) - int(yMin), pixSize, pixSize)))
			elif self.type is "explosion":
				particle.update(dt)
				if not particle.isAlive():
					self.particles.remove(particle)
				else:
					pixSize = particle.getTimeFraction()
					if particle.life > 900:
						sdl.renderCopy(renderer, self.tex3, None, sdl.Rect((int(particle.xPos) - int(xMin), int(particle.yPos) - int(yMin), pixSize, pixSize)))
					elif particle.life > 800:
						sdl.renderCopy(renderer, self.tex2, None, sdl.Rect((int(particle.xPos) - int(xMin), int(particle.yPos) - int(yMin), pixSize, pixSize)))
					elif particle.life > 0:
						sdl.renderCopy(renderer, self.tex1, None, sdl.Rect((int(particle.xPos) - int(xMin), int(particle.yPos) - int(yMin), pixSize, pixSize)))


				