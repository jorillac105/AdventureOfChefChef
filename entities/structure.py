import sdl
import game
import driver
from base import Base
import game as chef

class Structure:

	def __init__(self, val, xTile, yTile, texture, hasKey, identity):
		self.value = val
		self.identity = identity
		self.used = False
		self.visible = False
		self.triggered = False
		self.revealed = False
		self.xPos = xTile
		self.yPos = yTile
		self.height = 50
		self.width = 50
		self.texture = texture
		self.currentFrame = 0
		self.currentTime = -1 # no it's always different at first
		self.hasKey = hasKey
		self.base = Base(self.xPos, self.yPos, self.width, self.height, 0, 0) 

	def updateBase(self):
		self.base.topRight = [self.xPos + self.width - 0, self.yPos + 0]
		self.base.bottomLeft = [self.xPos + 0, self.yPos + self.height] 

	def changeVisibility(self):
		if not self.used:
			if self.visible:
				self.visible = False
			else:
				self.visible = True


	def triggerAction(self):
		self.triggered = True
		self.visible = False
		self.height = 80
		self.width = 90

	def getRect(self, xMin, yMin, xVal, xdt, yVal, ydt):
		if self.identity is "bluePipe" or self.identity is "redPipe":
			return sdl.Rect((int(50 * self.xPos) - int(xMin) , int(50 * self.yPos) - ydt - int(yMin), 50, yVal))
		else:	
			return sdl.Rect((int(50 * self.xPos) - int(xMin) - xdt , int(50 * self.yPos) - 25 - int(yMin) - ydt, xVal, yVal))

	def getMessageRect(self, num):
		textureW, textureH = game.textureSize(self.texture[num])
		return sdl.Rect((240, 500, textureW, textureH))

	def getVisible(self):
		return self.visible

	def getCameraPos(self):
		return self.yPos + self.height

	def renderSelf(self, time, renderer, xMin, yMin):
		if self.identity is "pantry":
			if self.used is False:
				if self.triggered:
					if self.hasKey:
						time1 = ((int(time / 125)) % 4) 
						if time1 is not self.currentTime: 
							self.currentFrame += 1
						spriteFrame = sdl.Rect((self.currentFrame * 90, 0, 90, 90))
						sdl.renderCopy(renderer, self.texture[0], spriteFrame, self.getRect(xMin, yMin, 90, 19, 90, 3))
						sdl.renderCopy(renderer, self.texture[4], None, self.getMessageRect(2))
						if self.currentFrame is 4:
							self.used = True
						self.currentTime = time1 
					else:
						time1 = ((int(time / 125)) % 4) 
						if time1 is not self.currentTime: 
							self.currentFrame += 1
						spriteFrame = sdl.Rect((self.currentFrame * 90, 0, 90, 90))
						sdl.renderCopy(renderer, self.texture[0], spriteFrame, self.getRect(xMin, yMin, 90, 19, 90, 3))
						if self.currentFrame is 4:
							self.used = True
						self.currentTime = time1 
			else:
				sdl.renderCopy(renderer, self.texture[1], None, self.getRect(xMin, yMin, 82, 16, 85, 0))
		elif self.identity is "bluePipe":
			if self.used is False:
				if self.triggered:
					time1 = ((int(time / 125)) % 4) 
					if time1 is not self.currentTime: 
						self.currentFrame += 1
					spriteFrame = sdl.Rect((self.currentFrame * 50, 0, 50, 70))
					sdl.renderCopy(renderer, self.texture[0], spriteFrame, self.getRect(xMin, yMin, 0, 20, 70, 20))
					if self.currentFrame is 4:
						self.used = True
					self.currentTime = time1 
			else:
				sdl.renderCopy(renderer, self.texture[2], None, self.getRect(xMin, yMin, 0, 19, 50, 0))
		elif self.identity is "redPipe":
			if self.used is False:
				if self.triggered:
					time1 = ((int(time / 125)) % 4) 
					if time1 is not self.currentTime: 
						self.currentFrame += 1
					spriteFrame = sdl.Rect((self.currentFrame * 50, 0, 50, 70))
					sdl.renderCopy(renderer, self.texture[4], spriteFrame, self.getRect(xMin, yMin,0,0, 70, 20))
					if self.currentFrame is 4:
						self.used = True
					self.currentTime = time1 
			else:
				sdl.renderCopy(renderer, self.texture[5], None, self.getRect(xMin, yMin,0,0, 50, 0))

	def renderLight(self, renderer, xMin, yMin):
		if (self.identity is "redPipe" or self.identity is "bluePipe") and self.used is False and 'carrot' in driver.chef.items:
			if self.identity is "redPipe":
				texture = driver.lightTextures[7]
			else:
				texture = driver.lightTextures[5]
			textureW = 100
			textureH = 100
			sdl.setTextureBlendMode(texture, sdl.BLENDMODE_ADD)
			sdl.setTextureAlphaMod(texture, 128)
			xP = int(self.xPos * 50) - int(xMin) + 25 - int(textureW/2)
			yP = int(self.yPos * 50) - int(yMin) + 25 - int(textureH/2)
			posRect = sdl.Rect((xP, yP, textureW, textureH))
			sdl.renderCopy(renderer, texture, None, posRect)
		else:
			return

	def renderMessage(self, renderer, xMin, yMin):
		if self.used is False:
			if self.identity is "pantry" or self.identity is "graters":
				sdl.renderCopy(renderer, self.texture[2], None, self.getMessageRect(2))
			elif self.identity is "stairs":
				sdl.renderCopy(renderer, self.texture[5], None, self.getMessageRect(5))
			elif self.identity is "bluePipe":
				sdl.renderCopy(renderer, self.texture[7], None, self.getMessageRect(7))
			elif self.identity is "redPipe":
				sdl.renderCopy(renderer, self.texture[8], None, self.getMessageRect(8))
