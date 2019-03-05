import sys
sys.path.insert(0, '/../')
sys.path.insert(0, '/../entities/')
import driver
import sdl
import game
from basicState import BasicState
import MCClass as MC
from mouseBox import MouseBox

class MenuScreen(BasicState):
  def __init__(self):
                self.next = None

  def load(self):

                background = sdl.image.load("graphics/states/menu.png")
                global textureBG
                textureBG = driver.renderer.createTextureFromSurface(background)
                sdl.freeSurface(background)

                cursor = sdl.image.load("graphics/sprites/chef_idle_stroke.png")
                global cursorTexture
                cursorTexture = driver.renderer.createTextureFromSurface(cursor)
                sdl.freeSurface(cursor)

                global music
                music = sdl.mixer.loadMUS("music/songs/menu_screen.mod")
                global scrollSound, selectSound
                sdl.mixer.allocateChannels(2)
                scrollSound = sdl.mixer.loadWAV_RW(sdl.RWFromFile("music//chunks/menu_scroll.wav", 'rw'), 0)
                selectSound = sdl.mixer.loadWAV_RW(sdl.RWFromFile("music//chunks/menu_select.wav", 'rw'), 0)
                global boxes
                boxes = []
                boxes.append(MouseBox(245,160,260,60, 'levelZero', 0))
                boxes.append(MouseBox(245, 280, 260, 60, 'highScore', 1))
                boxes.append(MouseBox(245, 340, 260, 60, 'options', 2))
                boxes.append(MouseBox(245, 400, 260, 60, 'controls', 3))
                boxes.append(MouseBox(245, 460, 260, 60, 'quit', 4))

  def cleanup(self):
      if textureBG is not None:
        sdl.destroyTexture(textureBG)
      if cursorTexture is not None:
        sdl.destroyTexture(cursorTexture)
      if scrollSound is not None:
        sdl.mixer.freeChunk(scrollSound)
      if selectSound is not None:
        sdl.mixer.freeChunk(selectSound)
      if music is not None:
        sdl.mixer.freeMusic(music)



  def run(self):
                sdl.mixer.volume(-1, driver.volume)
                sdl.mixer.volumeMusic(driver.volume)
                sdl.mixer.playMusic(music, -1)
                cursor1 = MC.Chef(240, 160, 50, 80, 'none', 0, 0, 0, 0.001, 0.001, cursorTexture, True, 0, 0, 100, True, 1)
                cursor2 = MC.Chef(515, 160, 50, 80, 'none', 0, 0, 0, 0.001, 0.001, cursorTexture, True, 0, 0, 100, True, 1)


                running = True
                currentTime = 0
                lastTime = 0
                time = 0

                cursorPos = 0
                clicked = None

                event = sdl.Event()
                while running:
                        hover = None
	#### TIME MANAGEMENT ####
                        currentTime = sdl.getTicks()
                        dt = currentTime - lastTime
                        time += dt
                        lastTime = currentTime

	#### TEXTURE MEASUREMENTS ####
                        textureW, textureH = game.textureSize(textureBG)
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
                          elif event.type == sdl.MOUSEMOTION:
                              for i in range(len(boxes)):
                                  if (boxes[i].checkMotion(event.motion.x, event.motion.y)):
                                      hover = boxes[i].cursorPos
                          elif event.type == sdl.KEYDOWN:
                            if event.key.keysym.sym == sdl.K_UP:
                              sdl.mixer.playChannel(1, scrollSound, 0)
                              cursorPos -= 1
                              if cursorPos <= -1:
                                cursorPos = 4
                            elif event.key.keysym.sym == sdl.K_DOWN:
                              sdl.mixer.playChannel(1, scrollSound, 0)
                              cursorPos = (cursorPos + 1) % 5
                            elif event.key.keysym.sym == sdl.K_RETURN:
                              if (cursorPos == 0):
# Call to play game
                                sdl.mixer.playChannel(0, selectSound, 0)
                                running = False
                                self.next = "levelZero"
                              elif (cursorPos == 1):
# call to leaderboard
                                sdl.mixer.playChannel(0, selectSound, 0)
                                self.next = "highScore"
                                running = False
                              elif (cursorPos == 2):
#ADD IN OPTIONS
                                sdl.mixer.playChannel(0, selectSound, 0)
                                self.next = "options"
                                running = False
                              elif (cursorPos == 3):
#Call to controls screen
                                sdl.mixer.playChannel(0, selectSound, 0)
                                running = False
                                self.next = "controls"
                              elif (cursorPos == 4):
# Call to quit
                                sdl.mixer.playChannel(0, selectSound, 0)
                                running = False
                                game.turnOff()
                              while (sdl.getTicks() - currentTime < 300):
                                pass


	#### RENDER ####
                        sdl.renderClear(driver.renderer)
                        sdl.renderCopy(driver.renderer, textureBG, None, textureRect)
                        if (clicked is not None):
                            if clicked is 'quit':
                                running = False
                                game.turnOff()
                            else:
                                running = False
                                self.next = clicked

                        if (hover is not None):
                            cursorPos = hover

                        cursor1.updateY(180 + 60 * cursorPos)
                        cursor2.updateY(180 + 60 * cursorPos)
                        # render cursor in
                        time1 = ((int(time / 125)) % 4)
                        time2 = ((int(time / 500)) % 4)
                        # the rectangle that defines which sprite part the sprites
                        spriteFrame = sdl.Rect((time1 * 48, 0, 48, 80))
                        spriteFrame2 = sdl.Rect((time2 * 48, 0, 48, 80))
                        sdl.renderCopy(driver.renderer, cursorTexture, spriteFrame2, cursor1.getRect(0,0))
                        sdl.renderCopy(driver.renderer, cursorTexture, spriteFrame2, cursor2.getRect(0,0))

                        sdl.renderPresent(driver.renderer)
