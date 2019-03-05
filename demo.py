# Very simple SDL demo in Python.
#
# Sorry, this is not in a great state but I had to push it out to you. There is
# a lot of error checking that I ignore and a lot of things could be
# refactored. But at least you have something to go on for Assignment 1!

import sdl
import math

time2 = 0
width, height = 800, 600
window = None
renderer = None
title = "lol"

music = None
texture = None
font = None
font2 = None

def center(large, small):
    return large//2 - small//2


def centeredRect(largeW, largeH, smallW, smallH):
    return sdl.Rect((
        center(largeW, smallW), center(largeH, smallH),
        smallW, smallH
    ))

def textureSize(t):
    _, _, _, width, height = sdl.queryTexture(t)
    return width, height


def load():
    global music

    #music = sdl.mixer.loadMUS("sunlight.xm")
    image = sdl.image.load("magnet.jpg")
    character = sdl.image.load("chef-sprite.png")
    global texture
    global chefTexture
    texture = renderer.createTextureFromSurface(image)
    chefTexture = renderer.createTextureFromSurface(character)
    global font
    font = sdl.ttf.openFont("Pacifico.ttf", 72)

def cleanup():
    if font is not None:
        sdl.ttf.closeFont(font)
    if music is not None:
        sdl.mixer.freeMusic(music)
    if renderer is not None:
        sdl.destroyRenderer(renderer)
    if window is not None:
        sdl.destroyWindow(window)
    sdl.ttf.quit()
    sdl.mixer.closeAudio()
    sdl.quit()

def run():
    running = True
    lastTime = 0
    time = 0
  
    up = False
    down = False
    left = False
    right = False
    

    event = sdl.Event()
    xPos = 100
    yPos = 100
    size = 200
    while running:

        currentTime = sdl.getTicks()
        dt = currentTime - lastTime
        time += dt/1000.0
        lastTime = currentTime

        textureW, textureH = textureSize(texture)
        textureRect = centeredRect(width, height, textureW, textureH)

	#Figure out what keys are being pressed
        while sdl.pollEvent(event):
           if event.type == sdl.QUIT:
                running = False
           elif event.type == sdl.KEYUP:
                if event.key.keysym.sym in [sdl.K_q, sdl.K_ESCAPE]: running = False
                if event.key.keysym.sym == sdl.K_UP:  up = False
                elif event.key.keysym.sym == sdl.K_DOWN:  down = False
                elif event.key.keysym.sym == sdl.K_LEFT:  left = False
                elif event.key.keysym.sym == sdl.K_RIGHT:  right = False
           if event.type == sdl.KEYDOWN:
              if event.key.keysym.sym == sdl.K_UP: up = True
              elif event.key.keysym.sym == sdl.K_DOWN: down = True
              elif event.key.keysym.sym == sdl.K_LEFT: left = True
              elif event.key.keysym.sym == sdl.K_RIGHT: right = True

           #movement based on what keys are being pressed down
           if up and left: 
             yPos -= 10
             xPos -= 10      
           elif up and right: 
              yPos -= 10
              xPos += 10  
           elif down and left:
              yPos += 10
              xPos -= 10    
           elif down and right: 
              yPos += 10
              xPos += 10  
           elif up: yPos -= 10
           elif down: yPos += 10
           elif left: xPos -= 10
           elif right: xPos += 10

        testRect = sdl.Rect((xPos,yPos,size,size))
        sdl.renderClear(renderer)
        sdl.renderCopy(renderer, texture, None, textureRect)
        sdl.renderCopy(renderer,  chefTexture, None, testRect) 

        testRect = sdl.Rect((xPos,yPos,250,250))


        sdl.renderClear(renderer)

        sdl.renderCopy(renderer, texture, None, textureRect)

        sdl.renderCopy(renderer,  chefTexture, None, testRect)
        sdl.renderPresent(renderer)

if __name__ == "__main__":
    setup()
    load()
    run()
    cleanup()
