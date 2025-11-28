from cmu_graphics import *
from tools import Game

def onAppStart(app):
    app.game = Game()

def redrawAll(app):
    app.game.drawGame()

def onMousePress(app, mouseX, mouseY):
    app.game.isMousePress(mouseX, mouseY)

def onStep(app):
    app.game.updateGame()

def onKeyPress(app, key):
    app.game.isKeyPress(key)

def onMouseMove(app, mouseX, mouseY):
    app.game.isMouseMove(mouseX, mouseY)

def onMouseRelease(app, mouseX, mouseY):
    app.game.isMouseRelease(mouseX, mouseY)

runApp(width=400, height=600)

