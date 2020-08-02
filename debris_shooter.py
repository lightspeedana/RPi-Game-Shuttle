import math
import random
import pygame
import os
ourpath = os.getcwd()
debris = []
GRID_SIZE = (480,270)
RED = (255,0,0)
BLUE = (0,255,255)
GREEN = (0,0,255)
WHITE = (255,255,255)
BACKGROUND = (24, 19, 102)
GRAY = (81, 87, 83)
playerimage = pygame.image.load(os.path.join(ourpath,"images/playership.png"))
debris = []
global debristomake
debristomake = 20
SPEED = 1
pygame.init()
maxX = 1920
maxY = 1080
screen = pygame.display.set_mode((maxX,maxY))
pygame.display.set_caption('RPi Game Shuttle')
screen.fill(BLUE)
pygame.display.update()
font = pygame.font.SysFont("comicsansms", 16)
def sign(value):
    return value and [-1, 1][value > 0]
def makedebris():
    global debristomake
    size = (random.triangular(1,10),random.triangular(1,10))
    pos = [465 , random.randint(11,259)]
    direction = (-1,1)
    debris.append(Debris(direction,pos,size))
    debristomake -= 1
def display(text,color):
    # To be replaced
    pass
def textRender(text, rect, forecolor):
    newRect = pygame.Rect(rect)
    textobj, textRect = font.render(text, forecolor)
    textRect.center = newRect.center
    screen.blit(textobj, textRect)
def diff(pos1,pos2):
    diff1 = abs(pos1[0] - pos2[0])**2
    diff2 = abs(pos1[1] - pos2[1])**2
    return math.sqrt(diff1 + diff2)
def diffvec(pos1,pos2):
    return abs(pos1[0] - pos2[0]),abs(pos1[1] - pos2[1])
class Debris:
    destroy = lambda self: debris.remove(self)
    # Start with a constant direction and move like that constantly because of space physics
    def __init__(self,direction,pos=[0,0],size=(5,5),debristype="Rock",):
        self.type = debristype
        self.durability = 1
        self.pos = pos
        self.direction = direction
        self.size = size
        self.rect = None
    def move(self):
        self.pos[0] += self.direction[0]
        self.pos[1] += self.direction[1]
        if self.pos[0] >= GRID_SIZE[0] or self.pos[1] >= GRID_SIZE[1]:
            self.destroy()
    def gethit(self):
        self.durability -= 0.1
        if self.durability <= 0:
            self.destroy()
        debristomake -= 1
    def collide(self,pos):
        """
        difference = diffvec(pos,self.pos)
        if difference[0] <= self.size[0] and difference[1] <= self.size[1]:
            return True
        else:
            return False
        """
        return self.rect.collidepoint([pos[0]*4,pos[1]*4])
    def display(self):
        self.rect = pygame.Rect(*self.pos, *self.size)
        pygame.draw.rect(screen,GRAY,self.rect)
class Player:
    def __init__(self,pos=[0,0]):
        self.pos = pos
        self.shootcooldown = 0
        self.targetpos = None
        self.health = 100
    def tick(self,events):
        for piece in debris:
            if piece.collide(self.pos):
                self.health -= (piece.size[0] + piece.size[1])//2
        if self.shootcooldown:
            self.shootcooldown -= 1
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                gamepos = (pos[0]//4,pos[1]//4)
                if gamepos[0] < GRID_SIZE[0]//4:
                    # can only move within one half of the grid
                    self.targetpos = gamepos
                else:
                    self.shoot(gamepos)
        if self.targetpos == self.pos:
            self.targetpos = None # stop movement till next mouse click
        if self.targetpos:
            curx,cury = self.pos
            targetx,targety = self.targetpos
            distance = diff(self.pos,self.targetpos)
            proportion = SPEED/distance
            diffx = targetx - curx
            diffy = targety - cury
            diffx *= proportion
            diffy *= proportion
            self.pos[0] = math.floor(curx + diffx)
            self.pos[1] = math.floor(cury + diffy)
        if self.health <= 0:
            game_exit()
    def shoot(self,pos):
        if self.shootcooldown:
            display(f"You can't shoot yet! You still have {self.shootcooldown} ticks/seconds.",RED)
        for piece in debris:
            if piece.collide(pos):
                piece.gethit()
                break
        self.shootcooldown = 10
player = Player()
def game_exit():
    display("GAME OVER.",RED)
    quit()
while True:
    events = pygame.event.get()
    player.tick(events)
    while debristomake:
        makedebris()
    screen.fill(BACKGROUND)
    for piece in debris:
        piece.display()
    pygame.time.Clock().tick(60)
    pygame.display.update()
