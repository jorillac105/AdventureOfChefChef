import sys
sys.path.insert(0, '/../entities/')
sys.path.insert(0, '/../')
from basicState import BasicState
import sdl
import driver
import game

class LoadingScreen(BasicState):

	def load(self):
		loadingImage = sdl.image.load("graphics/states/loadingScreen.png")
		global loadingTexture 
		loadingTexture = driver.renderer.createTextureFromSurface(loadingImage)
		sdl.freeSurface(loadingImage)

	def run(self):
		sdl.renderClear(driver.renderer)

		textureW, textureH = game.textureSize(loadingTexture)
		textureRect = game.centeredRect(game.width, game.height, textureW, textureH)
		sdl.renderCopy(driver.renderer, loadingTexture, None, textureRect)
		sdl.renderPresent(driver.renderer)

	def cleanup(self):
		sdl.destroyTexture(loadingTexture)
