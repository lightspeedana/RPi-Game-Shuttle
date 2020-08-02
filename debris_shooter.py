import math
import random
import pygame
import os
import time
ourpath = os.getcwd()
debris = []
GRID_SIZE = (480,270)
RED = (255,0,0)
BLUE = (0,255,255)
GREEN = (0,0,255)
WHITE = (255,255,255)
BACKGROUND = (24, 19, 102)
GRAY = (81, 87, 83)
FPS = 60
playerimage = pygame.image.load(os.path.join(ourpath,"images/playership.png"))
playerimage = pygame.transform.scale(playerimage,(50,50))
debris = []
global debristomake
debristomake = 50
SPEED = 1
pygame.init()
maxX = 1920
maxY = 1080
screen = pygame.display.set_mode((maxX,maxY))
pygame.display.set_caption('RPI Game Shuttle')
screen.fill(BLUE)
pygame.display.update()
font = pygame.font.Font(os.path.join(ourpath,r"fonts/omegaflight.ttf"), 32)
centerRect = ( (maxX / 2) - 200,maxY/2,  20,20)
#centerRect = (maxX - 200,0,20,20)
def sign(value):
    return value and [-1, 1][value > 0]
def makedebris():
    global debristomake
    size = (math.floor(random.triangular(1,50)),math.floor(random.triangular(1,50)))
    pos = [random.randint(300,465) , random.randint(11,259)]
    direction = (-1,0.1)
    debris.append(Debris(direction,pos,size))
    debristomake -= 1
def display(text,color):
    textRender(text,centerRect,color)
    pygame.display.update()
    screen.fill(BACKGROUND)
    time.sleep(0.5)
    pass
def textRender(text, rect, forecolor):
    newRect = pygame.Rect(rect)
    textobj = font.render(text,True, forecolor)
    textRect = textobj.get_rect()
    textRect.center = newRect.center
    screen.blit(textobj, textRect)
def diff(pos1,pos2):
    diff1 = abs(pos1[0] - pos2[0])**2
    diff2 = abs(pos1[1] - pos2[1])**2
    return math.sqrt(diff1 + diff2)
def diffvec(pos1,pos2):
    return abs(pos1[0] - pos2[0]),abs(pos1[1] - pos2[1])
class Debris:
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
        if self.pos[0] >= GRID_SIZE[0] or self.pos[1] >= GRID_SIZE[1] or self.pos[0] <= 0 or self.pos[1] <= 0:
            self.destroy()
    def gethit(self):
        self.durability -= 1
        if self.durability <= 0:
            self.destroy()
    def collide(self,pos,usingpygame=True):
        """
        difference = diffvec(pos,self.pos)
        if difference[0] <= self.size[0] and difference[1] <= self.size[1]:
            return True
        else:
            return False
        """
        if usingpygame:
            return self.rect.collidepoint([pos[0]*4,pos[1]*4])
        else:
            difference = diffvec(pos,self.pos)
            if difference[0] <= (self.size[0] + 12.5) and difference[1] <= (self.size[1] + 12.5):
                return True
            else:
                return False
    def update(self):
        self.realpos = [self.pos[0]*4,self.pos[1]*4]
        self.realsize = [self.size[0]*4,self.size[1]*4]
        self.rect = pygame.Rect(*self.realpos, *self.size)
    def display(self):
        self.realpos = [self.pos[0]*4,self.pos[1]*4]
        self.realsize = [self.size[0]*4,self.size[1]*4]
        self.rect = pygame.Rect(*self.realpos, *self.size)
        pygame.draw.rect(screen,GRAY,self.rect)
    def destroy(self):
        global debristomake
        debris.remove(self)
        debristomake += 1
class Player:
    def __init__(self,pos=[0,0]):
        self.pos = pos
        self.shootcooldown = 0
        self.hitcooldown = 1
        self.targetpos = None
        self.health = 100
    def tick(self,events):
        for piece in debris:
            if piece.collide(self.pos,usingpygame=False) and not self.hitcooldown:
                self.health -= (piece.size[0] + piece.size[1])//2
                print(self.health)
                self.hitcooldown = 2
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                gamepos = (pos[0]//4,pos[1]//4)
                print(gamepos,"MOUSE CLICK")
                if gamepos[0] < GRID_SIZE[0]//4:
                    # can only move within one half of the grid
                    self.targetpos = gamepos
                    print(self.targetpos,"MOVEMENT")
                else:
                    self.shoot(pos)
        if self.targetpos == self.pos:
            self.targetpos = None # stop movement till next mouse click
        if self.targetpos:
            curx,cury = self.pos
            targetx,targety = self.targetpos
            distance = diff(self.pos,self.targetpos)
            if distance == 0 or math.floor(abs(targetx - curx)) == 0 and math.floor(abs(targety - cury)) == 0:
                self.targetpos = None
            else:
                proportion = SPEED/distance
                diffx = targetx - curx
                diffy = targety - cury
                diffx *= proportion
                diffy *= proportion
                self.pos[0] = curx + diffx
                self.pos[1] = cury + diffy
        if self.health <= 0:
            game_exit()
    def shoot(self,pos):
        if self.shootcooldown:
            display(f"You can't shoot yet! You still have {self.shootcooldown} seconds.",RED)
        else:
            for piece in debris:
                piece.update()
                if piece.rect.collidepoint(pos):
                    print(pos,piece.realpos)
                    piece.gethit()
                    break
            self.shootcooldown = 10
player = Player()
def game_exit():
    screen.fill(BACKGROUND)
    display("GAME OVER.",RED)
    time.sleep(5)
    quit()
counter = 0
while True:
    events = pygame.event.get()
    player.tick(events)
    while debristomake:
        makedebris()
    for piece in debris:
        piece.move()
    screen.fill(BACKGROUND)
    for piece in debris:
        piece.display()
    realplayer = (int(player.pos[0]*4),int(player.pos[1]*4))
    screen.blit(playerimage,realplayer)
    textRender(f"Health: {player.health}",(maxX - 200,0,20,20),RED)
    textRender(f"Shoot cooldown: {player.shootcooldown}",(maxX - 200,50,20,20),RED)
    pygame.display.update()
    counter += 1
    if counter % FPS == 0:
        if player.shootcooldown:
            player.shootcooldown -= 1
        if player.hitcooldown:
            player.hitcooldown -= 1
        if player.pos[1] <= 35:
            player.health -= 10
    pygame.time.Clock().tick(FPS)
