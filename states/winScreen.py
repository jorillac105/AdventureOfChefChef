import sys
sys.path.insert(0, '/../')
import game
import driver
import sdl
from basicState import BasicState

class WinScreen(BasicState):
	def __init__(self):
		self.next = None

	def load(self):
		winString = "YOU WON"
		winScreen = sdl.image.load("graphics/story/you_won.png")
		global winTexture
		winTexture = driver.renderer.createTextureFromSurface(winScreen)
		sdl.freeSurface(winScreen)
		

	def run(self):
		running = True
		currentTime = 0
		lastTime = 0
		time = 0
		pressed = False

		event = sdl.Event()

		while running:
			currentTime = sdl.getTicks()
			dt = currentTime - lastTime
			time += dt
			lastTime = currentTime

			textureW, textureH = game.textureSize(winTexture)
			goRect = game.centeredRect(game.width, game.height, textureW, textureH)

			if time <= 3000:
				sdl.renderClear(driver.renderer)
				alpha = int(round((time/ 3000.0) * 255))
				sdl.setTextureAlphaMod(winTexture, alpha)
				sdl.renderCopy(driver.renderer, winTexture, None, goRect)
				while sdl.pollEvent(event):
					if event.type == sdl.KEYDOWN:
						time += 3000
					if event.key.keysym.sym in [sdl.K_q, sdl.K_ESCAPE]:
						running = False
						game.turnOff()
			else:
				sdl.renderClear(driver.renderer)
				sdl.renderCopy(driver.renderer, winTexture, None, goRect)
				while sdl.pollEvent(event):
					if event.type == sdl.KEYDOWN:
						if event.key.keysym.sym in [sdl.K_q, sdl.K_ESCAPE]:
							running = False
							game.turnOff()
						elif event.key.keysym.sym in [sdl.K_SPACE, sdl.K_RETURN]:
							running = False
							self.next = "highScore"
			sdl.renderPresent(driver.renderer)

	def cleanup(self):
		if winTexture is not None:
			sdl.destroyTexture(winTexture)
