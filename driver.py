import sdl
import game
import rats
import MCClass as MC
import math
import random
from score import Score
from loading import LoadingScreen

off = False

def setup():
    sdl.init(sdl.INIT_VIDEO | sdl.INIT_AUDIO)
    sdl.mixer.openAudio(22050, sdl.mixer.DEFAULT_FORMAT, 2, 4096)
    sdl.ttf.init()
    global scoreFont
    scoreFont = sdl.ttf.openFont("graphics/fonts/ptsans.ttf", 24)

    global window
    window = sdl.createWindow(
        game.title,
        sdl.WINDOWPOS_UNDEFINED, sdl.WINDOWPOS_UNDEFINED,
        game.width, game.height,
        sdl.WINDOW_SHOWN,
    )

    global renderer
    renderer = sdl.createRenderer(
        window,
        -1,
        sdl.RENDERER_ACCELERATED,
    )
    global scoreBoard
    scoreBoard = Score()

    global volume
    volume = 128

    #global loading
    #loading = LoadingScreen()

    chefActionImages = [ sdl.image.load("graphics/sprites/chef_idle_new.png"), #[0][0]
                    sdl.image.load("graphics/sprites/chef_up_new.png"),
                    sdl.image.load("graphics/sprites/chef_right_new.png"),
                    sdl.image.load("graphics/sprites/chef_down_new.png"),
                    sdl.image.load("graphics/sprites/chef_left_new.png"),
                    sdl.image.load("graphics/sprites/chef_hurt_new.png"), #[0][5]
                    sdl.image.load("graphics/sprites/chef_attack_new.png"),
                    sdl.image.load("graphics/sprites/chef_attack_graters.png"),
                    sdl.image.load("graphics/sprites/chef_attack_bomb.png"),
                    sdl.image.load("graphics/sprites/chef_idle_left.png"),
                    sdl.image.load("graphics/sprites/chef_idle_right.png"),#[0][10]
                    sdl.image.load("graphics/sprites/chef_idle_up.png"),
                    sdl.image.load("graphics/sprites/chef_attack_knife.png"),
                    sdl.image.load("graphics/sprites/chef_dying.png")]

    chefItemImages =  [sdl.image.load("graphics/items/heart.png"), #0
                    sdl.image.load("graphics/items/key.png"), #1
                    sdl.image.load("graphics/items/carrot.png"), #2
                    sdl.image.load("graphics/items/ladles.png"), #3
                    sdl.image.load("graphics/items/graters.png"), #4
                    sdl.image.load("graphics/items/bomb.png"), #5
                    sdl.image.load("graphics/items/knife_small.png"),  #6
                    sdl.image.load("graphics/items/knife_medium.png"), #7
                    sdl.image.load("graphics/items/knife_large.png"), #8
                    sdl.image.load("graphics/items/knife_set.png")] #[1][9]

    chefUIImages = []
    for x in range(9):
      chefUIImages.append(sdl.image.load("graphics/ui/pizza_" + str(x) + ".png"))
    chefUIImages.append( sdl.image.load("graphics/messages/no_energy.png")) #9
    chefUIImages.append( sdl.image.load("graphics/ui/green.png")) #10
    chefUIImages.append( sdl.image.load("graphics/ui/red.png")) #11
    chefUIImages.append( sdl.image.load("graphics/ui/bomb_explosion.png")) #12
    chefUIImages.append( sdl.image.load("graphics/ui/range_arrow.png")) #13
    chefUIImages.append( sdl.image.load("graphics/messages/need_weapon.png")) #14

    chefInstructionImages = [sdl.image.load("graphics/ui/bsv_info.png"), #0
                            sdl.image.load("graphics/ui/key_info.png"),
                            sdl.image.load("graphics/ui/ladles_info.png"),
                            sdl.image.load("graphics/ui/graters_info.png"),
                            sdl.image.load("graphics/ui/carrot_info.png"),
                            sdl.image.load("graphics/ui/pizza_info.png"), #5
                            sdl.image.load("graphics/ui/tomato_info.png"),
                            sdl.image.load("graphics/ui/knives_info.png")]

    lightImages = []
    lightImages.append( sdl.image.load("graphics/colors/letsGo.png")) #0
    lightImages.append( sdl.image.load("graphics/colors/letsGo2.png")) #1
    lightImages.append( sdl.image.load("graphics/colors/letsBoom.png")) #2
    lightImages.append( sdl.image.load("graphics/colors/orangeBossGo.png")) #3
    lightImages.append( sdl.image.load("graphics/colors/purpleProjectileGo.png")) #4
    lightImages.append( sdl.image.load("graphics/colors/blueBossGo.png")) #5
    lightImages.append( sdl.image.load("graphics/colors/greenBossGo.png")) #6
    lightImages.append( sdl.image.load("graphics/colors/redBossGo.png")) #7


    global lightTextures
    lightTextures = []
    for x in range(len(lightImages)):
        lightTextures.append(renderer.createTextureFromSurface(lightImages[x]))
        sdl.freeSurface(lightImages[x])




    global chefActionTextures
    global chefItemTextures
    global chefUITextures
    global chefInstructionTextures

    chefActionTextures = []
    for x in range(len(chefActionImages)):
      chefActionTextures.append(renderer.createTextureFromSurface(chefActionImages[x]))
      sdl.freeSurface(chefActionImages[x])

    chefItemTextures = []
    for x in range(len(chefItemImages)):
      chefItemTextures.append(renderer.createTextureFromSurface(chefItemImages[x]))
      sdl.freeSurface(chefItemImages[x])

    chefUITextures = []
    for x in range(len(chefUIImages)):
      chefUITextures.append(renderer.createTextureFromSurface(chefUIImages[x]))
      sdl.freeSurface(chefUIImages[x])

    chefInstructionTextures = []
    for x in range(len(chefInstructionImages)):
      chefInstructionTextures.append(renderer.createTextureFromSurface(chefInstructionImages[x]))
      sdl.freeSurface(chefInstructionImages[x])

    global chef
    chef = MC.Chef(350, 220, 50, 80, 'none', 0.2, 0, 0, 0.001, 0.001,
            [chefActionTextures, chefItemTextures, chefUITextures, chefInstructionTextures], False, 10000, 0, 3, False, [1, 300])


def cleanup():
    if renderer is not None:
        sdl.destroyRenderer(renderer)
    if window is not None:
        sdl.destroyWindow(window)
    for x in range(len(chefActionTextures)):
        if chefActionTextures[x] is not None:
            sdl.destroyTexture(chefActionTextures[x])
    for x in range(len(chefItemTextures)):
        if chefItemTextures[x] is not None:
            sdl.destroyTexture(chefItemTextures[x])
    for x in range(len(chefUITextures)):
        if chefUITextures[x] is not None:
            sdl.destroyTexture(chefUITextures[x])
    for x in range(len(chefInstructionTextures)):
        if chefInstructionTextures[x] is not None:
            sdl.destroyTexture(chefInstructionTextures[x])
    sdl.ttf.quit()
    sdl.mixer.closeAudio()
    sdl.quit()
