import numpy
import pygame
import random
import requests
import time
from PIL import Image, ImageDraw


### WINDOW INITIALISATION ###
pygame.init()
pygame.display.set_caption("RPi Game Shuttle")

### CONSTANT DECLARATIONS ###
DISPLAY_WIDTH  = 1920
DISPLAY_HEIGHT = 1080
DISPLAY_SIZE = numpy.array( (DISPLAY_WIDTH, DISPLAY_HEIGHT) )

ISS_DATA_URL = 'http://api.open-notify.org/iss-now.json'

COLOURS = {
    "blue":  (0, 74, 173),
    "white": (255, 255, 255),
    "red":   (214, 25, 27),
    "green": (25, 214, 27),
    "space": (24, 19, 102),
    "grey":  (81, 87, 83)
}

DEFAULT_FONT = pygame.font.Font("fonts/omegaflight.ttf", 40)
LOGO = pygame.image.load("images/logo.png")
LOGO = pygame.transform.scale(LOGO, (1000, 1000))
INTRO_MUSIC = pygame.mixer.Sound("music/intro.ogg")
DISPLAY = pygame.display.set_mode( DISPLAY_SIZE )

### FUNCTION DECLARATIONS ###
def create_button(text: str = "", position: numpy.array = (0,0), colour: tuple = COLOURS["red"]) -> pygame.Rect:
    text = DEFAULT_FONT.render(text, True, colour)
    text_rect = text.get_rect()
    text_rect.center = position

    DISPLAY.blit(text, text_rect)
    pygame.display.update()
    print(type(text_rect))
    return text_rect


def halt() -> None:
    pygame.display.quit()
    pygame.quit()
    
    quit()


def shooter_game() -> None:

    ### CONSTANT DECLARATIONS

    debristomake = 50
    SPEED = 1
    playerimage = pygame.image.load("images/playership.png")
    playerimage = pygame.transform.scale(playerimage,(50,50))
    GRID_SIZE = (480,270)
    debris = []

    ### FUNCTION DELCARATIONS
    def game_exit():
        screen.fill(BACKGROUND)
        create_button( "GAME OVER.", DISPLAY_SIZE // 2, COLOURS["red"])
        time.sleep(1)
        halt()


    def makedebris():
        nonlocal debristomake
        size = (numpy.floor(random.triangular(1,50)),numpy.floor(random.triangular(1,50)))
        pos = [random.randint(300,465) , random.randint(11,259)]
        direction = (-1,0.1)
        debris.append(Debris(direction,pos,size))
        debristomake -= 1


    def diffvec(pos1,pos2):
        return abs(pos1[0] - pos2[0]),abs(pos1[1] - pos2[1])


    def diff(pos1,pos2):
        diff1 = abs(pos1[0] - pos2[0])**2
        diff2 = abs(pos1[1] - pos2[1])**2
        return (diff1 + diff2)**0.5


    ### CLASS DECLARATIONS
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
            pygame.draw.rect(DISPLAY,COLOURS["grey"],self.rect)
        def destroy(self):
            nonlocal debristomake
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
                    self.hitcooldown = 2
            for event in events:
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    gamepos = (pos[0]//4,pos[1]//4)
                    if gamepos[0] < GRID_SIZE[0]//4:
                        # can only move within one half of the grid
                        self.targetpos = gamepos
                    else:
                        self.shoot(pos)
            if self.targetpos == self.pos:
                self.targetpos = None # stop movement till next mouse click
            if self.targetpos:
                curx,cury = self.pos
                targetx,targety = self.targetpos
                distance = diff(self.pos,self.targetpos)
                if distance == 0 or numpy.floor(abs(targetx - curx)) == 0 and numpy.floor(abs(targety - cury)) == 0:
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
                create_button(f"You can't shoot yet! You still have {self.shootcooldown} seconds.", DISPLAY_SIZE // 2)
                time.sleep(0.5)            
            else:
                for piece in debris:
                    piece.update()
                    if piece.rect.collidepoint(pos):
                        piece.gethit()
                        break
                self.shootcooldown = 10
    
    player = Player()
    counter = 0

    # Event handling loop
    while True:
        events = pygame.event.get()
        for i in events:
            if i.type == pygame.QUIT:
                game_exit()
        player.tick(events)
        while debristomake:
            makedebris()
        for piece in debris:
            piece.move()
        DISPLAY.fill(COLOURS["space"])
        for piece in debris:
            piece.display()
        realplayer = (int(player.pos[0]*4),int(player.pos[1]*4))
        DISPLAY.blit(playerimage,realplayer)
        create_button(f"Health: {player.health}",DISPLAY_SIZE + (-250, 50 - DISPLAY_HEIGHT) ,COLOURS["red"])
        create_button(f"Shoot cooldown: {player.shootcooldown}",DISPLAY_SIZE + (-250, 100 - DISPLAY_HEIGHT),COLOURS["red"])
        pygame.display.update()
        counter += 1
        if counter % 60 == 0:
            if player.shootcooldown:
                player.shootcooldown -= 1
            if player.hitcooldown:
                player.hitcooldown -= 1
            if player.pos[1] <= 35:
                player.health -= 10
        pygame.time.Clock().tick(60)


def iss_game() -> None:

    # ISS game screen
    DISPLAY_WIDTH  = 1080
    DISPLAY_HEIGHT = 1080
    DISPLAY_SIZE = numpy.array( (DISPLAY_WIDTH, DISPLAY_HEIGHT) )
    DISPLAY = pygame.display.set_mode( DISPLAY_SIZE )
    image = pygame.image.load('out.jpg')
    DISPLAY.fill(COLOURS["blue"])
    pygame.display.flip()
    display_image = DISPLAY.blit(image, (0, 0))
    pygame.display.update()

    # Event handling loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                halt()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if display_image.collidepoint(x, y):
                    data = requests.get(url = ISS_DATA_URL)
                    finalData = data.json()
                    lat = float(finalData['iss_position']['latitude'])
                    lon = float(finalData['iss_position']['longitude'])
                    xCo = (int)(6 * lon + 540)
                    yCo = (int)(3 * lat + 540)
                    dist = round(((xCo - x)**2 + (yCo - y)**2) ** 0.5)
                    imageBlack = Image.new('RGB', (1080, 1080))
                    imageMap = Image.open('out.jpg').convert('RGBA')
                    imageBlack.paste(imageMap, (0,0))
                    draw = ImageDraw.Draw(imageBlack)
                    draw.rectangle([xCo, yCo, xCo+15, yCo+15], fill='blue', outline=None, width=20)
                    draw.rectangle([x, y, x+15, y+15], fill='red', outline=None, width=20)
                    imageBlack.save("finalOut.jpg", "JPEG")
                    newImage = pygame.image.load('finalOut.jpg')
                    DISPLAY.fill(COLOURS["blue"])
                    newImage_display = DISPLAY.blit(newImage, (0, 0))
                    pygame.display.update()
                    time.sleep(0.5)
                    create_button( f"You were {dist} pixels away!", DISPLAY_SIZE // 2  + (0, DISPLAY_HEIGHT // 2 - 100))
                    pygame.display.update()


def menu_screen() -> None:

    ### Menu screen
    DISPLAY.fill( COLOURS["blue"] )
    pygame.display.update()

    time.sleep(0.5)
    iss_button = create_button( "ISS Guessing Game", DISPLAY_SIZE // 2 + (0, -50))
    pygame.display.update()

    time.sleep(0.5)
    shooter_button = create_button( "Shooter Game", DISPLAY_SIZE // 2 + (0, 50))
    pygame.display.update()
    
    # Event handling loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                halt()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if iss_button.collidepoint(mouse_pos):
                    iss_game()
                elif shooter_button.collidepoint(mouse_pos):
                    shooter_game()
                

if __name__ == "__main__":

    ### Main screen
    DISPLAY.fill( COLOURS["blue"] )
    
    logo_coords = DISPLAY_SIZE // (2, 1)
    print(logo_coords)
    pygame.mixer.Sound.play(INTRO_MUSIC)
    while logo_coords[1] + 600 > (DISPLAY_HEIGHT // 2):
        DISPLAY.blit(LOGO, logo_coords // (2, 1))
        pygame.display.update()
        logo_coords -= (0, 15)

    time.sleep(0.5)
    main_text = create_button( "Press any key to start", DISPLAY_SIZE // 2 + (0, 100))
    
    # Event handling loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                halt()

            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN and main_text.collidepoint(pygame.mouse.get_pos()):
                menu_screen()
