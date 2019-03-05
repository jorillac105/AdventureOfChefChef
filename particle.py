import sdl
import math

class Particle():

	def __init__(self, typeOf, halfLife, xPos, yPos, direction, speed):
		self.origX = xPos
		self.origY = yPos
		self.xPos = xPos
		self.yPos = yPos
		self.life = halfLife
		self.direction = direction
		self.speed = speed * 3

	def isAlive(self):
		dist = math.sqrt((self.xPos - self.origX)**2 + (self.yPos - self.origY)**2)
		if self.life <= 0:
			return False
		elif dist > 150:
			return False 
		else:
			return True

	def update(self, dt):
		rads = math.radians(self.direction)
		self.xPos += round(self.speed * (math.cos(rads)) * dt)
		self.yPos += round(self.speed * (math.sin(rads)) * dt)
		self.life -= abs(dt)

	def getTimeFraction(self):
		return self.life // 100 + 1