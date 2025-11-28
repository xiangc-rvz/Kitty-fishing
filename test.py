from cmu_graphics import *
import random
import math
import time

def getDistance(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

def calculateEndPoint(startX, startY, angle, length):
    endX = startX + math.cos(math.radians(angle)) * length
    endY = startY + math.sin(math.radians(angle)) * length
    return endX, endY

class Fish:
    def __init__(self,x=None,y=None):
        self.color = random.choice(['red', 'orange', 'yellow', 'green', 'blue', 'purple'])
        self.x = x if x is not None else random.randint(25, 375)
        self.y = y if y is not None else random.randint(360, 575)

        self.speed = 1
        self.dx = random.choice([-self.speed, self.speed])
        self.dy = random.randint(-1, 1)
        self.facingLeft = self.dx < 0
        
        self.isAttracted = False
        self.hasTouchedBait = False
        self.isCaught = False
        
        self.tailAngle = 0  
        self.tailSwingSpeed = 2  
        self.tailMaxAngle = 20  
        self.tailDirection = 1
        self.targetTailAngle = 0 

        self.isEscaping = False
        self.escapeTimer = 0
        self.postEscapeTimer = 0
        self.escapeSpeed = 5
        self.fishingModeStartTime = 0
        self.isFishingMode = False

        self.hitCount = 0  
        self.hitCooldown = 0 
        self.isHitting = False 
        self.maxHits = 2 
        self.hitTimer = 0  

    def drawFish(self):
        if not self.isCaught:
            drawOval(self.x, self.y,35,20, fill=self.color, border = 'black')
            eyeX = self.x - 5 if self.facingLeft else self.x + 5
            drawCircle(eyeX, self.y, 2, fill='black')
            
            baseX = self.x + 15 if self.facingLeft else self.x - 15
            baseY = self.y

            angle = math.radians(self.tailAngle if self.facingLeft else 180 + self.tailAngle)
            tailLength = 25

            topX = baseX + tailLength * math.cos(angle - math.radians(30))
            topY = baseY + tailLength * math.sin(angle - math.radians(30))
            bottomX = baseX + tailLength * math.cos(angle + math.radians(30))
            bottomY = baseY + tailLength * math.sin(angle + math.radians(30))
            
            drawPolygon(baseX, baseY, topX, topY, bottomX, bottomY, 
                       fill=self.color, border='black', opacity=70)

    def swim(self):
        if not self.hasTouchedBait:
            self.x += self.dx
            self.y += self.dy

            hitBoundary = False

            if self.x <= 35:
                self.x = 35
                if self.dx < 0:
                    self.dx = self.speed
                    hitBoundary = True
            elif self.x >= 365:
                self.x = 365
                if self.dx > 0:
                    self.dx = -self.speed
                    hitBoundary = True

            if self.y <= 355:
                self.y = 355
                self.dy = abs(self.dy)
            elif self.y >= 580:
                self.y = 580
                self.dy = -abs(self.dy)

            if self.dx == 0 and self.dy == 0:
                self.dx = random.choice([-self.speed, self.speed])
                self.dy = random.randint(-1, 1)

            self.facingLeft = self.dx < 0
            self.updateTail(hitBoundary)
    
    def updateTail(self, hitBoundary):
        if hitBoundary:
            self.tailAngle = 0
            self.tailDirection = 1
        else:
            self.tailAngle += self.tailSwingSpeed * self.tailDirection
            if abs(self.tailAngle) >= self.tailMaxAngle:
                self.tailDirection *= -1

    def isEscape(self, bait):
        if bait is None:
            self.swim()
            return
            
        distance = getDistance(self.x, self.y, bait.x, bait.y)
        if distance > 0:
            escapeSpeed = 5
            self.dx = (self.x - bait.x) / distance * escapeSpeed
            self.dy = (self.y - bait.y) / distance * escapeSpeed
            
        self.x += self.dx
        self.y += self.dy
        
        if self.x <= 35:
            self.x = 35
            self.dx = abs(self.dx)
        elif self.x >= 365:
            self.x = 365
            self.dx = -abs(self.dx)
            
        if self.y <= 355:
            self.y = 355
            self.dy = abs(self.dy)
        elif self.y >= 580:
            self.y = 580
            self.dy = -abs(self.dy)

        self.facingLeft = self.dx < 0
        self.updateTail(False)
        
    def moveTowardsPoint(self, point, fishingMode='idle'):
        if point is None:
            self.swim()
            return False
        
        if fishingMode != 'fishing':
            self.swim()
            return False
        
        if fishingMode == 'fishing':
            if not point.touched and self.color == point.color:
                distance = getDistance(self.x, self.y, point.x, point.y)
                
                if self.isHitting:
                    if self.hitCooldown > 0:
                        self.hitCooldown -= 1
                        self.dx = self.dy = 0

                    else:
                        if distance < 10:
                            if not self.hasTouchedBait:
                                self.hitCount += 1
                                self.hitCooldown = 30 
                    
                                dx = self.x - point.x
                                dy = self.y - point.y
                                magnitude = (dx**2 + dy**2)**0.5 
                                if magnitude > 0:
                                    self.dx = (dx / magnitude) * 2
                                    self.dy = (dy / magnitude) * 2

                                if self.hitCount >= self.maxHits:
                                    self.hasTouchedBait = True
                                    self.dx = self.dy = 0
                                    point.touched = True
                                    point.touchedFish = self
                                    return True
                        else:
        
                            dx = point.x - self.x
                            dy = point.y - self.y
                            magnitude = (dx**2 + dy**2)**0.5
                            if magnitude > 0:
                                self.dx = (dx / magnitude) * 3
                                self.dy = (dy / magnitude) * 3
                elif distance < 80: 
                    self.isHitting = True
                    self.isAttracted = True
                    dx = point.x - self.x
                    dy = point.y - self.y
                    magnitude = (dx**2 + dy**2)**0.5
                    if magnitude > 0:
                        self.dx = (dx / magnitude) * 3
                        self.dy = (dy / magnitude) * 3
        
        self.swim()
        return False


class FishingBait:
    def __init__(self,x,y,color):
        self.x = x
        self.y = y
        self.color = color
        self.touched = False
        self.touchedFish = None
        self.attractedFish = None

    def drawBait(self, lineEndX, lineEndY):
        if not self.touched:
            drawCircle(lineEndX, lineEndY, 7, fill=self.color, border = 'black')

class FishManager:
    def __init__(self, game):
        self.game = game
        self.fishes = []
        self.checkAndaddFish()
        self.phase = "normal"  # 初始阶段
        self.phaseTimer = 0

    def addRandomfish(self):
        newfish = Fish()
        self.fishes.append(newfish)

    def checkAndaddFish(self):
        while len(self.fishes) < 8:
            self.addRandomfish()

    def drawAllFishes(self):
        for fish in self.fishes:
            fish.drawFish()

# --------------------------------------------------------
# AI Tool Used: ChatGPT
# Purpose: Debugging
# Prompt: Fishes do the wrong movement
# --------------------------------------------------------

    def updateFishes(self, bait=None, fishingMode='idle'): 
        if fishingMode == 'fishing':
            self.phaseTimer += 1

            if self.phaseTimer <= 30:
                self.phase = "escape"
                for fish in self.fishes:
                    fish.isEscape(bait)

            elif 30 < self.phaseTimer <= 60:
                self.phase = "transition"
                for fish in self.fishes:
                    fish.dx = fish.dy = 0
                    if self.phaseTimer == 60:  
                        fish.dx = random.choice([-fish.speed, fish.speed])
                        fish.dy = random.randint(-1, 1)
                    else:
                        fish.dx = fish.dy = 0

            else:
                self.phase = "normal"
                for fish in self.fishes:
                    if bait and fish.color == bait.color:
                        fish.moveTowardsPoint(bait, fishingMode)
                    else:
                        fish.swim()
        else:
            self.phase = "normal"
            self.phaseTimer = 0
            for fish in self.fishes:
                fish.swim()

    def removeFish(self, fish):
        if fish in self.fishes:
            self.fishes.remove(fish)
            self.checkAndaddFish()

    def hasFishTouchedBait(self):
        for fish in self.fishes:
            if fish.hasTouchedBait:
                return True
        return False

class KittenManager:
    def __init__(self, game):
        self.game = game
        self.player = KittenPlayer(self.game, -1)  
        self.player.x = 200 
        self.player.y = 150
    
    def getPlayerKitten(self):
        return self.player
    
    def getCurrentKitten(self):
            return self.player

    def drawPlayerKitten(self):
        self.player.drawKitten()

class KittenPlayer:
    def __init__(self, game, index):
        self.game = game
        self.x = 212 if index != -1 else 200  
        self.y = 95 if index != -1 else 150
        self.width = 80
        self.height = 80
        self.index = index
        self.isPlayer = (index == -1)  
        self.targetColor = random.choice(['red', 'orange', 'yellow', 'green', 'blue', 'purple'])
        self.isSatisfied = False
        self.image = '../asset/12.png' if self.isPlayer else f'../asset/kit{index + 1}.png'
        # Image source: https://www.pinterest.com/pin/775885842080
        # Image source: https://www.pinterest.com/pin/2251868557600246/

    def drawKitten(self):
        drawImage(self.image, self.x + 20, self.y, width=self.width, height=self.height, opacity=100)
        if self.isPlayer:
            drawLine(self.x + 60, self.y + 80, self.x + 120, self.y +40, fill='blue', lineWidth=5)
        if not self.isPlayer:
            drawCircle(self.x, self.y+15, 5, fill='white')
            drawCircle(self.x-5, self.y, 5, fill='white')
            drawRect(self.x-20, self.y-40, 90, 30, fill='white')    
            drawOval(self.x-2, self.y-25,25,15, fill=self.targetColor, border = 'black')
            drawCircle(self.x-7, self.y-25, 2, fill='black')
            drawPolygon(self.x+8, self.y-25, self.x+18, self.y-30, self.x+18, self.y-10, fill=self.targetColor, border='black', opacity=70)

    def move(self, dx, dy):
        if self.isPlayer:  
            newX = self.x + dx
            newY = self.y + dy
            if 0 <= newX <= 400 - (self.width + 50):
                self.x = newX
            if 86 <= newY <= 335 - self.height:
                self.y = newY

class FishingLine:
    def __init__(self, player):
        self.game = player.game
        self.player = player
        self.lineLength = 280
        self.colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
        self.colorIndex = 0 
        self.color = self.colors[self.colorIndex]
        self.angle = 0
        self.direction = 1
        self.mode = 'idle' 
        self.endX, self.endY = self.player.x + 120, self.player.y + 15
        self.currentBait = None
        self.currentBait = FishingBait(self.endX, self.endY, self.color)
        self.fishEscaped = False

    def drawLine(self):
        rodEndX = self.player.x + 120
        rodEndY = self.player.y + 40

        if self.mode == 'idle':
            self.endX = rodEndX
            self.endY = rodEndY + 40
            if self.currentBait:
                self.currentBait.x = self.endX
                self.currentBait.y = self.endY
        drawLine(rodEndX, rodEndY, self.endX, self.endY, fill='black', lineWidth=2)

        if self.currentBait:
            self.currentBait.drawBait(self.endX, self.endY)

    def followMouse(self, mouseX, mouseY):
        if self.mode == 'mouse':
            rodEndX = self.player.x + 120
            rodEndY = self.player.y - 5
            distance = math.sqrt((mouseX - rodEndX)**2 + (mouseY - rodEndY)**2)
            angle = math.atan2(mouseY - rodEndY, mouseX - rodEndX)
            
            if distance <= self.lineLength:
                self.endX = mouseX
                self.endY = mouseY
            else:
                self.endX, self.endY = calculateEndPoint(rodEndX, rodEndY, math.degrees(angle), self.lineLength)
            
            if self.currentBait:
                self.currentBait.x = self.endX
                self.currentBait.y = self.endY

    def checkMouseClick(self, mouseX, mouseY):
        if self.mode != 'mouse': 
            return
        rodEndX = self.player.x + 120
        rodEndY = self.player.y - 5
        distance = getDistance(rodEndX, rodEndY, mouseX, mouseY)
        if distance <= self.lineLength:
            self.mode = 'fishing'
            self.endX = mouseX
            self.endY = mouseY

            if self.currentBait:
                self.currentBait.x = mouseX
                self.currentBait.y = mouseY
        else:
            angle = math.atan2(mouseY - rodEndY, mouseX - rodEndX)
            self.endX, self.endY = calculateEndPoint(rodEndX, rodEndY, math.degrees(angle), self.lineLength)
            if self.currentBait:
                self.currentBait.x = self.endX
                self.currentBait.y = self.endY
# --------------------------------------------------------
# AI Tool Used: ChatGPT
# Purpose: Debugging
# Prompt: No bait after user clicking
# --------------------------------------------------------
    def update(self):
        rodEndX = self.player.x + 120
        rodEndY = self.player.y - 5
        if self.mode == 'swing':
            self.angle += 2 * self.direction
            if self.angle >= 180 or self.angle <= 0:
                self.direction *= -1
            self.endX, self.endY = calculateEndPoint(rodEndX, rodEndY, self.angle, self.lineLength)
            if self.currentBait:  
                self.currentBait.x = self.endX
                self.currentBait.y = self.endY

    def shootLine(self):
        rodEndX = self.player.x + 120
        rodEndY = self.player.y - 5
        if self.mode == 'swing':
            self.mode = 'fishing'
            self.endX, self.endY = calculateEndPoint(rodEndX, rodEndY, self.angle, self.lineLength)
            self.currentBait = FishingBait(self.endX, self.endY, self.color)
            
        elif self.mode == 'mouse':
            self.mode = 'fishing'
            if self.endX is None or self.endY is None:
                self.endX, self.endY = rodEndX, rodEndY + 15
            self.currentBait = FishingBait(self.endX, self.endY, self.color)       

    def resetToIdle(self):
        if self.mode == 'fishing':
            if self.currentBait is not None:
                if not hasattr(self.currentBait, 'touched'):
                    self.currentBait.touched = False
                if not hasattr(self.currentBait, 'touchedFish'):
                    self.currentBait.touchedFish = None

                if not self.currentBait.touched and not self.currentBait.touchedFish:  # 如果没有钓到鱼就收杆
                    self.game.countScore.addScore('cancel_fishing')
            elif self.fishEscaped:
                self.game.countScore.addScore('fish_escaped')
                self.fishEscaped = False
        self.mode = 'idle'
        self.endX, self.endY = self.player.x + 120, self.player.y + 15
        self.currentBait = FishingBait(self.endX, self.endY, self.color)
        self.showWarning = False

    def switchColor(self):
        if self.mode == 'idle':
            self.colorIndex = (self.colorIndex + 1) % len(self.colors)
            self.color = self.colors[self.colorIndex]
        if self.currentBait:
            self.currentBait.color = self.color

class Bar:
    def __init__(self, fish):
        self.fish = fish
        self.x = 200  
        self.y = 200
        self.width = 150
        self.height = 20
        self.progress = 0
        self.lastClickTime = time.time()  

    def drawBar(self):
        drawRect(self.x, self.y, self.width, self.height, fill='gray', border='black', borderWidth=1, opacity = 50)
        drawRect(self.x, self.y, self.progress, self.height, fill='green', opacity = 80)
# --------------------------------------------------------
# AI Tool Used: ChatGPT
# Purpose: Debugging
# Prompt: No change after user stops clicking
# --------------------------------------------------------
    def increaseProgress(self):
        self.progress = min(self.progress + 15, self.width)  
        self.lastClickTime = time.time()  

    def decreaseProgress(self):
        if time.time() - self.lastClickTime > 3:  
            self.progress = max(self.progress - 5, 0)  

    def isComplete(self):
        return self.progress >= self.width

__all__ = ['KittenPlayer', 'FishingLine', 'FishManager', 'Bar', 'getDistance', 
           'Fish', 'FishingBait', 'KittenManager']

