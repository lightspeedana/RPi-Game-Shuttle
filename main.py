import time
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect

pygame.init()
pygame.display.set_caption("RPi Game Shuttle")

display_width = 1920
display_height = 1080

blue = (0, 74, 173)
white = (255, 255, 255)
red = (214, 25, 27)
green = (25, 214, 27)

game_display = pygame.display.set_mode((display_width, display_height))

large_text = pygame.font.Font("fonts/omegaflight.ttf", 40)

def intro():

    logo = pygame.image.load("images/logo.png")
    logo = pygame.transform.scale(logo, (1000, 1000))
    logo_start_x = display_height
    logo_start_y = display_width // 2

    logo_rect = logo.get_rect()
    logo_rect.center = ((display_width // 2), (display_height // 2))
    logo_start_y = display_height
    logo_start_x = logo_rect.center[0]

    game_display.fill(blue)
    game_display.blit(logo, ((logo_start_x, logo_start_y)))
    pygame.display.update()
    print(logo_rect.center)
    print((logo_start_x, logo_start_y))

    while logo_start_y != (logo_rect.center[1] - 600):
        logo_start_y -= 20
        print(logo_start_y)
        game_display.blit(logo, ((logo_rect.center[0] // 2, logo_start_y)))
        pygame.display.update()

def text_objects(text, font, colour):
    text_surface = font.render(text, True, colour)
    return text_surface, text_surface.get_rect()

def button_display(text, colour, pos):
    text_surf, text_rect = text_objects(text, large_text, colour)
    text_rect.center = pos
    game_display.blit(text_surf, text_rect)
    pygame.display.update()
    return text_rect

def title_screen():
    intro()
    time.sleep(0.5)
    button_area = button_display("Press any key to start", red, (display_width // 2, display_height // 2 + 100))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            elif event.type == pygame.KEYDOWN or (event.type == pygame.MOUSEBUTTONDOWN and button_area.collidepoint(pygame.mouse.get_pos())):
                return True

def halt():
    pygame.display.quit()
    pygame.quit()
    quit()

if __name__ == "__main__":
    if title_screen():
        game_display.fill(blue)
        menu_iss_button_rect = button_display("ISS Guessing Game", red, (display_width // 2, display_height // 2 - 50))
        menu_space_button_rect = button_display("Space Shooter Game", red, (display_width // 2, display_height // 2 + 50))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if menu_iss_button_rect.collidepoint(pos):
                        print("ISS game!")
                    elif menu_space_button_rect.collidepoint(pos):
                        print("Shooter game!")
                elif event.type == pygame.QUIT:
                    halt()
    else:
        halt()
