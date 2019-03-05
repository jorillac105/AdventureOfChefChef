import sys
sys.path.insert(0, '/../entities/')
sys.path.insert(0, '/../')
from basicState import BasicState
import sdl
import driver
import game

class Story(BasicState):
	def __init__(self, num):
		self.num = num
		self.textures = []
		self.length = 0
		self.alpha = 255.0

	def load(self):
		images = []
		if self.num is 1:
			images.append(sdl.image.load("graphics/story/intro_0.png"))
			images.append(sdl.image.load("graphics/story/intro_1.png"))
			images.append(sdl.image.load("graphics/story/intro_2.png"))
			images.append(sdl.image.load("graphics/story/intro_3.png"))
			images.append(sdl.image.load("graphics/states/level1.png"))
		elif self.num is 2:
			images.append(sdl.image.load("graphics/story/basement_0.png"))
			images.append(sdl.image.load("graphics/story/basement_1.png"))
		elif self.num is 3:
			images.append(sdl.image.load("graphics/states/level2.png"))
		elif self.num is 4:
			images.append(sdl.image.load("graphics/story/miniboss_0.png"))
			images.append(sdl.image.load("graphics/story/miniboss_1.png"))
		elif self.num is 5:
			images.append(sdl.image.load("graphics/states/level3.png"))
		elif self.num is 6:
			for x in range(0, 8):
				images.append(sdl.image.load('graphics/story/boss_' + str(x) + '.png'))
		elif self.num is 7:
			images.append(sdl.image.load("graphics/story/you_won.png"))
			images.append(sdl.image.load("graphics/states/credits.png"))
			global blackScreen
			blackScreen = driver.renderer.createTextureFromSurface(sdl.image.load('graphics/colors/black.png'))
			sdl.setTextureBlendMode(blackScreen,sdl.BLENDMODE_BLEND)
		self.length = len(images)
		for x in range(len(images)):
			self.textures.append(driver.renderer.createTextureFromSurface(images[x]))
			sdl.freeSurface(images[x])
		global textureRect
		textureW, textureH = game.textureSize(self.textures[0])
		textureRect = game.centeredRect(game.width, game.height, textureW, textureH)

	#def transition6(self):
	def updateAlpha(self):
		if self.alpha > 0:
			self.alpha -= .2
		elif self.alpha <= 0:
			self.alpha = 0

	def run(self):
		running = True
		count = 0
		event = sdl.Event()
		#if self.num is 7:
		while running:
			sdl.renderClear(driver.renderer)
			sdl.renderCopy(driver.renderer, self.textures[count], None, textureRect)

			if count ==  0 and self.num is 7:
				self.updateAlpha()
				sdl.setTextureAlphaMod(blackScreen, int(self.alpha))
				sdl.renderCopy(driver.renderer, blackScreen, None, textureRect)

			while sdl.pollEvent(event):
				if event.type == sdl.QUIT:
				 	running = False
				 	game.turnOff()
				elif event.type == sdl.MOUSEBUTTONDOWN: count += 1
				elif event.type == sdl.KEYUP:
					if event.key.keysym.sym in [sdl.K_q, sdl.K_ESCAPE]:
						running = False
						game.turnOff()
					elif event.key.keysym.sym == sdl.K_RETURN:  count += 100
					elif (count < self.length - 1 or self.num is 2 or self.num is 4 or self.num is 6 or self.num is 7) and event.key.keysym.sym == sdl.K_SPACE: count += 1

			if count > self.length - 1:
				running = False
			sdl.renderPresent(driver.renderer)

	def cleanup(self):
		for x in range(len(self.textures)):
			sdl.destroyTexture(self.textures[x])
