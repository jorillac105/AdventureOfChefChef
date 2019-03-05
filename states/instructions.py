import sys
sys.path.insert(0, '/../')
sys.path.insert(0, '/../entities/')
import driver
import sdl
import game
from basicState import BasicState

class Instruct(BasicState):
    def __init__(self, camera):
        self.camera = camera

    def run(self, itemName):
        sdl.mixer.volume(-1, driver.volume)
        sdl.mixer.volumeMusic(driver.volume)

        running = True
        currentTime = 0
        lastTime = 0
        time = 0

        keepOnPlaying = True

        event = sdl.Event()

        sdl.mixer.allocateChannels(2)
        selectSound = sdl.mixer.loadWAV_RW(sdl.RWFromFile("music//chunks/menu_select.wav", 'rw'), 0)
        cur = 0
        if itemName is "bsv":
            cur = 0
        elif itemName is "key":
            cur = 1
        elif itemName is "ladles":
            cur = 2
        elif itemName is "graters":
            cur = 3
        elif itemName is "carrot":
            cur = 4
        elif itemName is "pizza":
            cur = 5
        elif itemName is "tomato":
            cur = 6
        elif itemName is "knives":
            cur = 7

        while running:

#### TIME MANAGEMENT ####
            currentTime = sdl.getTicks()
            dt = currentTime - lastTime
            time += dt
            lastTime = currentTime

#### TEXTURE MEASUREMENTS ####
            textureW, textureH = game.textureSize(driver.chef.textures[3][cur])
            textureRect = game.centeredRect(game.width, game.height, textureW, textureH)
            sdl.renderClear(driver.renderer)
            self.camera.display(time, dt,False, None)
            sdl.renderCopy(driver.renderer, driver.chef.textures[3][cur], None, textureRect)
            sdl.renderPresent(driver.renderer)

#### HANDLE INPUT ####
            while sdl.pollEvent(event):
                if event.type == sdl.QUIT:
                    running = False
                    game.turnOff()
                    keepOnPlaying = False
                elif event.type == sdl.KEYUP:
                    if event.key.keysym.sym in [sdl.K_q, sdl.K_ESCAPE]:
                        running = False
                        game.turnOff()
                        keepOnPlaying = False
                if event.type == sdl.KEYDOWN:
                    if event.key.keysym.sym is sdl.K_SPACE:
                        sdl.mixer.playChannel(0, selectSound, 0)
                        running = False
                        keepOnPlaying = True


#### RENDER ####

                if not running:
                    return keepOnPlaying
        sdl.renderClear(driver.renderer)
        if selectSound is not None:
            sdl.mixer.freeChunk(selectSound)
