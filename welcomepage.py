from cmu_graphics import *
class Mainmenu:
    def __init__(self, game):
        self.game = game
        self.playButtonColor = 'pink'
        self.instructionsButtonColor = 'pink'
        self.backgroundPath = '../asset/fishing-cat.png'
#The kitten picture material comes from: https://www.pinterest.com/pin/775885842080065690/
    
    def drawMenuBackground(self):
        drawImage(self.backgroundPath, 0, 0, width=400, height=600)

    def drawMenuButton(self):
        drawRect(130,353,140,50,fill=self.playButtonColor, opacity=0, border = 'white', borderWidth = 5)
        drawRect(130,421,140,50,fill=self.instructionsButtonColor, opacity=0)

    def isMouseInPlayButton(self,x,y):
        return 130<=x<=270 and 353<=y<=403
    
    def isMouseInInstructionsButton(self,x,y):
        return 130<=x<=270 and 421<=y<=471



