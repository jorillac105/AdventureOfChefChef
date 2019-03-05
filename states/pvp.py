import sys
import math
sys.path.insert(0, '/../entities/')
sys.path.insert(0, '/../')
import driver
import sdl
from basicState import BasicState
import MCClass as MC
import object
import random
import game
import rats
import navGraph
from emitter import Emitter
from object import Object
from camera import Camera
from structure import Structure
from story import Story
from pauseMenu import Pause
from projectile import Projectile

class Pvp(BasicState):

    def __init__(self):
        self.next = None

  # relies on the Seperating Axis Theorem to test for intersection

    def intersects(self, first, other):
        first.updateBasePvp()
        other.updateBasePvp()
        return not (first.base.topRight[0] < other.base.bottomLeft[0]            # True if there's a collision.
                    or first.base.bottomLeft[0]
                    > other.base.topRight[0] or first.base.topRight[1]
                    > other.base.bottomLeft[1]
                    or first.base.bottomLeft[1]
                    < other.base.topRight[1])

    def load(self):
        time = sdl.getTicks()

    # driver.loading.load()

        global music
        global hit
        global explosionSound
        global ratDyingSound
        global scrollSound
        story = Story(4)
        story.load()
        story.run()

    # driver.loading.run()

        sdl.mixer.allocateChannels(3)
        music = sdl.mixer.loadMUS('music/songs/3.mod')
        hit = []
        for i in range(3):
            hit.append(sdl.mixer.loadWAV_RW(sdl.RWFromFile('music/chunks/hit'
                        + str(i) + '.wav', 'rw'), 0))
        explosionSound = \
            sdl.mixer.loadWAV_RW(sdl.RWFromFile('music/chunks/explosion.wav'
                                 , 'rw'), 0)
        ratDyingSound = \
            sdl.mixer.loadWAV_RW(sdl.RWFromFile('music/chunks/rat_death.mp3'
                                 , 'rw'), 0)

        scrollSound = sdl.mixer.loadWAV_RW(sdl.RWFromFile("music//chunks/menu_scroll.wav", 'rw'), 0)

        ratImages = [
            sdl.image.load('graphics/sprites/rat_2_hurt.png'),
            sdl.image.load('graphics/sprites/rat_2_up.png'),
            sdl.image.load('graphics/sprites/rat_2_right.png'),
            sdl.image.load('graphics/sprites/rat_2_down.png'),
            sdl.image.load('graphics/sprites/rat_2_left.png'),
            sdl.image.load('graphics/sprites/rat_2_attack_up.png'),
            sdl.image.load('graphics/sprites/rat_2_attack_right.png'),
            sdl.image.load('graphics/sprites/rat_2_attack_down.png'),
            sdl.image.load('graphics/sprites/rat_2_attack_left.png'),
            sdl.image.load('graphics/items/cheese.png'),
            ]

    # array of tiles used throughout the map

        mapImages = []
        for x in range(1, 13):
            mapImages.append(sdl.image.load('graphics/map/boss/'
                             + str(x) + '.png'))

        objectImages = []
        objectImages.append(sdl.image.load('graphics/items/pizza_animation.png'
                            ))
        objectImages.append(sdl.image.load('graphics/items/heart_animation.png'
                            ))
        objectImages.append(sdl.image.load('graphics/items/carrot_animation.png'
                            ))
        objectImages.append(sdl.image.load('graphics/items/key_animation.png'
                            ))
        objectImages.append(sdl.image.load('graphics/items/bomb_animation.png'
                            ))

        pipeImages = [
            sdl.image.load('graphics/items/blue_pipe_animation.png'),
            sdl.image.load('graphics/items/blue_pipe_closed.png'),
            sdl.image.load('graphics/items/blue_pipe_open.png'),
            sdl.image.load('graphics/items/blue_pipe_trap_animation.png'
                           ),
            sdl.image.load('graphics/items/red_pipe_animation.png'),
            sdl.image.load('graphics/items/red_pipe_closed.png'),
            sdl.image.load('graphics/items/red_pipe_open.png'),
            sdl.image.load('graphics/messages/press_open.png'),
            sdl.image.load('graphics/messages/press_close.png'),
            ]

        weaponImages = []
        weaponImages.append(sdl.image.load('graphics/items/ladles.png'))
        weaponImages.append(sdl.image.load('graphics/items/graters.png'
                            ))

        pipeTextures = []
        for x in range(len(pipeImages)):
            pipeTextures.append(driver.renderer.createTextureFromSurface(pipeImages[x]))
            sdl.freeSurface(pipeImages[x])

    # creates an array of arrays of integrets that represents our map's floor

        global map
        map = []
        with open('data/pvp.txt') as f:
            for line in f:
                currentLine = []
                split = line.split()
                for value in line.split():
                    currentLine.append(int(value))
                map.append(currentLine)

    # fill up the objects array which contains the objects that can be collided with

        global structures
        structures = []


        self.navGraph = navGraph.navGraph(map, {1, 26, 27, 28, 29}, 1)

    # for now just stuff that's dropped by the rats + the carrot

        global objects
        objects = []

        global objectTextures
        objectTextures = []
        for x in range(len(objectImages)):
            objectTextures.append(driver.renderer.createTextureFromSurface(objectImages[x]))
            sdl.freeSurface(objectImages[x])
        for x in range(len(weaponImages)):
            objectTextures.append(driver.renderer.createTextureFromSurface(weaponImages[x]))
            sdl.freeSurface(weaponImages[x])

        global ratTextures
        ratTextures = []
        for x in range(len(ratImages)):
            ratTextures.append(driver.renderer.createTextureFromSurface(ratImages[x]))
            sdl.freeSurface(ratImages[x])

        global mapTextures
        limitedVisionTexture1 = \
            driver.renderer.createTextureFromSurface(sdl.image.load('graphics/ui/limited_vision1.png'
                ))
        limitedVisionTexture2 = \
            driver.renderer.createTextureFromSurface(sdl.image.load('graphics/ui/limited_vision2.png'
                ))
        mapTextures = []
        for x in range(len(mapImages)):
            mapTextures.append(driver.renderer.createTextureFromSurface(mapImages[x]))
            sdl.freeSurface(mapImages[x])
        mapTextures.append(limitedVisionTexture1)
        mapTextures.append(limitedVisionTexture2)

    # set the current score to waht it was plus 100000

        driver.scoreBoard.setScore(driver.chef.score + 100000)

    # driver.loading.cleanup()

    def cleanup(self):
        if music is not None:
            sdl.mixer.freeMusic(music)

        for x in range(len(ratTextures)):
            if ratTextures[x] is not None:
                sdl.destroyTexture(ratTextures[x])

        for x in range(len(mapTextures)):
            if mapTextures[x] is not None:
                sdl.destroyTexture(mapTextures[x])

        for x in range(len(objectTextures)):
            if objectTextures[x] is not None:
                sdl.destroyTexture(objectTextures[x])

        for x in range(len(hit)):
            if hit[x] is not None:
                sdl.mixer.freeChunk(hit[x])

        if ratDyingSound is not None:
            sdl.mixer.freeChunk(ratDyingSound)

        if explosionSound is not None:
            sdl.mixer.freeChunk(explosionSound)

    def createRandomRat(self, directions, time):
        enemySpeed = 0.05

      # xPosition = 500 #random.randint(600, 601)
      # yPosition = 450 #random.randint(450, 451)

        xPosition = random.randint(0, len(map[0]) - 1)
        yPosition = random.randint(0, len(map) - 1)

        direction = directions[random.randint(0, 7)]
        rat = rats.Enemy(
            xPosition * 50,
            yPosition * 50,
            50,
            60,
            direction,
            enemySpeed,
            5,
            1,
            time,
            self.navGraph
            )

        while rat.checkCollisions(rat.getImmediateSurroundings(map)):
            xPosition = random.randint(0, len(map[0]) - 1)
            yPosition = random.randint(0, len(map) - 1)
            rat.updateX(xPosition * 50)
            rat.updateY(yPosition * 50)

        rat.initialNavigation(self.chefNode)

        return rat

    def addEmitter(
        self,
        xPos,
        yPos,
        life,
        typeOf,
        ):
        return Emitter(xPos, yPos, typeOf, 50, life)

    def playHitSound(self):
        i = random.randint(0, 2)
        sdl.mixer.playChannel(0, hit[0], 0)

    def run(self):

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
                     sdl.image.load("graphics/sprites/chef_attack_knife.png")]

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
        chefUIImages.append( sdl.image.load("graphics/messages/no_energy.png"))
        chefUIImages.append( sdl.image.load("graphics/ui/green.png"))
        chefUIImages.append( sdl.image.load("graphics/ui/red.png"))
        chefUIImages.append( sdl.image.load("graphics/ui/bomb_explosion.png"))
        chefUIImages.append( sdl.image.load("graphics/ui/range_arrow.png"))



        global chefActionTextures
        global chefItemTextures
        global chefUITextures

        chefActionTextures = []
        for x in range(len(chefActionImages)):
         chefActionTextures.append(driver.renderer.createTextureFromSurface(chefActionImages[x]))
         sdl.freeSurface(chefActionImages[x])

        chefItemTextures = []
        for x in range(len(chefItemImages)):
         chefItemTextures.append(driver.renderer.createTextureFromSurface(chefItemImages[x]))
         sdl.freeSurface(chefItemImages[x])

        chefUITextures = []
        for x in range(len(chefUIImages)):
         chefUITextures.append(driver.renderer.createTextureFromSurface(chefUIImages[x]))
         sdl.freeSurface(chefUIImages[x])

        global chef2
        chef2 = MC.Chef(400, 270, 50, 80, 'none', 0.2, 0, 0, 0.001, 0.001,
            [chefActionTextures, chefItemTextures, chefUITextures], False, 10000, 0, 3, False, [1, 300])
        chef2.updateTitle(2)

        sdl.mixer.volume(-1, driver.volume)
        sdl.mixer.volumeMusic(driver.volume)
        sdl.mixer.playMusic(music, -1)
        running = True
        accumulator = 0.0

      # clockwise starting at 12 o'clock

        directions = [
            'n',
            'ne',
            'e',
            'se',
            's',
            'sw',
            'w',
            'nw',
            ]

      # Boolean key directions

        up = False
        down = False
        left = False
        right = False

        up2 = False
        down2 = False
        left2 = False
        right2 = False



      # space = attack

        space = False

      # z - place bomb

        z = False

      # x - blow that shit up

        x = False

      # r = release the rats

        r = False

      # use = use interactible structure

        use = False

      # a / s /d / w to move the knife aimer left/right

        a = False
        s = False
        d = False
        w = False

      # f to create a new projectile for the chef
        f = False

      # list of enemies

        enemies = []

      # list of emitters

        emitters = []
        explosionLife = 500

        driver.chef.addWeapon('knives')
        chef2.addWeapon('knives')

      # true if not at the black screen

        notBlackScreen = True
        fadeToBlackTime = 0

        event = sdl.Event()

        driver.chef.velX = 0
        driver.chef.velY = 0
        driver.chef.xPos = 550
        driver.chef.yPos = 350
        driver.chef.direction = 'none'
        driver.chef.floorTile = [1, 26, 27, 28, 29]
        driver.chef.attacking = False
        driver.chef.attackingTime = 0

        time = 0
        lastTime = sdl.getTicks()
        camera = Camera(
            driver.chef,
            chef2,
            map,
            mapTextures,
            objects,
            enemies,
            emitters,
            game.width,
            game.height,
            ratTextures,
            structures,
            6,
            None,
            None
            )
        pauseMenu = Pause(camera)
        chef2.addCamera(camera)
        paused = False

       # create 5 randomly placed enemies moving in a random direction at enemySpeed

        self.chefNode = self.navGraph.getNode(driver.chef.xPos//50, driver.chef.yPos//50)


        currentTime = sdl.getTicks()
        sdl.renderPresent(driver.renderer)
        frames = 0
        ratCount = 0
        keyPress = False
        while running:
            currentTime = sdl.getTicks()
            framerate = 3000 / 60.0
            dt = currentTime - lastTime
            time += dt
            lastTime = currentTime
            accumulator += dt

          # the time at which the player can be hit by enemies

            while accumulator >= framerate:
                if paused:
                    pauseMenu.load()
                    running = pauseMenu.run()
                    pauseMenu.cleanup
                    paused = False
                    lastTime = sdl.getTicks()
                    sdl.mixer.volume(-1, driver.volume)
                    sdl.mixer.volumeMusic(driver.volume)
                else:
                    if driver.chef.getHealth() <= 0:
                      driver.chef.health = 3
                      chef2.health = 3
                    if chef2.getHealth() <= 0:
                      driver.chef.health = 3
                      chef2.health = 3


                # elif (driver.chef.yPos <= 50  and driver.chef.xPos >= len(map[0]) * 50 - 150 and
                #   driver.chef.xPos <= len(map[0]) * 50 - 100 and
                  #  driver.chef.hasKey is True and len(enemies) is 0):
                  # running = False
                  # self.next = "levelTwo"

                    while sdl.pollEvent(event):
                        if event.type == sdl.QUIT:
                            running = False
                            game.turnOff()
                        elif event.type == sdl.KEYUP:
                            if event.key.keysym.sym in [sdl.K_q,
                                    sdl.K_ESCAPE]:
                                running = False
                                game.turnOff()
                            if event.key.keysym.sym == sdl.K_UP:
                                up = False
                            elif event.key.keysym.sym == sdl.K_DOWN:
                                down = False
                            elif event.key.keysym.sym == sdl.K_LEFT:
                                left = False
                            elif event.key.keysym.sym == sdl.K_RIGHT:
                                right = False
                            elif event.key.keysym.sym == sdl.K_SPACE:
                                space = False
                            elif event.key.keysym.sym == sdl.K_RETURN:
                                use = False
                            elif event.key.keysym.sym == sdl.K_z:
                                z = False
                            elif event.key.keysym.sym == sdl.K_l:
                              if not space and not driver.chef.getDizzy() and not driver.chef.attacking and 'knives' in driver.chef.weapons:
                                randInt = random.randint(1,3)
                                randDegree = random.randint(-7,7) # make a cone of knives, I mean he is spiining how accurate can he be
                                tempX = driver.chef.velX
                                tempY = driver.chef.velY
                                if randInt is 1:
                                  driver.chef.projectiles.append(Projectile(driver.chef.xPos + driver.chef.width / 2, driver.chef.yPos + driver.chef.height / 2, 32, 32, 'knife', driver.chef.textures[1][6], driver.renderer, math.pi + math.radians(randDegree),tempX, tempY))
                                if randInt is 2:
                                  driver.chef.projectiles.append(Projectile(driver.chef.xPos + driver.chef.width / 2, driver.chef.yPos + driver.chef.height / 2, 45, 45, 'knife', driver.chef.textures[1][7], driver.renderer, math.pi + math.radians(randDegree),tempX, tempY))
                                if randInt is 3:
                                  driver.chef.projectiles.append(Projectile(driver.chef.xPos + driver.chef.width / 2, driver.chef.yPos + driver.chef.height / 2, 50, 50, 'knife', driver.chef.textures[1][8], driver.renderer, math.pi + math.radians(randDegree),tempX, tempY))
                              else: driver.chef.knifeAttacking = False
                            elif event.key.keysym.sym == sdl.K_SEMICOLON:
                              if not space and not driver.chef.getDizzy() and not driver.chef.attacking and 'knives' in driver.chef.weapons:
                                randInt = random.randint(1,3)
                                randDegree = random.randint(-7,7) # make a cone of knives, I mean he is spiining how accurate can he be
                                tempX = driver.chef.velX
                                tempY = driver.chef.velY
                                if randInt is 1:
                                  driver.chef.projectiles.append(Projectile(driver.chef.xPos + driver.chef.width / 2, driver.chef.yPos + driver.chef.height / 2, 32, 32, 'knife', driver.chef.textures[1][6], driver.renderer, .5 * math.pi + math.radians(randDegree),tempX, tempY))
                                if randInt is 2:
                                  driver.chef.projectiles.append(Projectile(driver.chef.xPos + driver.chef.width / 2, driver.chef.yPos + driver.chef.height / 2, 45, 45, 'knife', driver.chef.textures[1][7], driver.renderer, .5 * math.pi + math.radians(randDegree),tempX, tempY))
                                if randInt is 3:
                                  driver.chef.projectiles.append(Projectile(driver.chef.xPos + driver.chef.width / 2, driver.chef.yPos + driver.chef.height / 2, 50, 50, 'knife', driver.chef.textures[1][8], driver.renderer, .5 * math.pi + math.radians(randDegree),tempX, tempY))
                              else: driver.chef.knifeAttacking = False
                            elif event.key.keysym.sym == sdl.K_QUOTE:
                              if not space and not driver.chef.getDizzy() and not driver.chef.attacking and 'knives' in driver.chef.weapons:
                                randInt = random.randint(1,3)
                                randDegree = random.randint(-7,7) # make a cone of knives, I mean he is spiining how accurate can he be
                                tempX = driver.chef.velX
                                tempY = driver.chef.velY
                                if randInt is 1:
                                  driver.chef.projectiles.append(Projectile(driver.chef.xPos + driver.chef.width / 2, driver.chef.yPos + driver.chef.height / 2, 32, 32, 'knife', driver.chef.textures[1][6], driver.renderer, math.radians(randDegree),tempX, tempY))
                                if randInt is 2:
                                  driver.chef.projectiles.append(Projectile(driver.chef.xPos + driver.chef.width / 2, driver.chef.yPos + driver.chef.height / 2, 45, 45, 'knife', driver.chef.textures[1][7], driver.renderer, math.radians(randDegree),tempX, tempY))
                                if randInt is 3:
                                  driver.chef.projectiles.append(Projectile(driver.chef.xPos + driver.chef.width / 2, driver.chef.yPos + driver.chef.height / 2, 50, 50, 'knife', driver.chef.textures[1][8], driver.renderer, math.radians(randDegree),tempX, tempY))
                              else: driver.chef.knifeAttacking = False
                            elif event.key.keysym.sym == sdl.K_p:
                              if not space and not driver.chef.getDizzy() and not driver.chef.attacking and 'knives' in driver.chef.weapons:
                                randInt = random.randint(1,3)
                                randDegree = random.randint(-7,7) # make a cone of knives, I mean he is spiining how accurate can he be
                                tempX = driver.chef.velX
                                tempY = driver.chef.velY
                                if not space and not driver.chef.getDizzy() and not driver.chef.attacking and 'knives' in driver.chef.weapons:
                                  if randInt is 1:
                                   driver.chef.projectiles.append(Projectile(driver.chef.xPos + driver.chef.width / 2, driver.chef.yPos + driver.chef.height / 2, 32, 32, 'knife', driver.chef.textures[1][6], driver.renderer, 1.5 * math.pi + math.radians(randDegree), tempX, tempY))
                                  if randInt is 2:
                                    driver.chef.projectiles.append(Projectile(driver.chef.xPos + driver.chef.width / 2, driver.chef.yPos + driver.chef.height / 2, 45, 45, 'knife', driver.chef.textures[1][7], driver.renderer, 1.5 * math.pi + math.radians(randDegree), tempX, tempY))
                                  if randInt is 3:
                                    driver.chef.projectiles.append(Projectile(driver.chef.xPos + driver.chef.width / 2, driver.chef.yPos + driver.chef.height / 2, 50, 50, 'knife', driver.chef.textures[1][8], driver.renderer, 1.5 * math.pi + math.radians(randDegree), tempX, tempY))
                              else: driver.chef.knifeAttacking = False
                            elif event.key.keysym.sym == sdl.K_f:
                                f = False
                            if event.key.keysym.sym == sdl.K_t:
                                up2 = False
                            elif event.key.keysym.sym == sdl.K_g:
                                down2 = False
                            elif event.key.keysym.sym == sdl.K_f:
                                left2 = False
                            elif event.key.keysym.sym == sdl.K_h:
                                right2 = False
                            elif event.key.keysym.sym == sdl.K_a:
                              if not space and not chef2.getDizzy() and not chef2.attacking and 'knives' in chef2.weapons:
                                randInt = random.randint(1,3)
                                randDegree = random.randint(-7,7) # make a cone of knives, I mean he is spiining how accurate can he be
                                tempX = chef2.velX
                                tempY = chef2.velY
                                if randInt is 1:
                                  chef2.projectiles.append(Projectile(chef2.xPos + chef2.width / 2, chef2.yPos + chef2.height / 2, 32, 32, 'knife', chef2.textures[1][6], driver.renderer, math.pi + math.radians(randDegree),tempX, tempY))
                                if randInt is 2:
                                  chef2.projectiles.append(Projectile(chef2.xPos + chef2.width / 2, chef2.yPos + chef2.height / 2, 45, 45, 'knife', chef2.textures[1][7], driver.renderer, math.pi + math.radians(randDegree),tempX, tempY))
                                if randInt is 3:
                                  chef2.projectiles.append(Projectile(chef2.xPos + chef2.width / 2, chef2.yPos + chef2.height / 2, 50, 50, 'knife', chef2.textures[1][8], driver.renderer, math.pi + math.radians(randDegree),tempX, tempY))
                              else: chef2.knifeAttacking = False
                            elif event.key.keysym.sym == sdl.K_s:
                              if not space and not chef2.getDizzy() and not chef2.attacking and 'knives' in chef2.weapons:
                                randInt = random.randint(1,3)
                                randDegree = random.randint(-7,7) # make a cone of knives, I mean he is spiining how accurate can he be
                                tempX = chef2.velX
                                tempY = chef2.velY
                                if randInt is 1:
                                  chef2.projectiles.append(Projectile(chef2.xPos + chef2.width / 2, chef2.yPos + chef2.height / 2, 32, 32, 'knife', chef2.textures[1][6], driver.renderer, .5 * math.pi + math.radians(randDegree),tempX, tempY))
                                if randInt is 2:
                                  chef2.projectiles.append(Projectile(chef2.xPos + chef2.width / 2, chef2.yPos + chef2.height / 2, 45, 45, 'knife', chef2.textures[1][7], driver.renderer, .5 * math.pi + math.radians(randDegree),tempX, tempY))
                                if randInt is 3:
                                  chef2.projectiles.append(Projectile(chef2.xPos + chef2.width / 2, chef2.yPos + chef2.height / 2, 50, 50, 'knife', chef2.textures[1][8], driver.renderer, .5 * math.pi + math.radians(randDegree),tempX, tempY))
                              else: chef2.knifeAttacking = False
                            elif event.key.keysym.sym == sdl.K_d:
                              if not space and not chef2.getDizzy() and not chef2.attacking and 'knives' in chef2.weapons:
                                randInt = random.randint(1,3)
                                randDegree = random.randint(-7,7) # make a cone of knives, I mean he is spiining how accurate can he be
                                tempX = chef2.velX
                                tempY = chef2.velY
                                if randInt is 1:
                                  chef2.projectiles.append(Projectile(chef2.xPos + chef2.width / 2, chef2.yPos + chef2.height / 2, 32, 32, 'knife', chef2.textures[1][6], driver.renderer, math.radians(randDegree),tempX, tempY))
                                if randInt is 2:
                                  chef2.projectiles.append(Projectile(chef2.xPos + chef2.width / 2, chef2.yPos + chef2.height / 2, 45, 45, 'knife', chef2.textures[1][7], driver.renderer, math.radians(randDegree),tempX, tempY))
                                if randInt is 3:
                                  chef2.projectiles.append(Projectile(chef2.xPos + chef2.width / 2, chef2.yPos + chef2.height / 2, 50, 50, 'knife', chef2.textures[1][8], driver.renderer, math.radians(randDegree),tempX, tempY))
                              else: chef2.knifeAttacking = False
                            elif event.key.keysym.sym == sdl.K_w:
                              if not space and not chef2.getDizzy() and not chef2.attacking and 'knives' in chef2.weapons:
                                randInt = random.randint(1,3)
                                randDegree = random.randint(-7,7) # make a cone of knives, I mean he is spiining how accurate can he be
                                tempX = chef2.velX
                                tempY = chef2.velY
                                if not space and not chef2.getDizzy() and not chef2.attacking and 'knives' in chef2.weapons:
                                  if randInt is 1:
                                   chef2.projectiles.append(Projectile(chef2.xPos + chef2.width / 2, chef2.yPos + chef2.height / 2, 32, 32, 'knife', chef2.textures[1][6], driver.renderer, 1.5 * math.pi + math.radians(randDegree), tempX, tempY))
                                  if randInt is 2:
                                    chef2.projectiles.append(Projectile(chef2.xPos + chef2.width / 2, chef2.yPos + chef2.height / 2, 45, 45, 'knife', chef2.textures[1][7], driver.renderer, 1.5 * math.pi + math.radians(randDegree), tempX, tempY))
                                  if randInt is 3:
                                    chef2.projectiles.append(Projectile(chef2.xPos + chef2.width / 2, chef2.yPos + chef2.height / 2, 50, 50, 'knife', chef2.textures[1][8], driver.renderer, 1.5 * math.pi + math.radians(randDegree), tempX, tempY))
                              else: chef2.knifeAttacking = False
                        if event.type == sdl.KEYDOWN:
                            if event.key.keysym.sym == sdl.K_UP:
                                up = True
                            elif event.key.keysym.sym == sdl.K_DOWN:
                                down = True
                            elif event.key.keysym.sym == sdl.K_LEFT:
                                left = True
                            elif event.key.keysym.sym == sdl.K_RIGHT:
                                right = True
                            elif event.key.keysym.sym == sdl.K_SPACE:
                                space = True
                            if event.key.keysym.sym == sdl.K_t:
                                up2 = True
                            elif event.key.keysym.sym == sdl.K_g:
                                down2 = True
                            elif event.key.keysym.sym == sdl.K_f:
                                left2 = True
                            elif event.key.keysym.sym == sdl.K_h:
                                right2 = True
                            elif event.key.keysym.sym == sdl.K_SPACE:
                                space = True
                            elif event.key.keysym.sym == sdl.K_r:
                                r = True
                            elif event.key.keysym.sym == sdl.K_r:
                                r = True
                            elif event.key.keysym.sym == sdl.K_a:
                                a = True
                            elif event.key.keysym.sym == sdl.K_s:
                                s = True
                            elif event.key.keysym.sym == sdl.K_d:
                                d = True
                            elif event.key.keysym.sym == sdl.K_w:
                                w = True
                            elif event.key.keysym.sym == sdl.K_f:
                                f = True
                            elif event.key.keysym.sym == sdl.K_RETURN:
                                use = True
                            elif event.key.keysym.sym == sdl.K_h:

                      # debug option to add 8 health

                                driver.chef.setCanBeHit(False)
                                driver.chef.setDizzy(True)
                                driver.chef.setCanBeHitTime(time + 3000)
                                driver.chef.setDizzyTime(time + 750)

                          # sdl.mixer.playMusic(bumpSound, 1)

                                driver.chef.updateHealth(8)

                            elif event.key.keysym.sym == sdl.K_m:
                                running = False
                                self.next = 'menu'
                            elif event.key.keysym.sym == sdl.K_c:

                      # Debug: add a carrot item

                                if 'carrot' not in driver.chef.items:
                                    driver.chef.addItem('carrot')
                                else:
                                    driver.chef.removeItem('carrot')
                            elif event.key.keysym.sym == sdl.K_z:
                                # place the bomb down
                                if 'bomb' in driver.chef.weapons:
                                    driver.chef.setPlacingBomb(True)
                                    objects.append(Object(
                                        driver.chef.xPos - 75,
                                        driver.chef.yPos - 25,
                                        200,
                                        200,
                                        'bomb',
                                        driver.chef.textures[2][10],
                                        ))
                                    driver.chef.weapons.remove('bomb')
                            elif event.key.keysym.sym == sdl.K_x:
                                sound = False
                                for x in range(len(objects) - 1, -1,
                                        -1):
                                    if objects[x].getTitle() == 'bomb':
                                        sound = True
                                        tsum = currentTime \
    + explosionLife
                                        emit = \
    self.addEmitter(objects[x].xPos + objects[x].width // 2,
                    objects[x].yPos + objects[x].height // 2, tsum,
                    'explosion')
                                        emit.emit()
                                        emitters.append(emit)
                                        for enemy in enemies:
                                            if self.withinRange(objects[x],
        enemy, 100):
                                                enemy.updateHealth(-4)
                                                enemy.setHurt(True)
                                                enemy.setHurtTime(time
        + 1000)
                                        if self.withinRange(objects[x], driver.chef, 100):
                                           driver.chef.health = 0
                                        objects.append(Object(
                                            objects[x].xPos,
                                            objects[x].yPos,
                                            200,
                                            200,
                                            'explosion',
                                            driver.chef.textures[2][12],
                                            ))
                                        objects.remove(objects[x])
                                if sound:
                                    sdl.mixer.playChannel(1,
        explosionSound, 0)
                            elif event.key.keysym.sym == sdl.K_e:
                                tsum = currentTime + explosionLife
                                emit = self.addEmitter(driver.chef.xPos
                                        + driver.chef.getWidth() // 2,
                                        driver.chef.yPos
                                        + driver.chef.getHeight() // 2,
                                        tsum, 'explosion')
                                emit.emit()
                                emitters.append(emit)
                            elif event.key.keysym.sym == sdl.K_b:
                                driver.chef.addWeapon('bomb')

                    keyPress = left or right or up or down
                    keyPress2 = left2 or right2 or up2 or down2
                    driver.chef.degreePress = a or s or d or w

                # based on the keys pressed down set the driver.chef's direction

                    if keyPress is True:
                        driver.chef.updateDirection(up, down, left,
                                right)

                    if keyPress2 is True:
                        chef2.updateDirection(up2, down2, left2,
                                right2)


                # if items are "used" aka past their onscreen time, remove them

                    for x in range(len(objects) - 1, -1, -1):
                        if objects[x].used is True:
                            objects.remove(objects[x])

                # remove projectiles if they are too much offscreen CHEF1
                    projLen = len(driver.chef.projectiles)
                    for x in range(projLen -1, -1, -1):
                      projectile = driver.chef.projectiles[x]
                      if abs(projectile.xPos - driver.chef.xPos) > 1000 or abs(projectile.yPos - driver.chef.yPos) > 1000:
                        driver.chef.projectiles.remove(projectile)

                # remove projectiles if they are too much offscreen CHEF2
                    projLen = len(chef2.projectiles)
                    for x in range(projLen -1, -1, -1):
                      projectile = chef2.projectiles[x]
                      if abs(projectile.xPos - chef2.xPos) > 1000 or abs(projectile.yPos - chef2.yPos) > 1000:
                        chef2.projectiles.remove(projectile)

                # check for intersections between the chef1's projectiles and chef2
                    projLen = len(driver.chef.projectiles)
                    for x in range(projLen -1, -1, -1):
                      projectile = driver.chef.projectiles[x]
                      remove = False
                      if self.intersects(projectile, chef2):
                          chef2.updateHealth(-1)
                          remove = True
                      if remove is True:
                         driver.chef.projectiles.remove(projectile)

                # check for intersections between the chef2's projectiles and the chef1
                    projLen = len(chef2.projectiles)
                    for x in range(projLen -1, -1, -1):
                      projectile = chef2.projectiles[x]
                      remove = False
                      if self.intersects(projectile, driver.chef):
                          driver.chef.updateHealth(-1)
                          remove = True
                      if remove is True:
                         chef2.projectiles.remove(projectile)

                # update driver.chef position based on what keys are being pressed
                # down if keys are pressed down and he is not off the screen
                # also based on if driver.chef collides into stuff

                    driver.chef.updatePosition(accumulator, map, keyPress)
                    for projectile in driver.chef.projectiles:
                      projectile.updatePosition(accumulator)

                    # print("1: " + str(len(driver.chef.projectiles)) + " 2: " + str(len(chef2.projectiles)))
                    chef2.updatePosition(accumulator, map, keyPress2)
                    for projectile in chef2.projectiles:
                      projectile.updatePosition(accumulator)

                    self.chefNode = driver.chef.getNode(self.navGraph)

                # boing sound if the driver.chef hits the wall
                # if self.checkCollisions(driver.chef, objects):
                #  sdl.mixer.playMusic(boingSound, 1)


                    accumulator -= framerate

            camera.display(currentTime, dt, keyPress, time)
            sdl.renderPresent(driver.renderer)
