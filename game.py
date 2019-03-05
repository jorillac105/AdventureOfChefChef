import sys
sys.path.insert(0, 'entities/')
sys.path.insert(0, 'states/')
import sdl
import math
import random
import MCClass as MC
import rats
import driver
from levelZero import LevelZero
from levelTwo import LevelTwo
from levelThree import LevelThree
from levelFour import LevelFour
from levelFive import LevelFive
from pvp import Pvp
from titleScreen import TitleScreen
from menuScreen import MenuScreen
from gameOver import GameOver
from winScreen import WinScreen
from highScoreScreen import HighScore
from controlScreen import Controls
from options import Options

time2 = 0
width, height = 800, 600
window = None
renderer = None
title = "The Legend of Chef Chef"

music = None
texture = None


curState = TitleScreen()

def changeState(s):
    if s == "menu":
        mS = MenuScreen()
        return mS
    elif s == "levelZero":
        l0 = LevelZero()
        return l0
    elif s == "gameOver":
        gO = GameOver()
        return gO
    elif s == "youWin":
        yW =  WinScreen()
        return yW
    elif s == "levelTwo":
        l2 = LevelTwo()
        return l2
    elif s == "levelThree":
        l3 = LevelThree()
        return l3
    elif s == "levelFour":
        l4 = LevelFour()
        return l4
    elif s == "levelFive":
        l5 = LevelFive()
        return l5
    elif s == "pvp":
        l6 = Pvp()
        return l6
    elif s == "highScore":
        hS = HighScore()
        return hS
    elif s == "controls":
        cT = Controls()
        return cT
    elif s == "options":
        oP = Options()
        return oP

def turnOff():
    driver.off = True

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


if __name__ == "__main__":
    driver.setup()
    while not driver.off:
        curState.load()
        curState.run()
        curState.cleanup()
        if not curState.next == None:
            curState = changeState(curState.next)
    driver.cleanup()
