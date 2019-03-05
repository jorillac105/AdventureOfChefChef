import sys
sys.path.insert(0, '/../')
import driver
import sdl
import game
from basicState import BasicState

class TitleScreen(BasicState):
	def __init__(self):
		self.next = None

	def load(self):
		global fade, full
		fade = driver.renderer.createTextureFromSurface(sdl.image.load("graphics/colors/black.png"))
		full = driver.renderer.createTextureFromSurface(sdl.image.load("graphics/states/title_full.png"))


	def cleanup(self):
		if fade is not None:
			sdl.destroyTexture(fade)
		if full is not None:
			sdl.destroyTexture(full)



	def run(self):
		running = True
		currentTime = 0
		lastTime = 0
		time = 0

		event = sdl.Event()
		textureW, textureH = game.textureSize(full)
		textureRect = game.centeredRect(game.width, game.height, textureW, textureH)
		sdl.setTextureBlendMode(full, sdl.BLENDMODE_ADD)

		while running:
			currentTime = sdl.getTicks()
			dt = currentTime - lastTime
			time += dt
			lastTime = currentTime

			if time <= 3000:
				sdl.renderClear(driver.renderer)
				alpha = int(round((time/ 3000.0) * 255))
				if alpha > 255:
					time += 3000
					alpha = 255
				sdl.renderCopy(driver.renderer, fade, None, textureRect)
				sdl.setTextureAlphaMod(full, alpha)
				sdl.renderCopy(driver.renderer, full, None, textureRect)
				while sdl.pollEvent(event):
					if event.type == sdl.KEYDOWN:
						time += 3000
					elif event.type == sdl.MOUSEBUTTONDOWN: time += 3000
					if event.key.keysym.sym in [sdl.K_q, sdl.K_ESCAPE]:
						running = False
						game.turnOff()
			else:
				sdl.renderCopy(driver.renderer, fade, None, textureRect)
				sdl.renderCopy(driver.renderer, full, None, textureRect)
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
