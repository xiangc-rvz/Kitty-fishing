from cmu_graphics import *
class Bag:
    def __init__(self):
        self.fishes = {}  
        self.x = 300
        self.y = 10
        self.isDragging = False
        self.draggedFish = None
        self.dragX = 0
        self.dragY = 0

    def isMouseInFish(self, mouseX, mouseY):
        index = 0  
        for color, count in self.fishes.items():
            if count > 0:  
                fishX = self.x + 15
                fishY = self.y + index * 25 + 20
                if (fishX <= mouseX <= fishX + 20 and 
                    fishY <= mouseY <= fishY + 20):
                    return color
                index += 1  
        return None

    def startDragging(self, mouseX, mouseY):
        fishColor = self.isMouseInFish(mouseX, mouseY)
        if fishColor:
            self.isDragging = True
            self.draggedFish = fishColor
            self.dragX = mouseX
            self.dragY = mouseY

    def updateDragging(self, mouseX, mouseY):
        if self.isDragging:
            self.dragX = mouseX
            self.dragY = mouseY

    def stopDragging(self, mouseX, mouseY, customerQueue):
        if self.isDragging:
            customer = customerQueue.getCustomerAtPosition(mouseX, mouseY)
            if customer and customer.targetColor == self.draggedFish:
                if self.removeFish(self.draggedFish):
                    customerQueue.satisfyCustomer(customer)
            self.isDragging = False
            self.draggedFish = None

    def addFish(self, fish):
        color = fish.color
        self.fishes[color] = self.fishes.get(color, 0) + 1

    def removeFish(self, color):
        if color in self.fishes and self.fishes[color] > 0:
            self.fishes[color] -= 1
            return True
        return False

# --------------------------------------------------------
# AI Tool Used: ChatGPT
# Purpose: Optimization logic and debugging
# Prompt: helping improve showing what in the bag 
# --------------------------------------------------------

    def drawBag(self):
        drawRect(self.x + 10, self.y, 80, 180, fill=None, border = 'black')
        drawRect(self.x + 10, self.y, 80, 180, fill='white', opacity=30) #bag background
        drawLabel('BAG', self.x + 50, self.y + 15, size=14)
        
        index = 0
        for color, count in self.fishes.items():
            if count > 0:
                drawRect(self.x +15, self.y + index * 25 + 25, 20, 20, fill=color, border = 'black')
                drawCircle(self.x+22, self.y+35+index * 25, 2, fill='black')
                drawLabel(f'x{count}', self.x + 50, self.y + index * 25 + 30)
                index += 1
        
        if self.isDragging:
            drawRect(self.dragX - 10, self.dragY - 10, 20, 20,
                    fill=self.draggedFish, opacity=0)