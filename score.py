import game
import sdl
import driver

class Score():
	def __init__(self):
		self.totalScore = 0

	def setScore(self, num):
		self.totalScore = num

	def updateScore(self, num):
		self.totalScore += num

	def renderScore(self, renderer):
		stringScore = "Score: " + str(self.totalScore)
		score = sdl.ttf.renderText_Solid(driver.scoreFont, stringScore,
			 sdl.Color((255,255,255)).cdata[0])
		scoreTexture = renderer.createTextureFromSurface(score)
		textureW, textureH = game.textureSize(scoreTexture)
		scoreRect = game.centeredRect(game.width, 60, textureW, textureH)
		sdl.renderCopy(renderer, scoreTexture, None, scoreRect)
		sdl.freeSurface(score)
		sdl.destroyTexture(scoreTexture)

	def getScore(self):
		return self.totalScore

	def clearScore(self):
		self.totalScore = 0
