from cmu_graphics import *
class Countscore:
    def __init__(self):
        self.score = 0
        self.scoreEvents = {
            'satisfy_first_customer': 100,  # 满足第一个顾客
            'satisfy_waiting_customer': 100,  # 满足等待中的顾客
            'customer_timeout': -10,  # 顾客等待超时
            'cancel_fishing': -5,  # 取消钓鱼
            'fish_escaped': -5, 
        }
    
    def addScore(self, event):
        if event in self.scoreEvents:
            self.score += self.scoreEvents[event]
    
    def getScore(self):
        return self.score
    
    def resetScore(self):
        self.score = 0