import math
import pygame
import random

class Target :
    MAX_SIZE = 50
    GROWTH_RATE = 0.7
    COLOUR = ["red", "black", "gold"]
    SECOND_COLOUR = "white"

    def __init__(self, x, y) :
        self.x = x
        self.y = y
        self.size = 0
        self.grow = True
        self.colour_chosen = random.choices(self.COLOUR, weights=[0.83,0.1, 0.07], k=1)[0]

    def update(self):
        if self.size + self.GROWTH_RATE >=  self.MAX_SIZE :
            self.grow = False
        
        if self.grow: self.size += self.GROWTH_RATE
        else : self.size -= self.GROWTH_RATE

    def draw(self, win) :
        pygame.draw.circle(win, self.colour_chosen, (self.x, self.y), self.size)
        pygame.draw.circle(win, self.SECOND_COLOUR, (self.x, self.y), self.size * 0.8)
        pygame.draw.circle(win, self.colour_chosen, (self.x, self.y), self.size * 0.6)
        pygame.draw.circle(win, self.SECOND_COLOUR, (self.x, self.y), self.size * 0.4)

    def collide(self, x, y):
        dist = math.sqrt((self.x - x)**2 + (self.y - y)**2)
        return dist <= self.size