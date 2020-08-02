import time
import pygame
import numpy

### WINDOW INITIALISATION ###
pygame.init()
pygame.display.set_caption("RPi Game Shuttle")

### CONSTANT DECLARATIONS ###
DISPLAY_WIDTH  = 1920
DISPLAY_HEIGHT = 1080
DISPLAY_SIZE = numpy.array( (DISPLAY_WIDTH, DISPLAY_HEIGHT) )

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
                    print("ISS!")
                elif shooter_button.collidepoint(mouse_pos):
                    print("Shooter!")
                

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
