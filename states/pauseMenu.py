import sys
sys.path.insert(0, '/../')
sys.path.insert(0, '/../entities/')
import driver
import sdl
import game
from basicState import BasicState
import MCClass as MC
from controlScreen import Controls
from options import Options
from mouseBox import MouseBox

class Pause(BasicState):
    def __init__(self, camera):
        self.camera = camera

    def load(self):
        pauseImage = sdl.image.load("graphics/states/pause_menu.png")
        cursor = sdl.image.load("graphics/sprites/chef_idle_stroke.png")

        global pauseTexture
        pauseTexture = driver.renderer.createTextureFromSurface(pauseImage)
        sdl.freeSurface(pauseImage)

        global cursorTexture
        cursorTexture = driver.renderer.createTextureFromSurface(cursor)
        sdl.freeSurface(cursor)

        global scrollSound, selectSound
        sdl.mixer.allocateChannels(2)
        scrollSound = sdl.mixer.loadWAV_RW(sdl.RWFromFile("music//chunks/menu_scroll.wav", 'rw'), 0)
        selectSound = sdl.mixer.loadWAV_RW(sdl.RWFromFile("music//chunks/menu_select.wav", 'rw'), 0)

        global boxes
        boxes = []
        boxes.append(MouseBox(245, 220, 260, 60, 'resume', 0))
        boxes.append(MouseBox(245, 280, 320, 60, 'options', 1))
        boxes.append(MouseBox(245, 340, 260, 60, 'controls', 2))
        boxes.append(MouseBox(245, 400, 260, 60, 'quit', 3))


    def run(self):
        sdl.mixer.volume(-1, driver.volume)
        sdl.mixer.volumeMusic(driver.volume)
        cursor1 = MC.Chef(240, 160, 50, 80, 'none', 0, 0, 0, 0.001, 0.001, cursorTexture, True, 0, 0, 100, True, 1)
        cursor2 = MC.Chef(515, 160, 50, 80, 'none', 0, 0, 0, 0.001, 0.001, cursorTexture, True, 0, 0, 100, True, 1)


        running = True
        currentTime = 0
        lastTime = 0
        time = 0

        cursorPos = 0

        keepOnPlaying = True

        event = sdl.Event()
        controls = Controls()
        options = Options()
        while running:
            hover = None
            clicked = None
#### TIME MANAGEMENT ####
            currentTime = sdl.getTicks()
            dt = currentTime - lastTime
            time += dt
            lastTime = currentTime

#### TEXTURE MEASUREMENTS ####
            textureW, textureH = game.textureSize(pauseTexture)
            textureRect = game.centeredRect(game.width, game.height, textureW, textureH)

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
                elif event.type == sdl.MOUSEBUTTONDOWN:
                    if event.button.button == sdl.BUTTON_LEFT:
                        for i in range(len(boxes)):
                            if clicked is None:
                                sdl.mixer.playChannel(0, selectSound, 0)
                                clicked = boxes[i].checkEvent(event.motion.x, event.motion.y)
                elif event.type == sdl.MOUSEMOTION:
                    for i in range(len(boxes)):
                        if (boxes[i].checkMotion(event.motion.x, event.motion.y)):
                            hover = boxes[i].cursorPos
                elif event.type == sdl.KEYDOWN:
                    if event.key.keysym.sym == sdl.K_UP:
                        sdl.mixer.playChannel(1, scrollSound, 0)
                        cursorPos -= 1
                        if cursorPos <= -1:
                            cursorPos = 3
                    elif event.key.keysym.sym == sdl.K_DOWN:
                        sdl.mixer.playChannel(1, scrollSound, 0)
                        cursorPos = (cursorPos + 1) % 4
                    elif event.key.keysym.sym == sdl.K_p:
                        sdl.mixer.playChannel(0, selectSound, 0)
                        running = False
                        keepOnPlaying = True
                    elif event.key.keysym.sym == sdl.K_RETURN:
                        if (cursorPos == 0):
    # Call to play game
                            sdl.mixer.playChannel(0, selectSound, 0)
                            running = False
                            keepOnPlaying = True
                        elif (cursorPos == 1):
    #ADD IN OPTIONS
                            sdl.mixer.playChannel(0, selectSound, 0)
                            options.load()
                            options.run()
                            options.cleanup()
                        elif (cursorPos == 2):
    #Call to controls screen
                            sdl.mixer.playChannel(0, selectSound, 0)
                            controls.load()
                            controls.run()
                            controls.cleanup()
                        elif (cursorPos == 3):
    # Call to quit
                            sdl.mixer.playChannel(0, selectSound, 0)
                            running = False
                            game.turnOff()
                            keepOnPlaying = False
                        while (sdl.getTicks() - currentTime < 300):
                            pass


#### RENDER ####
                if (clicked is not None):
                    if clicked is 'quit':
                        running = False
                        game.turnOff()
                        keepOnPlaying = False
                    elif clicked is "controls":
                        controls.load()
                        controls.run()
                        controls.cleanup()
                    elif clicked is "options":
                        options.load()
                        options.run()
                        options.cleanup()
                    elif clicked is "resume":
                        running = False
                        keepOnPlaying = True

                if (hover is not None):
                    cursorPos = hover

                cursor1.updateY(220 + 60 * cursorPos)
                cursor2.updateY(220 + 60 * cursorPos)
                sdl.renderClear(driver.renderer)
                self.camera.display(time, dt,False, None)
                sdl.renderCopy(driver.renderer, pauseTexture, None, textureRect)

                # render cursor in
                time1 = ((int(time / 125)) % 4)
                time2 = ((int(time / 500)) % 4)
                # the rectangle that defines which sprite part the sprites

                spriteFrame = sdl.Rect((time1 * 48, 0, 48, 80))
                spriteFrame2 = sdl.Rect((time2 * 48, 0, 48, 80))
                sdl.renderCopy(driver.renderer, cursorTexture, spriteFrame2, cursor1.getRect(0,0))
                sdl.renderCopy(driver.renderer, cursorTexture, spriteFrame2, cursor2.getRect(0,0))

                sdl.renderPresent(driver.renderer)
                if not running:
                    return keepOnPlaying


    def cleanup(self):
        sdl.renderClear(driver.renderer)
        if pauseTexture is not None:
            sdl.destroyTexture(pauseTexture)
        if cursorTexture is not None:
            sdl.destroyTexture(cursorTexture)
        if scrollSound is not None:
            sdl.mixer.freeChunk(scrollSound)
        if selectSound is not None:
            sdl.mixer.freeChunk(selectSound)
