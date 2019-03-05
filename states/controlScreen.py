import sys
sys.path.insert(0, '/../')
import game
import driver
import sdl
from basicState import BasicState

class Controls(BasicState):
	def __init__(self):
		self.next = None

	def load(self):
		background = sdl.image.load("graphics/states/controls.png")
		global backgroundTexture
		backgroundTexture = driver.renderer.createTextureFromSurface(background)
		sdl.freeSurface(background)

	def run(self):
		running = True
		currentTime = 0
		lastTime = 0
		time = 0

		event = sdl.Event()
		while running:
			sdl.renderClear(driver.renderer)
			textureW, textureH = game.textureSize(backgroundTexture)
			backgroundRect = game.centeredRect(game.width, game.height, textureW, textureH)
			sdl.renderCopy(driver.renderer, backgroundTexture, None, backgroundRect)
			while sdl.pollEvent(event):
				if event.type == sdl.MOUSEBUTTONDOWN:
					running = False
					self.next = "menu"
				elif event.type == sdl.KEYDOWN:
					if event.key.keysym.sym in [sdl.K_q, sdl.K_ESCAPE]:
						running = False
						game.turnOff()
					elif event.key.keysym.sym in [sdl.K_SPACE, sdl.K_RETURN]:
						running = False
						self.next = "menu"
			sdl.renderPresent(driver.renderer)

	def cleanup(self):
		if backgroundTexture is not None:
			sdl.destroyTexture(backgroundTexture)
