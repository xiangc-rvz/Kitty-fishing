from cmu_graphics import *
from score import Countscore

class CustomerQueue:
    def __init__(self,game):
        self.game = game
        self.customers = []
        self.maxDisplayed = 3
        self.customerWaitTimer = 0
        self.waitInterval = 240
        self.customerWaitTimers = {}

    def update(self):
        self.customerWaitTimer += 1
        if self.customerWaitTimer >= self.waitInterval and len(self.customers) < 6:
            self.addCustomer()
            self.customerWaitTimer = 0

        for customer in self.customers:
            if customer not in self.customerWaitTimers:
                self.customerWaitTimers[customer] = 0
            
            self.customerWaitTimers[customer] += 1
            if self.customerWaitTimers[customer] >= 300:  
                self.game.countScore.addScore('customer_timeout')  
                self.customerWaitTimers[customer] = 0

    def getCurrentCustomer(self):
        return self.customers[0] if self.customers else None

    def addCustomer(self):
        if len(self.customers) < 6:
            from test import KittenPlayer
            newCustomer = KittenPlayer(None, len(self.customers))
            self.customers.append(newCustomer)
            self.updateCustomerPositions()

    def removeCurrentCustomer(self):
        if self.customers:
            self.customers.pop(0)
            self.updateCustomerPositions()
            self.customerSpawnTimer = self.waitInterval - 60

    def updateCustomerPositions(self):
        index = 0
        for customer in self.customers[:self.maxDisplayed]:
            customer.x = 30 + index * 90
            customer.y = 120
            index += 1

    def getCustomerAtPosition(self, mouseX, mouseY):
        for customer in self.customers[:self.maxDisplayed]:
            if (customer.x <= mouseX <= customer.x + 80 and 
                customer.y <= mouseY <= customer.y + 80):
                return customer
        return None

# --------------------------------------------------------
# AI Tool Used: ChatGPT
# Purpose: Optimization logic and debugging
# Prompt: having problem in update customers position and quantity
# --------------------------------------------------------

    def satisfyCustomer(self, customer):
        if customer in self.customers:
            if customer == self.customers[0]:
                self.game.countScore.addScore('satisfy_first_customer')
            else:
                self.game.countScore.addScore('satisfy_first_customer')
            self.customers.remove(customer)

            if customer in self.customerWaitTimers:
                del self.customerWaitTimers[customer]
            self.updateCustomerPositions()


    def drawCustomers(self):
         index = 0
         for customer in self.customers[:self.maxDisplayed]:
            customer.drawKitten()

            waitTime = self.customerWaitTimers.get(customer, 0) // 30  
            drawLabel(f'Wait: {waitTime}s', customer.x + 40, customer.y - 30, size=12)

            if index == 0 and customer:
                drawLabel("Current", customer.x + 40, customer.y - 15, size=12)
            index += 1
        