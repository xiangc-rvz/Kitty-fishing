from cmu_graphics import *
from bag import Bag
from custome import CustomerQueue 
import random
import sys
import os

# --------------------------------------------------------
# AI Tool Used: ChatGPT
# Purpose: Debugging
# Prompt: failed to import Fishingmanager modules but actually write it 
# --------------------------------------------------------
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from score import Countscore
from welcomepage import Mainmenu
from instructionpage import Instruction
from playmode import Playmode
import test  

KittenManager = test.KittenManager
KittenPlayer = test.KittenPlayer
FishingLine = test.FishingLine
FishManager = test.FishManager
Bar = test.Bar
getDistance = test.getDistance
Fish = test.Fish
FishingBait = test.FishingBait


class Game:
    def __init__(self):
        self.countScore = Countscore()
        self.state = 'menu'  
        self.mainMenu = Mainmenu(self)
        self.instruction = Instruction(self)
        self.playMode = Playmode(self)
        self.kittenManager = None  
        self.fishManager = None
        self.fishingLine = None
        self.activeBar = None
        self.phase = "normal"  
        self.phaseTimer = 0
        self.bag = Bag()  
        self.customerQueue = CustomerQueue(self)
        self.backgroundPath = '../asset/GO.png'
        #cat image source: https://www.pinterest.com/pin/77405687340317013/

        self.gameTimer = 0
        self.gameLength = 4500  
        self.showGameOver = False

        self.isPaused = False
        self.showPauseMenu = False

    def initializeGameState(self):
        self.kittenManager = None 
        self.fishManager = None
        self.fishingLine = None
        self.activeBar = None
        self.phase = "normal"
        self.phaseTimer = 0
        self.bag = Bag()
        self.customerQueue = CustomerQueue(self)
        self.countScore.resetScore()
        self.gameTimer = 0
        self.showGameOver = False

        if not self.kittenManager:
            self.kittenManager = KittenManager(self)
            self.fishManager = FishManager(self)
            self.fishingLine = FishingLine(self.kittenManager.getPlayerKitten())
            self.fishingLine.game = self
            self.gameTimer = 0

    def drawPauseMenu(self):
        if self.showPauseMenu:
            lightfill = rgb(250,161,89)
            drawRect(0, 0, 400, 600, fill='black', opacity=30)
            drawRect(100, 200, 200, 200, fill='white', opacity=80)
            drawLabel('Game Paused', 200, 250, size=24, bold=True)
            drawRect(150, 280, 100, 30, fill=lightfill, opacity=80)
            drawLabel('Resume', 200, 295, size=16, bold=True)
            drawRect(150, 320, 100, 30, fill='salmon')
            drawLabel('Main Menu', 200, 335, size=16, bold=True)

    def drawGame(self):
        if self.state == 'menu':
            self.mainMenu.drawMenuBackground()
            self.mainMenu.drawMenuButton()
        elif self.state == 'instructions':
            self.instruction.drawIntroBackground()
        elif self.state == 'game':
            self.playMode.drawMainBackground()
            self.playMode.drawMainInfo()
            timeLeft = max(0, (self.gameLength - self.gameTimer) // 30)
            drawLabel(f'Score: {self.countScore.getScore()}', 90, 35, fill = 'white', bold = True,  size=20)
            drawLabel(f'Time: {timeLeft}s', 95, 55, fill = 'white', bold = True, size=20)
            
            if self.kittenManager:
                self.kittenManager.drawPlayerKitten()
                self.customerQueue.drawCustomers()
                self.bag.drawBag()
                self.fishManager.drawAllFishes()
                self.fishingLine.drawLine()
                if self.activeBar:
                    self.activeBar.drawBar()
            
            if self.showGameOver:
                self.drawGameOver()

            if self.showPauseMenu:
                self.drawPauseMenu()

    def drawGameOver(self):
        drawRect(0, 0, 400, 600, fill='black', opacity=30)
        drawImage(self.backgroundPath, 50, 150, width=300, height=200, opacity=80)
        drawLabel('Game Over!', 200, 200, size=24, bold=True)
        drawLabel(f'Final Score: {self.countScore.getScore()}',200, 250, bold=True, size=20)
        drawLabel('Click anywhere to return to menu', 200, 300, bold=True, size=14)

    def isMousePress(self, mouseX, mouseY):
        if self.showGameOver:
            self.state = 'menu'
            self.resetGame()
            return
        
        if self.state == 'menu':
            if self.mainMenu.isMouseInPlayButton(mouseX, mouseY):
                self.state = 'game'
                self.initializeGameState()
            elif self.mainMenu.isMouseInInstructionsButton(mouseX, mouseY):
                self.instruction = Instruction(self, previousState='menu')
                self.state = 'instructions'
        elif self.state == 'game':
            if self.showPauseMenu:
                if self.showPauseMenu:
                    if 150 <= mouseX <= 250 and 280 <= mouseY <= 310:
                        self.showPauseMenu = False
                        self.isPaused = False
                    
                    elif 150 <= mouseX <= 250 and 320 <= mouseY <= 350:
                        self.state = 'menu'
                        self.showPauseMenu = False
                        self.isPaused = False
                        self.resetGame()
                    return
                
            if self.playMode.isMouseInPauseButton(mouseX, mouseY):
                self.isPaused = not self.isPaused
                self.showPauseMenu = self.isPaused
                return
            
            if self.playMode.isMouseInInstructionsButton(mouseX,mouseY):
                self.instruction = Instruction(self, previousState='game')
                self.state = 'instructions'
            elif self.bag.isMouseInFish(mouseX, mouseY):
                self.bag.startDragging(mouseX, mouseY)
            else:
                self.isGameMousePress(mouseX, mouseY)

        elif self.state == 'instructions':
            if self.instruction.isMouseInCloseButton(mouseX, mouseY):
                self.state = self.instruction.previousState

    def isGameMousePress(self, mouseX, mouseY):
        if self.isPaused:
            return
        if self.fishingLine.currentBait and self.fishingLine.currentBait.touched:
            for fish in self.fishManager.fishes:
                if fish.hasTouchedBait and not fish.isCaught:
                    if getDistance(mouseX, mouseY, fish.x, fish.y) < 50:
                        if self.activeBar is None:
                            self.activeBar = Bar(fish)
                        self.activeBar.increaseProgress()
                        return
        if self.fishingLine.mode == 'mouse':
            self.fishingLine.checkMouseClick(mouseX, mouseY)

# --------------------------------------------------------
# AI Tool Used: ChatGPT
# Purpose: Optimization logic and debugging
# Prompt: The fish stops swimming after it touches the bait but before it is caught
# --------------------------------------------------------

    def updateGame(self):
        if self.state == 'game' and not self.showGameOver and not self.isPaused:
            self.gameTimer += 1
            if self.gameTimer >= self.gameLength:
                self.showGameOver = True
                return
            self.updateGameElements()

    def updateGameElements(self):
        self.customerQueue.update()
        self.fishManager.updateFishes(self.fishingLine.currentBait, self.fishingLine.mode)
        self.fishingLine.update()
        self.updateBar()
    
    def update(self):
        if self.state == 'fishing':
            self.phaseTimer += 1

            if self.phaseTimer <= 150:
                self.phase = "escape"
            elif 150 < self.phaseTimer <= 210:
                self.phase = "transition"
            else:
                self.phase = "normal"

            self.fishManager.updateFishes(self.fishingLine.currentBait, self.phase)

    def resetGame(self):
            self.initializeGameState()

    def handleFishCaught(self, fish): 
        currentCustomer = self.customerQueue.getCurrentCustomer()
        if currentCustomer and fish.color == currentCustomer.targetColor:
            self.customerQueue.removeCurrentCustomer()
            self.countScore.addScore('satisfy_first_customer')
            self.showSuccessMessage = True
        else:
            self.bag.addFish(fish)

    def updateBar(self):
        if self.isPaused:
            return
        if self.activeBar:
            self.activeBar.decreaseProgress()
            if self.activeBar.isComplete():
                self.activeBar.fish.isCaught = True
                self.fishManager.removeFish(self.activeBar.fish)
                self.handleFishCaught(self.activeBar.fish)
                self.activeBar = None
                self.fishingLine.currentBait = None
            elif self.activeBar.progress <= 0:
                self.resetFishState()

    def resetFishState(self):
        if self.fishingLine.mode == 'fishing' and not self.activeBar:
            self.countScore.addScore('cancel_fishing')
        elif self.activeBar and self.activeBar.progress > 0:
            self.fishingLine.fishEscaped = True
            self.countScore.addScore('fish_escaped')
        
        if self.activeBar:
            self.activeBar.fish.hasTouchedBait = False
            self.activeBar.fish.dx = random.randint(-3, 3)
            self.activeBar.fish.dy = random.randint(-2, 2)
            self.activeBar.fish.isAttracted = False
        
        self.activeBar = None
        self.fishingLine.currentBait = None
        self.fishingLine.mode = 'idle'
        self.fishingLine.resetToIdle()

    def isKeyPress(self, key):
        if self.state == 'game':
            currentKitten = self.kittenManager.getPlayerKitten()
            if not currentKitten or (self.fishingLine.mode == 'fishing' and key != 'space'):
                return
            if key == 'left': currentKitten.move(-10, 0)
            elif key == 'right': currentKitten.move(10, 0)
            elif key == 'up': currentKitten.move(0, -10)
            elif key == 'down': currentKitten.move(0, 10)
            elif key == 'r': self.fishingLine.mode = 'swing'
            elif key == 'c': self.fishingLine.mode = 'mouse'
            elif key == 'k': self.fishingLine.shootLine()
            elif key == 'space': self.fishingLine.resetToIdle()
            elif key == 's': self.fishingLine.switchColor()

    def isMouseMove(self, mouseX, mouseY):
        if self.state == 'game' and not self.isPaused:
            self.bag.updateDragging(mouseX, mouseY)
            if self.fishingLine.mode == 'mouse':
                self.fishingLine.followMouse(mouseX, mouseY)
    
    def isMouseRelease(self, mouseX, mouseY):
        if self.state == 'game' and not self.isPaused:
            self.bag.stopDragging(mouseX, mouseY, self.customerQueue)
