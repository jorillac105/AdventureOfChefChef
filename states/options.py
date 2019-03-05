import sys
sys.path.insert(0, '/../')
sys.path.insert(0, '/../entities/')
import driver
import sdl
import game
from basicState import BasicState
import MCClass as MC
from mouseBox import MouseBox

class Options(BasicState):
    def __init__(self):
        self.next = None

    def load(self):
        pauseImage = sdl.image.load("graphics/states/options.png")
        cursor = sdl.image.load("graphics/sprites/chef_idle_stroke.png")
        blueImage = sdl.image.load("graphics/states/options_indicator.png")

        global optionsTexture
        optionsTexture = driver.renderer.createTextureFromSurface(pauseImage)
        sdl.freeSurface(pauseImage)

        global cursorTexture
        cursorTexture = driver.renderer.createTextureFromSurface(cursor)
        sdl.freeSurface(cursor)

        global indTexture
        indTexture = driver.renderer.createTextureFromSurface(blueImage)
        sdl.free(blueImage)

        global scrollSound, selectSound
        sdl.mixer.allocateChannels(2)
        scrollSound = sdl.mixer.loadWAV_RW(sdl.RWFromFile("music//chunks/menu_scroll.wav", 'rw'), 0)
        selectSound = sdl.mixer.loadWAV_RW(sdl.RWFromFile("music//chunks/menu_select.wav", 'rw'), 0)

        global boxes
        boxes = []
        boxes.append(MouseBox(225,190,260,115, 'levelZero', 0))
        boxes.append(MouseBox(225, 305, 305, 115, 'pvp', 1))
        boxes.append(MouseBox(225, 420, 305, 115, 'highScore', 2))

        global volumeBoxes
        volumeBoxes = []
        for x in range(10):
            volumeBoxes.append(MouseBox(280 + 25*x, 242, 18, 18, x + 1, x + 1))



    def run(self):
        cursor1 = MC.Chef(220, 190, 50, 80, 'none', 0, 0, 0, 0.001, 0.001, cursorTexture, True, 0, 0, 100, True, 1)
        cursor2 = MC.Chef(535, 190, 50, 80, 'none', 0, 0, 0, 0.001, 0.001, cursorTexture, True, 0, 0, 100, True, 1)


        running = True
        currentTime = 0
        lastTime = 0
        time = 0

        cursorPos = 0
        brightnessPos = 10
        volumePos = round((driver.volume - 8) / 12)

        event = sdl.Event()

        textureW, textureH = game.textureSize(optionsTexture)
        textureRect = game.centeredRect(game.width, game.height, textureW, textureH)
        sdl.renderClear(driver.renderer)
        sdl.renderCopy(driver.renderer, optionsTexture, None, textureRect)

        # render cursor in
        time1 = ((int(time / 125)) % 4)
        time2 = ((int(time / 500)) % 4)
        # the rectangle that defines which sprite part the sprites
        spriteFrame = sdl.Rect((time1 * 48, 0, 48, 80))
        spriteFrame2 = sdl.Rect((time2 * 48, 0, 48, 80))
        sdl.renderCopy(driver.renderer, cursorTexture, spriteFrame2, cursor1.getRect(0,0))
        sdl.renderCopy(driver.renderer, cursorTexture, spriteFrame2, cursor2.getRect(0,0))

        #render in brightness indicators
        for i in range(brightnessPos):
            spot = sdl.Rect((280 + 25 * i, 357, 18, 18))
            sdl.renderCopy(driver.renderer, indTexture, None, spot)

        #render in volume indicators
        for i in range(volumePos):
            spot = sdl.Rect((280 + 25 * i, 242, 18, 18))
            sdl.renderCopy(driver.renderer, indTexture, None, spot)

        sdl.renderPresent(driver.renderer)

        while running:
            hover = None
            clicked = None
#### TIME MANAGEMENT ####
            currentTime = sdl.getTicks()
            dt = currentTime - lastTime
            time += dt
            lastTime = currentTime

#### TEXTURE MEASUREMENTS ####
            textureW, textureH = game.textureSize(optionsTexture)
            textureRect = game.centeredRect(game.width, game.height, textureW, textureH)

#### HANDLE INPUT ####
            while sdl.pollEvent(event):
                if event.type == sdl.QUIT:
                    running = False
                    game.turnOff()
                elif event.type == sdl.KEYUP:
                    if event.key.keysym.sym in [sdl.K_q, sdl.K_ESCAPE]:
                        running = False
                        game.turnOff()
                elif event.type == sdl.MOUSEBUTTONDOWN:
                    if event.button.button == sdl.BUTTON_LEFT:
                        for i in range(len(boxes)):
                            if clicked is None:
                                sdl.mixer.playChannel(0, selectSound, 0)
                                clicked = boxes[i].checkEvent(event.motion.x, event.motion.y)
                        for i in range(len(volumeBoxes)):
                            here = volumeBoxes[i].checkEvent(event.motion.x, event.motion.y)
                            if here is not None:
                                volumePos = here
                elif event.type == sdl.MOUSEMOTION:
                    for i in range(len(boxes)):
                        if (boxes[i].checkMotion(event.motion.x, event.motion.y)):
                            hover = boxes[i].cursorPos
                if event.type == sdl.KEYDOWN:
                    if event.key.keysym.sym == sdl.K_UP:
                        sdl.mixer.playChannel(1, scrollSound, 0)
                        cursorPos -= 1
                        if cursorPos <= -1:
                            cursorPos = 2
                    elif event.key.keysym.sym == sdl.K_DOWN:
                        sdl.mixer.playChannel(1, scrollSound, 0)
                        cursorPos = (cursorPos + 1) % 3
                    elif event.key.keysym.sym == sdl.K_RIGHT:
                        sdl.mixer.playChannel(1, scrollSound, 0)
                        if cursorPos is 1:
                            if sdl.getWindowBrightness(driver.window) < 1:
                                brightnessPos += 1
                                sdl.setWindowBrightness(driver.window,
                                    sdl.getWindowBrightness(driver.window)+ 0.05)
                        elif cursorPos is 0:
                            if volumePos < 10:
                                volumePos += 1
                                sdl.mixer.volume(-1, volumePos * 12)
                                driver.volume = volumePos * 12
                    elif event.key.keysym.sym == sdl.K_LEFT:
                        sdl.mixer.playChannel(1, scrollSound, 0)
                        if cursorPos is 1:
                            if sdl.getWindowBrightness(driver.window) > .5:
                                brightnessPos -= 1
                                sdl.setWindowBrightness(driver.window,
                                    sdl.getWindowBrightness(driver.window) - 0.05)
                        elif cursorPos is 0:
                            if volumePos > 1:
                                volumePos -= 1
                                sdl.mixer.volume(-1, volumePos * 12)
                                driver.volume = volumePos * 12
                    elif event.key.keysym.sym == sdl.K_RETURN:
                        if (cursorPos == 0):
    # Call to play game
                            sdl.mixer.playChannel(1, scrollSound, 0)
                        elif (cursorPos == 1):
    #ADD IN OPTIONS
                            sdl.mixer.playChannel(1, scrollSound, 0)
                        elif (cursorPos == 2):
    #Call to controls screen
                            sdl.mixer.playChannel(0, selectSound, 0)
                            running = False
                            self.next = "menu"
                        while (sdl.getTicks() - currentTime < 300):
                            pass

                if (hover is not None):
                    cursorPos = hover

                if clicked is not None:
                    if cursorPos is 2:
                        sdl.mixer.playChannel(0, selectSound, 0)
                        running = False
                        self.next = "menu"
                cursor1.updateY(190 + 115 * cursorPos)
                cursor2.updateY(190 + 115 * cursorPos)

#### RENDER ####
                sdl.renderClear(driver.renderer)
                sdl.renderCopy(driver.renderer, optionsTexture, None, textureRect)

                # render cursor in
                time1 = ((int(time / 125)) % 4)
                time2 = ((int(time / 500)) % 4)
                # the rectangle that defines which sprite part the sprites
                spriteFrame = sdl.Rect((time1 * 48, 0, 48, 80))
                spriteFrame2 = sdl.Rect((time2 * 48, 0, 48, 80))
                sdl.renderCopy(driver.renderer, cursorTexture, spriteFrame2, cursor1.getRect(0,0))
                sdl.renderCopy(driver.renderer, cursorTexture, spriteFrame2, cursor2.getRect(0,0))

                for i in range(brightnessPos):
                    spot = sdl.Rect((280 + 25 * i, 357, 18, 18))
                    sdl.renderCopy(driver.renderer, indTexture, None, spot)
                for i in range(volumePos):
                    spot = sdl.Rect((280 + 25 * i, 242, 18, 18))
                    sdl.renderCopy(driver.renderer, indTexture, None, spot)
                sdl.renderPresent(driver.renderer)


    def cleanup(self):
        sdl.renderClear(driver.renderer)
        if optionsTexture is not None:
            sdl.destroyTexture(optionsTexture)
        if cursorTexture is not None:
            sdl.destroyTexture(cursorTexture)
        if scrollSound is not None:
            sdl.mixer.freeChunk(scrollSound)
        if selectSound is not None:
            sdl.mixer.freeChunk(selectSound)
        if indTexture is not None:
            sdl.destroyTexture(indTexture)
