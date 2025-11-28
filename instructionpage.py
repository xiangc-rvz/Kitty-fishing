from cmu_graphics import *
class Instruction:
    def __init__(self, game, previousState='menu'):
        self.game = game
        self.previousState = previousState
        self.backgroundPath = '../asset/instruction.png'
        # image source: https://www.pinterest.com/pin/351912465402080/

    def drawIntroBackground(self):
        drawImage(self.backgroundPath, 0, 0, width=400, height=600)

    def isMouseInCloseButton(self,x,y):
        return 315<=x<=355 and 48<=y<=88
    