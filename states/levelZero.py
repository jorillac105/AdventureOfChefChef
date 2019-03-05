import sys
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
import math
import navGraph
from emitter import Emitter
from object import Object
from camera import Camera
from structure import Structure
from story import Story
from base import Base
from pauseMenu import Pause
from instructions import Instruct



class LevelZero(BasicState):

    def __init__(self):
        self.next = None

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
        global ratDyingSound, getOut, hitGeneric, woosh
        global hit
        global ladleHit
        global story1, story2
        story1 = Story(1)
        story2 = Story(2)
        story1.load()
        story2.load()
        story1.run()

    # driver.loading.run()

    # assigning music channels

        sdl.mixer.allocateChannels(5)
        music = sdl.mixer.loadMUS('music/songs/level1music.xm')
        ratDyingSound = \
            sdl.mixer.loadWAV_RW(sdl.RWFromFile('music/chunks/rat_death.mp3'
                                 , 'rw'), 0)
        getOut = \
            sdl.mixer.loadWAV_RW(sdl.RWFromFile('music/chunks/get_out_you_dirty_rats.wav'
                                 , 'rw'), 0)

        hit = []
        for i in range(3):
            hit.append(sdl.mixer.loadWAV_RW(sdl.RWFromFile('music/chunks/hit'
                        + str(i) + '.wav', 'rw'), 0))
        ladleHit =  sdl.mixer.loadWAV_RW(sdl.RWFromFile('music/chunks/ladle_hit.wav', 'rw'), 0)
        hitGeneric =  sdl.mixer.loadWAV_RW(sdl.RWFromFile('music/chunks/hit.wav', 'rw'), 0)
        woosh = sdl.mixer.loadWAV_RW(sdl.RWFromFile('music/chunks/woosh.wav', 'rw'), 0)

        ratImages = [
            sdl.image.load('graphics/sprites/rat_hurt.png'), #0
            sdl.image.load('graphics/sprites/rat_up.png'),
            sdl.image.load('graphics/sprites/rat_right.png'), #2
            sdl.image.load('graphics/sprites/rat_down.png'),
            sdl.image.load('graphics/sprites/rat_left.png'), #4
            sdl.image.load('graphics/sprites/rat_attack_up.png'),
            sdl.image.load('graphics/sprites/rat_attack_right.png'), #6
            sdl.image.load('graphics/sprites/rat_attack_down.png'),
            sdl.image.load('graphics/sprites/rat_attack_left.png'), #8
            sdl.image.load('graphics/items/cheese.png'),
            sdl.image.load('graphics/ui/light.png'), #10
            ]

    # array of tiles used throughout the map

        mapImages = []
        for x in range(1, 32):
            mapImages.append(sdl.image.load('graphics/map/' + str(x)
                             + '.png'))

        objectImages = []
        objectImages.append(sdl.image.load('graphics/items/pizza_animation.png'
                            ))
        objectImages.append(sdl.image.load('graphics/items/heart_animation.png'
                            ))
        objectImages.append(sdl.image.load('graphics/items/carrot_animation.png'
                            ))
        objectImages.append(sdl.image.load('graphics/items/key_animation.png'
                            ))

        weaponImages = []
        weaponImages.append(sdl.image.load('graphics/items/ladles.png'))
        weaponImages.append(sdl.image.load('graphics/items/graters.png'
                            ))

        pantryImages = [
            sdl.image.load('graphics/items/open_pantry.png'),
            sdl.image.load('graphics/items/pantry_open.png'),
            sdl.image.load('graphics/messages/press_open.png'),
            sdl.image.load('graphics/items/open_pantry_key.png'),
            sdl.image.load('graphics/messages/found_key.png'),
            sdl.image.load('graphics/messages/basement_locked.png'),
            ]

        pantryTextures = []
        for x in range(len(pantryImages)):
            pantryTextures.append(driver.renderer.createTextureFromSurface(pantryImages[x]))
            sdl.freeSurface(pantryImages[x])

    # creates an array of arrays of integrets that represents our map's floor

        global map
        map = []
        with open('data/map.txt') as f:
            for line in f:
                currentLine = []
                split = line.split()
                for value in line.split():
                    currentLine.append(int(value))
                map.append(currentLine)

    # fill up the objects array which contains the objects that can be collided with

        global structures
        structures = []
        count = 0
        for j in range(len(map)):
            for i in range(len(map[j])):
                value = map[j][i]
                if value is 27:
                    if count is 0:
                        struct = Structure(
                            value,
                            i,
                            j,
                            pantryTextures,
                            True,
                            'pantry',
                            )
                        count += 1
                    else:
                        struct = Structure(
                            value,
                            i,
                            j,
                            pantryTextures,
                            False,
                            'pantry',
                            )
                    structures.append(struct)
                elif value is (2 or 3):
                    structures.append(Structure(
                        value,
                        i,
                        j,
                        pantryTextures,
                        False,
                        'stairs',
                        ))
                elif value is not 1:
                    structures.append(Structure(
                        value,
                        i,
                        j,
                        None,
                        False,
                        None,
                        ))

        #a graph of every tile mapped to every one of its neighbors

        self.navGraph = navGraph.navGraph(map, {1}, 1)

    # for now just stuff that's dropped by the rats

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
        mapTextures = []
        for x in range(len(mapImages)):
            mapTextures.append(driver.renderer.createTextureFromSurface(mapImages[x]))
            sdl.freeSurface(mapImages[x])


        driver.scoreBoard.clearScore()
        driver.scoreBoard.updateScore(100000)

    # driver.loading.cleanup()

    def cleanup(self):
        story1.cleanup()
        story2.cleanup()
        if music is not None:
            sdl.mixer.freeMusic(music)
        for x in range(len(hit)):
            if hit[x] is not None:
                sdl.mixer.freeChunk(hit[x])
        if getOut is not None:
            sdl.mixer.freeChunk(getOut)

        if ratDyingSound is not None:
            sdl.mixer.freeChunk(ratDyingSound)

        if ladleHit is not None:
            sdl.mixer.freeChunk(ladleHit)

        if hitGeneric is not None:
            sdl.mixer.freeChunk(hitGeneric)

        if woosh is not None:
            sdl.mixer.freeChunk(woosh)

        for x in range(len(ratTextures)):
            if ratTextures[x] is not None:
                sdl.destroyTexture(ratTextures[x])

        for x in range(len(mapTextures)):
            if mapTextures[x] is not None:
                sdl.destroyTexture(mapTextures[x])

        for x in range(len(objectTextures)):
            if objectTextures[x] is not None:
                sdl.destroyTexture(objectTextures[x])

    def playHitSound(self):
        i = random.randint(0, 2)
        sdl.mixer.playChannel(0, hit[0], 0)
        self.genericHit()

    def genericHit(self):
        sdl.mixer.playChannel(-1, hitGeneric, 0)

    def createRandomRat(self, directions, time):
        enemySpeed = 0.05

      # xPosition = 500 #random.randint(600, 601)
      # yPosition = 450 #random.randint(450, 451)

        xPosition = random.randint(0, len(map[0]) - 1)
        yPosition = random.randint(0, len(map) - 1)

        direction = directions[random.randint(0, 7)]
        rat = rats.Enemy(xPosition * 50, yPosition * 50, 50, 60, direction, enemySpeed, 3, 1, time, self.navGraph)

        while rat.checkCollisions(rat.getImmediateSurroundings(map)):
            yPosition = random.randint(0, len(map) - 1)
            xPosition = random.randint(0, len(map[0]) - 1)
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

    def run(self):
        driver.chef.resetChef()
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

      # space = attack

        space = False

      # r = release the rats

        r = False

      # use = use interactible structure

        use = False

      # paused = whether or not the game is paused

        paused = False

      # list of enemies

        enemies = []

      # list of emitters

        emitters = []
        explosionLife = 500

        event = sdl.Event()

      # add the carrot

        objects.append(Object(
            1500,
            600,
            50,
            50,
            'carrot',
            objectTextures[2],
            ))

      # add the ladle bject

        objects.append(Object(
            500,
            650,
            50,
            50,
            'ladles',
            objectTextures[4],
            ))

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
            1,
            None,
            None
            )
        pauseMenu = Pause(camera)

        instructionScreen = Instruct(camera)
        instr = False
        global item

        # create 5 randomly placed enemies moving in a random direction at enemySpeed

        #self.chefNode = self.navGraph.getNode(driver.chef.xPos//50, driver.chef.yPos//50)
        self.chefNode = driver.chef.getNode(self.navGraph)
        currentTime = sdl.getTicks()
        for i in range(3):
            enemies.append(self.createRandomRat(directions, currentTime))

        sdl.renderPresent(driver.renderer)

        frames = 0
        keyPress = False
        sdl.mixer.playChannel(2, getOut, 0)
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
                                if driver.chef.yPos <= 50 and driver.chef.xPos \
                                >= len(map[0]) * 50 - 150 and driver.chef.xPos \
                                <= len(map[0]) * 50 - 100 and 'key' \
                                in driver.chef.items and len(enemies) is 0:

                                    running = False
                                    driver.chef.items.remove('key')
                                    driver.chef.score = driver.scoreBoard.getScore()
                                    self.next = 'levelTwo'
                                    story2.run()
                                    return
                                use = False
                            elif event.key.keysym.sym == sdl.K_z:
                                z = False
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
                            elif event.key.keysym.sym == sdl.K_RETURN:
                                use = True
                            elif event.key.keysym.sym == sdl.K_h:

                      # Debug: add 100 health

                                driver.chef.setCanBeHit(False)
                                driver.chef.setDizzy(True)
                                driver.chef.setCanBeHitTime(currentTime + 3000)
                                driver.chef.setDizzyTime(currentTime + 750)
                                driver.chef.updateHealth(8)
                            elif event.key.keysym.sym == sdl.K_l:
                                enemies.append(self.createRandomRat(directions,
                                        time))
                            elif event.key.keysym.sym == sdl.K_m:
                                running = False
                                self.next = 'menu'
                            # Debug: go to level 2
                            elif event.key.keysym.sym == sdl.K_2:
                                running = False
                                if 'key' in driver.chef.items:
                                    driver.chef.items.remove('key')
                                driver.chef.score = \
                                    driver.scoreBoard.getScore()
                                self.next = 'levelTwo'
                                story2.run()
                                return
                            # Debug: go to level 3
                            elif event.key.keysym.sym == sdl.K_3:
                                running = False
                                if 'key' in driver.chef.items:
                                    driver.chef.items.remove('key')
                                driver.chef.score = \
                                    driver.scoreBoard.getScore()
                                self.next = 'levelThree'
                                story2.run()
                                return
                            # Debug: go to level 4
                            elif event.key.keysym.sym == sdl.K_4:
                                running = False
                                if 'key' in driver.chef.items:
                                    driver.chef.items.remove('key')
                                driver.chef.score = \
                                    driver.scoreBoard.getScore()
                                self.next = 'levelFour'
                                story2.run()
                            # Debug: go to level 5
                            elif event.key.keysym.sym == sdl.K_5:
                                running = False
                                if 'key' in driver.chef.items:
                                    driver.chef.items.remove('key')
                                driver.chef.score = \
                                    driver.scoreBoard.getScore()
                                self.next = 'levelFive'
                                story2.run()
                            # Debug: go to pvp level
                            elif event.key.keysym.sym == sdl.K_6:
                                running = False
                                if 'key' in driver.chef.items:
                                    driver.chef.items.remove('key')
                                driver.chef.score = \
                                    driver.scoreBoard.getScore()
                                self.next = 'pvp'
                                story2.run()
                            # Debug: toggle the carrot item
                            elif event.key.keysym.sym == sdl.K_w:
                                if 'carrot' not in driver.chef.items:
                                    driver.chef.addItem('carrot')
                                else:
                                    driver.chef.removeItem('carrot')
                            # Debug: toggle the key item
                            elif event.key.keysym.sym == sdl.K_k:
                                if 'key' not in driver.chef.items:
                                    driver.chef.addItem('key')
                                else:
                                    driver.chef.removeItem('key')
                            elif event.key.keysym.sym == sdl.K_e:
                                tsum = currentTime + explosionLife
                                emit = self.addEmitter(driver.chef.xPos
                                        + driver.chef.getWidth() // 2,
                                        driver.chef.yPos
                                        + driver.chef.getHeight() // 2,
                                        tsum, 'explosion')
                                emit.emit()
                                emitters.append(emit)
                            elif event.key.keysym.sym == sdl.K_p:
                                paused = True

                    keyPress = left or right or up or down

                # based on the keys pressed down set the driver.chef's direction

                    if keyPress is True:
                        driver.chef.updateDirection(up, down, left,
                                right)

                # pressing space on keydown will place the player into attacking state

                    if space and currentTime > driver.chef.getAttackingTime() \
                        and len(driver.chef.weapons) is not 0:
                        if driver.chef.getEnergy() > 0:
                            driver.chef.setAttacking(True)
                            driver.chef.setAttackingTime(currentTime + 300)  # attacking animation with be 1s
                            driver.chef.updateEnergy(-1)
                            sdl.mixer.playChannel(-1, woosh, 0)
                        else:

                    # If you try to attack when you're out of energy, become dizzy for .5s

                            driver.chef.setDizzy(True)
                            driver.chef.setDizzyTime(currentTime + 500)


                # if the player presses "space" the driver.chef will go into attacking mode
                # which overrides other animations except getting hit

                    if currentTime > driver.chef.getAttackingTime() \
                        or driver.chef.getDizzy():
                        driver.chef.setAttacking(False)
                    else:
                        driver.chef.setAttacking(True)
                        driver.chef.setEnergyRegenTime(currentTime + 1000)

                # if the player is not attacking, and less than 8 pizza slices, and not dizzy, and 3s from last time attacked, give energy

                    if not space and driver.chef.getEnergy() < 8 \
                        and not driver.chef.getDizzy() and currentTime \
                        > driver.chef.getEnergyRegenTime():
                        driver.chef.updateEnergy(1)
                        driver.chef.setEnergyRegenTime(currentTime + 1000)

                # if driver.chef not attacking or dizzy, and on same tile as object, pick it up

                    if currentTime > driver.chef.getAttackingTime() \
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
                                    objects.remove(obj)
                                    if not driver.chef.inGottenItems('graters'):
                                        instr = True
                                        driver.chef.setGottenItems('graters')
                                        item = 'graters'

                # make sure the rats aren't invulnable after a set time

                    for enemy in enemies:
                        if currentTime > enemy.getHurtTime():
                            enemy.setHurt(False)
                            enemy.resetDamageChange()

                    for pantry in structures:
                        if pantry.identity is 'pantry' \
                            and pantry.triggered is False:
                            pantry.xPos *= 50
                            pantry.yPos *= 50
                            pantry.yPos += 20
                            if self.intersects(driver.chef, pantry):
                                if pantry.visible is False:
                                    pantry.changeVisibility()
                            else:
                                if pantry.visible:
                                    pantry.changeVisibility()

                            pantry.xPos /= 50
                            pantry.yPos -= 20
                            pantry.yPos /= 50
                            if pantry.visible:
                                if use is True:
                                    pantry.triggerAction()
                                    if pantry.hasKey is True:
                                        driver.chef.items.append('key')
                                        instr = True
                                        driver.chef.setGottenItems('key')
                                        item = 'key'
                                    else:

                        # randomly give either pizza or hearts

                                        randNum = random.randint(1, 10)
                                        if randNum is 1:
                                            objects.append(Object(
                                                enemy.xPos
    + enemy.getWidth() // 2,
                                                enemy.yPos
    + enemy.getHeight() // 2,
                                                50,
                                                50,
                                                'heart',
                                                objectTextures[1],
                                                ))
                                        elif randNum > 1 and randNum <= 4:
                                            objects.append(Object(
                                                pantry.xPos * 50,
                                                pantry.yPos * 50 + 50,
                                                50,
                                                50,
                                                'pizza',
                                                objectTextures[0],
                                                ))
                        elif pantry.identity is 'stairs':
                            if 'key' not in driver.chef.items:
                                pantry.xPos *= 50
                                pantry.xPos -= 50
                                pantry.yPos *= 50
                                if self.intersects(driver.chef, pantry):
                                    if pantry.visible is False:
                                        pantry.changeVisibility()
                                else:
                                    if pantry.visible is True:
                                        pantry.changeVisibility()
                                pantry.xPos += 50
                                pantry.xPos /= 50
                                pantry.yPos /= 50

                # make sure the rats aren't attacking after a set time

                    for enemy in enemies:
                        if currentTime > enemy.getAttackingTime():
                            enemy.setAttacking(0)

                # if the invulnability expired set hit back to true

                    if currentTime > driver.chef.getCanBeHitTime():
                        driver.chef.setCanBeHit(True)

                # if the dizzyness expired, set dizzy back to false

                    if currentTime > driver.chef.getDizzyTime():
                        driver.chef.setDizzy(False)
                        driver.chef.resetDamageChange()

                # checking whether rats are hitting the driver.chef

                    for enemy in enemies:
                        if self.intersects(driver.chef, enemy):

                    # if sdl.hasIntersection(enemy.getRect(), driver.chef.getRect()):
                    # if intersection different things happend depending on if your attacking

                            if driver.chef.getAttacking():
                                if not enemy.getHurt():  # if the rat can take damage
                                    enemy.updateHealth(-1)
                                    enemy.goOppositeDirection(currentTime)
                                    enemy.setHurt(True)
                                    enemy.setHurtTime(currentTime + 1000)
                                    enemy.bump(driver.chef.getAttackingDirection(enemy))
                                    self.genericHit()
                                    sdl.mixer.playChannel(-1, ladleHit, 0)
                                    camera.activateShake(currentTime, 200, 3, 3)

                            else:
                                if driver.chef.getCanBeHit():
                                    if not enemy.getHurt():  # hurt rats can't damage us
                                        driver.chef.setCanBeHit(False)
                                        driver.chef.setDizzy(True)
                                        driver.chef.setCanBeHitTime(currentTime
        + 3000)
                                        driver.chef.setDizzyTime(currentTime
        + 750)
                                        driver.chef.bump(enemy.getAttackingDirection(driver.chef))
                                        enemy.setAttackingTime(currentTime
        + 500)
                                        self.playHitSound()
                                        driver.chef.updateHealth(-1)
                                        camera.activateShake(currentTime, 300, 5, 5)
                                        enemy.goOppositeDirection(currentTime)

                # if rat gets hit five times by bumping, it dies

                    for enemy in enemies:
                        if enemy.health <= 0:
                            int = random.randint(1, 6)
                            if int is 1:
                                objects.append(Object(
                                    enemy.xPos + enemy.getWidth() // 2,
                                    enemy.yPos + enemy.getHeight()
    // 2,
                                    50,
                                    50,
                                    'heart',
                                    objectTextures[1],
                                    ))
                            elif int > 1 and int <= 3:
                                objects.append(Object(
                                    enemy.xPos,
                                    enemy.yPos,
                                    50,
                                    50,
                                    'pizza',
                                    objectTextures[0],
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

                    self.chefNode = driver.chef.getNode(self.navGraph)

                    #x, y = self.chefNode.getPos()

                    #print ("CHEFNODE = ", x,", ",y)

                # update enemy positions based on direction
                # if currentTime >= 10000:
                # if r is True:

                    for enemy in enemies:
                        enemy.updatePosition(accumulator, map, self.navGraph,
                                self.chefNode, currentTime)
                    accumulator -= framerate

            camera.display(currentTime, dt, keyPress, time)
            sdl.renderPresent(driver.renderer)
