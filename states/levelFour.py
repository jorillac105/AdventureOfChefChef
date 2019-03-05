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
from instructions import Instruct

class LevelFour(BasicState):

    def __init__(self):
        self.next = None

    def objectsWithinRange(self, bomb, chef, enemies, range):
      for enemy in enemies:
        xDiff = abs((bomb.xPos + bomb.width / 2) - (enemy.xPos + enemy.width / 2))
        yDiff = abs((bomb.yPos + bomb.height / 2) - (enemy.yPos + enemy.height / 2))
        distance = math.sqrt(math.pow(xDiff, 2) + math.pow(yDiff, 2))
        if distance <= range:
          return True
      xDiff = abs((bomb.xPos + bomb.width / 2) - (chef.xPos + chef.width / 2))
      yDiff = abs((bomb.yPos + bomb.height / 2) - (chef.yPos + chef.height / 2))
      distance = math.sqrt(math.pow(xDiff, 2) + math.pow(yDiff, 2))
      if distance <= range:
        return True
      return False

    def withinRange(
        self,
        bomb,
        enemy,
        range,
        ):
        xDiff = abs(bomb.xPos + bomb.width / 2 - (enemy.xPos
                    + enemy.width / 2))
        yDiff = abs(bomb.yPos + bomb.height / 2 - (enemy.yPos
                    + enemy.height / 2))
        distance = math.sqrt(math.pow(xDiff, 2) + math.pow(yDiff, 2))
        if distance <= range:
            return True
        else:
            return False

  # relies on the Seperating Axis Theorem to test for intersection

    def intersects(self, first, other):
        first.updateBase()
        other.updateBase()

      # True if there's a collision.

        return not (first.base.topRight[0] < other.base.bottomLeft[0]
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
        global ladleHit, graterHit, knifeThrow, hitGeneric
        global explosionSound
        global ratDyingSound, woosh
        global scrollSound
        story = Story(5)
        story.load()
        story.run()

    # driver.loading.run()

        sdl.mixer.allocateChannels(4)
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
        ladleHit =  sdl.mixer.loadWAV_RW(sdl.RWFromFile('music/chunks/ladle_hit.wav', 'rw'), 0)
        graterHit =  sdl.mixer.loadWAV_RW(sdl.RWFromFile('music/chunks/grater_hit.wav', 'rw'), 0)
        hitGeneric =  sdl.mixer.loadWAV_RW(sdl.RWFromFile('music/chunks/hit.wav', 'rw'), 0)
        knifeThrow =  sdl.mixer.loadWAV_RW(sdl.RWFromFile('music/chunks/knife_throw.wav', 'rw'), 0)

        scrollSound = sdl.mixer.loadWAV_RW(sdl.RWFromFile("music//chunks/menu_scroll.wav", 'rw'), 0)
        woosh = sdl.mixer.loadWAV_RW(sdl.RWFromFile('music/chunks/woosh.wav', 'rw'), 0)

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
        for x in range(1, 30):
            mapImages.append(sdl.image.load('graphics/map/level_3/'
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
        with open('data/level4.txt') as f:
            for line in f:
                currentLine = []
                split = line.split()
                for value in line.split():
                    currentLine.append(int(value))
                map.append(currentLine)

    # fill up the objects array which contains the objects that can be collided with

        global structures
        structures = []
        global exit
        count = 0
        for j in range(len(map)):
            for i in range(len(map[j])):
                value = map[j][i]
                if value is 24:
                    structures.append(Structure(
                        value,
                        i,
                        j,
                        pipeTextures,
                        False,
                        'bluePipe',
                        ))
                elif value is 25:
                    structures.append(Structure(
                        value,
                        i,
                        j,
                        pipeTextures,
                        False,
                        'redPipe',
                        ))


        self.navGraph = navGraph.navGraph(map, {1, 26, 27, 28, 29}, 4)

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

        if ladleHit is not None:
            sdl.mixer.freeChunk(ladleHit)

        if graterHit is not None:
            sdl.mixer.freeChunk(graterHit)

        if hitGeneric is not None:
            sdl.mixer.freeChunk(hitGeneric)

        if woosh is not None:
            sdl.mixer.freeChunk(woosh)

        if knifeThrow is not None:
            sdl.mixer.freeChunk(knifeThrow)

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
        self.genericHit()

    def genericHit(self):
        sdl.mixer.playChannel(-1, hitGeneric, 0)

    def run(self):
        sdl.mixer.volume(-1, driver.volume)
        sdl.mixer.volumeMusic(driver.volume)
        sdl.mixer.playMusic(music, -1)
        running = True
        accumulator = 0.0
        hittable = True

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

      # add the knives
        objects.append(Object(
            600,
            400,
            50,
            50,
            'knives',
            driver.chef.textures[1][9],
            ))

      # true if not at the black screen

        notBlackScreen = True
        fadeToBlackTime = 0

        event = sdl.Event()

        driver.chef.velX = 0
        driver.chef.velY = 0
        driver.chef.xPos = 550
        driver.chef.yPos = 250
        driver.chef.direction = 'none'
        driver.chef.floorTile = [1, 26, 27, 28, 29]
        driver.chef.attacking = False
        driver.chef.attackingTime = 0

        time = 0
        lastTime = sdl.getTicks()
        camera = Camera(
            driver.chef,
            None,
            map,
            mapTextures,
            objects,
            enemies,
            emitters,
            game.width,
            game.height,
            ratTextures,
            structures,
            4,
            None,
            None
            )

        camera.updateChefX(driver.chef.xPos)
        camera.updateChefY(driver.chef.yPos)

        pauseMenu = Pause(camera)
        paused = False

        instructionScreen = Instruct(camera)
        instr = False
        global item

       # create 5 randomly placed enemies moving in a random direction at enemySpeed

        self.chefNode = self.navGraph.getNode(driver.chef.xPos//50, driver.chef.yPos//50)

        for i in range(4):
           enemies.append(self.createRandomRat(directions, time))

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
                elif instr:
                    instructionScreen.run(item)
                    instr = False
                    lastTime = sdl.getTicks()
                    sdl.mixer.volume(-1, driver.volume)
                    sdl.mixer.volumeMusic(driver.volume)
                    up= False
                    down = False
                    left = False
                    right = False
                    space = False
                    use = False
                    z = False
                else:
                    if driver.chef.dead:
                        running = False
                        self.next = 'gameOver'

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
                            elif event.key.keysym.sym == sdl.K_a:
                              if not space and not driver.chef.getDizzy() and not driver.chef.attacking and 'knives' in driver.chef.weapons and driver.chef.getEnergy() > 0:
                                driver.chef.updateEnergy(-1)
                                driver.chef.knifeAttackingTime = time +  driver.chef.knifeDelay
                                driver.chef.knifeAttacking = True
                                sdl.mixer.playChannel(1, knifeThrow, 0)
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
                            elif event.key.keysym.sym == sdl.K_s:
                              if not space and not driver.chef.getDizzy() and not driver.chef.attacking and 'knives' in driver.chef.weapons and driver.chef.getEnergy() > 0:
                                driver.chef.updateEnergy(-1)
                                driver.chef.knifeAttackingTime = time +  driver.chef.knifeDelay
                                driver.chef.knifeAttacking = True
                                sdl.mixer.playChannel(1, knifeThrow, 0)
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
                            elif event.key.keysym.sym == sdl.K_d:
                              if not space and not driver.chef.getDizzy() and not driver.chef.attacking and 'knives' in driver.chef.weapons and driver.chef.getEnergy() > 0:
                                driver.chef.updateEnergy(-1)
                                driver.chef.knifeAttackingTime = time +  driver.chef.knifeDelay
                                driver.chef.knifeAttacking = True
                                sdl.mixer.playChannel(1, knifeThrow, 0)
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
                            elif event.key.keysym.sym == sdl.K_w:
                              if not space and not driver.chef.getDizzy() and not driver.chef.attacking and 'knives' in driver.chef.weapons and driver.chef.getEnergy() > 0:
                                driver.chef.updateEnergy(-1)
                                driver.chef.knifeAttackingTime = time +  driver.chef.knifeDelay
                                driver.chef.knifeAttacking = True
                                sdl.mixer.playChannel(1, knifeThrow, 0)
                                randInt = random.randint(1,3)
                                randDegree = random.randint(-7,7) # make a cone of knives, I mean he is spiining how accurate can he be
                                tempX = driver.chef.velX
                                tempY = driver.chef.velY
                                if randInt is 1:
                                  driver.chef.projectiles.append(Projectile(driver.chef.xPos + driver.chef.width / 2, driver.chef.yPos + driver.chef.height / 2, 32, 32, 'knife', driver.chef.textures[1][6], driver.renderer, 1.5 * math.pi + math.radians(randDegree), tempX, tempY))
                                if randInt is 2:
                                  driver.chef.projectiles.append(Projectile(driver.chef.xPos + driver.chef.width / 2, driver.chef.yPos + driver.chef.height / 2, 45, 45, 'knife', driver.chef.textures[1][7], driver.renderer, 1.5 * math.pi + math.radians(randDegree), tempX, tempY))
                                if randInt is 3:
                                  driver.chef.projectiles.append(Projectile(driver.chef.xPos + driver.chef.width / 2, driver.chef.yPos + driver.chef.height / 2, 50, 50, 'knife', driver.chef.textures[1][8], driver.renderer, 1.5 * math.pi + math.radians(randDegree), tempX, tempY))
                              else: driver.chef.knifeAttacking = False
                            elif event.key.keysym.sym == sdl.K_f:
                                f = False
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
                            elif event.key.keysym.sym == sdl.K_l:
                                enemies.append(self.createRandomRat(directions,
                                        time))
                            elif event.key.keysym.sym == sdl.K_5:
                                running = False
                                if 'key' in driver.chef.items:
                                    driver.chef.items.remove('key')
                                driver.chef.score = \
                                    driver.scoreBoard.getScore()
                                self.next = 'levelFive'
                            elif event.key.keysym.sym == sdl.K_m:
                                running = False
                                self.next = 'menu'
                            elif event.key.keysym.sym == sdl.K_c:

                      # Debug: add a carrot item

                                if 'carrot' not in driver.chef.items:
                                    driver.chef.addItem('carrot')
                                else:
                                    driver.chef.removeItem('carrot')
                            elif event.key.keysym.sym == sdl.K_z and not driver.chef.placingBomb:
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
                                        camera.activateShake(currentTime, 300, 20, 20)
                                        for enemy in enemies:
                                            if self.withinRange(objects[x],
        enemy, 100):
                                                enemy.updateHealth(-4)
                                                enemy.setHurt(True)
                                                enemy.setHurtTime(time + 1000)
                                                enemy.bump(objects[x].getAttackingDirection(enemy))
                                        if self.withinRange(objects[x], driver.chef, 100):
                                           driver.chef.updateHealth(-10)
                                           driver.chef.bump(objects[x].getAttackingDirection(driver.chef))
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
                            elif event.key.keysym.sym == sdl.K_p:
                                paused = True

               # if the time is past the knifespin animation stop it
                    if time > driver.chef.knifeAttackingTime:
                      driver.chef.knifeAttacking = False

                    keyPress = left or right or up or down
                    driver.chef.degreePress = a or s or d or w

                # based on the keys pressed down set the driver.chef's direction

                    if keyPress is True:
                        driver.chef.updateDirection(up, down, left,
                                right)

                # if items are "used" aka past their onscreen time, remove them

                    for x in range(len(objects) - 1, -1, -1):
                        if objects[x].used is True:
                            objects.remove(objects[x])

                # remove projectiles if they are too much offscreen
                    projLen = len(driver.chef.projectiles)
                    for x in range(projLen -1, -1, -1):
                      projectile = driver.chef.projectiles[x]
                      if abs(projectile.xPos - driver.chef.xPos) > 1000 or abs(projectile.yPos - driver.chef.yPos) > 1000:
                        driver.chef.projectiles.remove(projectile)

                # check for intersections between the chef's projectiles and the rats
                    projLen = len(driver.chef.projectiles)
                    for x in range(projLen -1, -1, -1):
                      projectile = driver.chef.projectiles[x]
                      remove = False
                      for enemy in enemies:
                        if self.intersects(projectile, enemy):
                          self.genericHit()
                          remove = True
                          enemy.updateHealth(-1)
                          enemy.setHurt(True)
                          enemy.setHurtTime(time + 1000)
                          camera.activateShake(currentTime, 200, 3, 3)
                      if remove is True:
                         driver.chef.projectiles.remove(projectile)

                # if bombs are planted, make sure to check for enemies inside

                    for x in range(len(objects)):
                        if objects[x].title == 'bomb':
                            if self.objectsWithinRange(objects[x], driver.chef,
                                    enemies, 100):
                                objects[x].texture = \
                                    driver.chef.textures[2][11]
                            else:
                                objects[x].texture = \
                                    driver.chef.textures[2][10]

                # pressing space on keydown will place the player into attacking state

                    if space and time > driver.chef.getAttackingTime():
                        if driver.chef.getEnergy() > 0:
                            driver.chef.setAttacking(True)
                            driver.chef.setAttackingTime(time + 1000)  # attacking animation with be 1s
                            driver.chef.updateEnergy(-1)
                            sdl.mixer.playChannel(-1, woosh, 0)
                        else:

                    # If you try to attack when you're out of energy, become dizzy for .5s

                            driver.chef.setDizzy(True)
                            driver.chef.setDizzyTime(time + 500)

                # if the player presses "space" the driver.chef will go into attacking mode
                # which overrides other animations except getting hit

                    if time > driver.chef.getAttackingTime() \
                        or driver.chef.getDizzy():
                        driver.chef.setAttacking(False)
                    else:
                        driver.chef.setAttacking(True)
                        driver.chef.setEnergyRegenTime(time + 1000)

                # if the player is not attacking, and less than 8 pizza slices, and not dizzy, and 3s from last time attacked, give energy

                    if not space and driver.chef.getEnergy() < 8 \
                        and not driver.chef.getDizzy() and time \
                        > driver.chef.getEnergyRegenTime():
                        driver.chef.updateEnergy(1)
                        driver.chef.setEnergyRegenTime(time + 750)

                # if driver.chef not attacking or dizzy, and on same tile as object, pick it up

                    if time > driver.chef.getAttackingTime() \
                        and not driver.chef.getDizzy():
                        for obj in objects:
                            if self.intersects(driver.chef, obj):
                                if obj.getTitle() == 'pizza' \
                                    and driver.chef.getEnergy() < 8:
                                    driver.chef.updateEnergy(1)
                                    objects.remove(obj)
                                    if not driver.chef.inGottenItems('pizza'):
                                        instr = True
                                        driver.chef.setGottenItems('pizza')
                                        item = 'pizza'
                                if obj.getTitle() == 'heart' \
                                    and driver.chef.getHealth() <= 8:
                                    driver.chef.updateHealth(1)
                                    objects.remove(obj)
                                    if not driver.chef.inGottenItems('tomato'):
                                        instr = True
                                        driver.chef.setGottenItems('tomato')
                                        item = 'tomato'
                                if obj.getTitle() == 'carrot':
                                    driver.chef.addItem('carrot')
                                    objects.remove(obj)
                                    if not driver.chef.inGottenItems('carrot'):
                                        instr = True
                                        driver.chef.setGottenItems('carrot')
                                        item = 'carrot'
                                if obj.getTitle() == 'ladles':
                                    driver.chef.addWeapon('ladles')
                                    objects.remove(obj)
                                    if not driver.chef.inGottenItems('ladles'):
                                        instr = True
                                        driver.chef.setGottenItems('ladles')
                                        item = 'ladles'
                                if obj.getTitle() == 'graters':
                                    driver.chef.addWeapon('graters')
                                    if 'ladles' in driver.chef.weapons:
                                        driver.chef.weapons.remove('ladles')
                                    if not driver.chef.inGottenItems('graters'):
                                        instr = True
                                        driver.chef.setGottenItems('graters')
                                        item = 'graters'
                                        objects.remove(obj)
                                if obj.getTitle() == 'bombObject' \
                                    and driver.chef.getNumBombs() <= 5:
                                    driver.chef.addWeapon('bomb')
                                    objects.remove(obj)
                                    if not driver.chef.inGottenItems('bsv'):
                                        instr = True
                                        driver.chef.setGottenItems('bsv')
                                        item = 'bsv'
                                if obj.getTitle() == 'knives':
                                    driver.chef.addWeapon('knives')
                                    objects.remove(obj)
                                    if not driver.chef.inGottenItems('knives'):
                                        instr = True
                                        driver.chef.setGottenItems('knives')
                                        item = 'knives'

                # make sure the rats aren't invulnable after a set time

                    for enemy in enemies:
                        if time > enemy.getHurtTime():
                            enemy.setHurt(False)
                            enemy.resetDamageChange()

                # handling structure interactions

                    pipesClosed = True
                    for structure in structures:
                        if structure.identity is 'bluePipe' \
                            and structure.triggered is False:
                            structure.xPos *= 50
                            structure.yPos *= 50
                            structure.xPos -= 20
                            structure.yPos -= 20
                            structure.width += 40
                            structure.height += 40
                            if self.intersects(driver.chef, structure):
                                if structure.visible is False:
                                    structure.changeVisibility()
                            else:
                                if structure.visible:
                                    structure.changeVisibility()
                            structure.yPos += 20
                            structure.width -= 40
                            structure.height -= 40
                            structure.xPos += 20
                            structure.xPos /= 50
                            structure.yPos /= 50
                            if structure.visible:
                                if use is True:
                                    structure.triggerAction()
                                    camera.activateShake(currentTime, 200, 2, 2)
                                    randNum = random.randint(1, 10)
                                    if randNum is 1:
                                        if map[int(structure.xPos)][int(structure.yPos)] is not 1:
                                            objects.append(Object(
                                                structure.xPos * 50,
                                                structure.yPos * 50 - 50,
                                                50,
                                                50,
                                                'heart',
                                                objectTextures[1],
                                                ))
                                        else:
                                            objects.append(Object(
                                                structure.xPos * 50,
                                                structure.yPos * 50 + 50,
                                                50,
                                                50,
                                                'heart',
                                                objectTextures[1],
                                                ))
                                    elif randNum > 1 and randNum <= 10:
                                        if map[int(structure.xPos)][int(structure.yPos)] is not 1:
                                            objects.append(Object(
                                                structure.xPos * 50,
                                                structure.yPos * 50 - 50,
                                                50,
                                                50,
                                                'pizza',
                                                objectTextures[0],
                                                ))
                                        else:
                                            objects.append(Object(
                                                structure.xPos * 50,
                                                structure.yPos * 50 + 50,
                                                50,
                                                50,
                                                'pizza',
                                                objectTextures[0],
                                                ))
                        elif structure.identity is 'redPipe' \
                            and structure.triggered is False:
                            if not structure.used:
                                pipesClosed = False
                                structure.xPos *= 50
                                structure.yPos *= 50
                                structure.xPos -= 20
                                structure.yPos -= 20
                                structure.width += 40
                                structure.height += 40
                                if self.intersects(driver.chef,
                                        structure):
                                    if structure.visible is False:
                                        structure.changeVisibility()
                                else:
                                    if structure.visible:
                                        structure.changeVisibility()
                                structure.yPos += 20
                                structure.width -= 40
                                structure.height -= 40
                                structure.xPos += 20
                                structure.xPos /= 50
                                structure.yPos /= 50
                                if ratCount is 7:
                                    direction = \
    directions[random.randint(0, 7)]
                                    rat = rats.Enemy(
                                       structure.xPos * 50 - 60,
                                        structure.yPos * 50 - 20,
                                        50,
                                        60,
                                        direction,
                                        0.05,
                                        4,
                                        1,
                                        time,
                                        self.navGraph
                                        )
                                    rat.initialNavigation(self.chefNode)
                                    enemies.append(rat)
                                if structure.visible:
                                    if use is True:
                                        structure.triggerAction()
                                        camera.activateShake(currentTime, 200, 2, 2)

                # once the pipes are closed fade to black (RIGHT NOW WORKS WITH SPACE AS WELL)

                    if pipesClosed:
                        hittable = False
                        if notBlackScreen:
                            notBlackScreen = False
                            fadeToBlackTime = time + 6000
                            blackScreenTexture = \
                                driver.renderer.createTextureFromSurface(sdl.image.load('graphics/colors/black.png'
                                    ))
                            sdl.setTextureBlendMode(blackScreenTexture,
                                    sdl.BLENDMODE_BLEND)
                            objects.append(Object(
                                driver.chef.xPos - 800,
                                driver.chef.yPos - 600,
                                1600,
                                1200,
                                'blackScreen',
                                blackScreenTexture,
                                ))

                    # have the chef attacking so he can't lose to taking damage from the rats while it fades to black

                            driver.chef.setAttacking(True)
                            driver.chef.setAttackingTime(time + 4000)

                # Once the screen fully fades to black go to next level / win screen

                    if time > fadeToBlackTime and notBlackScreen \
                        is False:
                        running = False
                        self.next = 'levelFive'

                  # TRANSITION TO THE WIN SCREEN HERE

                # make sure the rats aren't attacking after a set time

                    for enemy in enemies:
                        if time > enemy.getAttackingTime():
                            enemy.setAttacking(0)

                # if the invulnability expired set hit back to true

                    if time > driver.chef.getCanBeHitTime():
                        driver.chef.setCanBeHit(True)

                # if the dizzyness expired, set dizzy back to false

                    if time > driver.chef.getDizzyTime():
                        driver.chef.setDizzy(False)
                        driver.chef.resetDamageChange()

                # checking whether rats are hitting the driver.chef

                    for enemy in enemies:
                        if self.intersects(driver.chef, enemy):

                    # if sdl.hasIntersection(enemy.getRect(), driver.chef.getRect()):
                    # if intersection different things happend depending on if your attacking

                            if driver.chef.getAttacking():
                                if not enemy.getHurt():  # if the rat can take damage
                                    if 'graters' in driver.chef.weapons:
                                        enemy.updateHealth(-2)
                                        self.genericHit()
                                        sdl.mixer.playChannel(-1, graterHit, 0)
                                    else:
                                        enemy.updateHealth(-1)
                                        self.genericHit()
                                        sdl.mixer.playChannel(-1, ladleHit, 0)
                                    enemy.goOppositeDirection(time)
                                    enemy.setHurt(True)
                                    enemy.setHurtTime(time + 1000)
                                    enemy.bump(driver.chef.getAttackingDirection(enemy))
                                    camera.activateShake(currentTime, 200, 3, 3)
                            else:
                                if driver.chef.getCanBeHit():
                                    if not enemy.getHurt():  # hurt rats can't damage us
                                        driver.chef.setCanBeHit(False)
                                        driver.chef.setDizzy(True)
                                        driver.chef.setCanBeHitTime(time
        + 3000)
                                        driver.chef.setDizzyTime(time
        + 750)
                                        driver.chef.bump(enemy.getAttackingDirection(driver.chef))  # finds out what direction the rats should attack from
                                        enemy.setAttackingTime(time
        + 500)
                                        if hittable:
                                            self.playHitSound()
                                            driver.chef.updateHealth(-2)
                                        enemy.goOppositeDirection(time)
                                        camera.activateShake(currentTime, 300, 10, 10)

                # if rat gets hit five times by bumping, it dies

                    for enemy in enemies:
                        if enemy.health <= 0:
                            num = random.randint(1, 12)
                            if num is 1:
                                objects.append(Object(
                                    enemy.xPos + enemy.getWidth() // 2,
                                    enemy.yPos + enemy.getHeight()
    // 2,
                                    50,
                                    50,
                                    'heart',
                                    objectTextures[1],
                                    ))
                            elif num > 1 and num <= 3:
                                objects.append(Object(
                                    enemy.xPos,
                                    enemy.yPos,
                                    50,
                                    50,
                                    'pizza',
                                    objectTextures[0],
                                    ))
                            elif num > 3 and num <= 4:
                                objects.append(Object(
                                    enemy.xPos,
                                    enemy.yPos,
                                    50,
                                    50,
                                    'bombObject',
                                    objectTextures[4],
                                    ))
                            tsum = currentTime + explosionLife
                            emit = self.addEmitter(enemy.xPos
                                    + enemy.getWidth() // 2, enemy.yPos
                                    + enemy.getHeight() // 2, tsum,
                                    'rat')
                            emit.emit()
                            emitters.append(emit)
                            enemies.remove(enemy)
                            sdl.mixer.playChannel(-1, ratDyingSound, 0)
                            driver.scoreBoard.updateScore(5000)

                # score goes down at a set rate, encourages speed

                    driver.scoreBoard.updateScore(-1 * dt)

                # update driver.chef position based on what keys are being pressed
                # down if keys are pressed down and he is not off the screen
                # also based on if driver.chef collides into stuff

                    driver.chef.updatePosition(accumulator, map,
                            keyPress)
                    for projectile in driver.chef.projectiles:
                      projectile.updatePosition(accumulator)

                    self.chefNode = driver.chef.getNode(self.navGraph)

                # boing sound if the driver.chef hits the wall
                # if self.checkCollisions(driver.chef, objects):
                #  sdl.mixer.playMusic(boingSound, 1)

                # update enemy positions based on direction
                # if currentTime >= 10000:
                # if r is True:

                    for enemy in enemies:
                        enemy.updatePosition(accumulator, map, self.navGraph,
                                self.chefNode, time)
                    ratCount += 1
                    ratCount %= 180
                    accumulator -= framerate

            camera.display(currentTime, dt, keyPress, time)
            sdl.renderPresent(driver.renderer)
