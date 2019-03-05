import sys
sys.path.insert(0, '/../')
import game
import driver
import sdl
from basicState import BasicState
import os;

class HighScore(BasicState):
	def __init__(self):
		self.next = None

	def load(self):
		global lines
		global newHigh
		global fh
		cur = driver.scoreBoard.getScore()
		newHigh = False
		if os.path.lexists("highScores.txt"):
			fh = open("highScores.txt", "r+")
			lines = fh.readlines()
			newHigh = False
			counter = 0
			for stri in lines:
				if cur > int(stri):
					newHigh = True
					break
				counter += 1
		else:
			fh = open("highScores.txt", "w+")
			if cur is not 0: newHigh = True
			counter = 0
			lines = ["0", "0", "0", "0", "0"]
			for stri in lines:
				fh.write(stri + "\n")

		highScoreString = ""
		if newHigh:
			fh.seek(0)
			fh.truncate()
			highScoreString = "New High Score!  \n"
			newCount = 0
			for stri in lines:
				if newCount == counter and counter < 3:
					fh.write(str(cur) + "\n")
					highScoreString += str(cur) + "\n"
					highScoreString += stri + "\n"
					fh.write(stri)
				elif newCount is not 4:
					highScoreString += stri + "\n"
					fh.write(stri)
				newCount += 1
		else:
			for stri in lines:
				highScoreString += stri + "\n"

		fh.close()

		highScore = sdl.ttf.renderText_Blended_Wrapped(driver.scoreFont, highScoreString,
			 sdl.Color((255,255,255)).cdata[0], (300))
		background = sdl.image.load("graphics/states/leaderboard.png")
		global highScoreTexture, backgroundTexture
		backgroundTexture = driver.renderer.createTextureFromSurface(background)
		highScoreTexture = driver.renderer.createTextureFromSurface(highScore)
		sdl.freeSurface(highScore)
		sdl.freeSurface(background)
		driver.scoreBoard.clearScore()

	def run(self):
		running = True
		currentTime = 0
		lastTime = 0
		time = 0

		event = sdl.Event()

		while running:
			currentTime = sdl.getTicks()
			dt = currentTime - lastTime
			time += dt
			lastTime = currentTime

			textureW, textureH = game.textureSize(highScoreTexture)
			goRect = game.centeredRect( 200 + game.width, 30 + game.height, textureW, textureH)

			textureW, textureH = game.textureSize(backgroundTexture)
			backgroundRect = game.centeredRect(game.width, game.height, textureW, textureH)

			sdl.renderClear(driver.renderer)

			sdl.renderCopy(driver.renderer, backgroundTexture, None, backgroundRect)
			if time <= 3000:
				alpha = int(round((time/ 3000.0) * 255))
				sdl.renderCopy(driver.renderer, highScoreTexture, None, goRect)
				while sdl.pollEvent(event):
					if event.type == sdl.MOUSEBUTTONDOWN:
						running = False
						self.next = "menu"
					if event.key.keysym.sym in [sdl.K_q, sdl.K_ESCAPE]:
						running = False
						game.turnOff()
			else:
				sdl.renderCopy(driver.renderer, highScoreTexture, None, goRect)
				while sdl.pollEvent(event):
					if event.type == sdl.MOUSEBUTTONDOWN:
						running = False
						self.next = "menu"
					if event.type == sdl.KEYDOWN:
						if event.key.keysym.sym in [sdl.K_q, sdl.K_ESCAPE]:
							running = False
							game.turnOff()
						else:
							running = False
							self.next = "menu"
			sdl.renderPresent(driver.renderer)

	def cleanup(self):
		if highScoreTexture is not None:
			sdl.destroyTexture(highScoreTexture)
