from cmu_graphics import *

class Playmode:
    def __init__(self, game):
        self.game = game
        self.backgroundPath = '../asset/gamescene.png'
        self.title = 'Main Info'


    def drawMainBackground(self):
        drawImage(self.backgroundPath, 0, 0, width=400, height=600)

    def drawMainInfo(self):
        darkfill = rgb(255, 143, 99)
        lightfill = rgb(250,161,89)

        drawRect(35,20,120,50,fill=darkfill, border ='black')

        drawRect(170,20,20,20,fill=lightfill, border = 'black')
        drawLabel("?", 180,30,size=10, fill='black', bold = True)
        drawRect(170,50,20,20,fill=darkfill,border = 'black', opacity = 60 )
        drawLabel("P", 180,60,size=10, fill='black', bold = True)

    
    def isMouseInInstructionsButton(self,x,y):
        return 170<=x<=190 and 20<=y<=40
    
    def isMouseInPauseButton(self,x,y):
        return 170<=x<=190 and 50<=y<=70
