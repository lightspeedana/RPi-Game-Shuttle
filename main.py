import time
import pygame
import numpy
import requests
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
    "green": (25, 214, 27)
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
    pass

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
