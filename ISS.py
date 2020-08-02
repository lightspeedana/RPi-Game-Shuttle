import pygame
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect
import requests
from PIL import Image, ImageDraw 

BLUE = (0, 74, 173)
WHITE = (255, 255, 255)
issDataURL = 'http://api.open-notify.org/iss-now.json'

pygame.init()
pygame.font.init()
pygame.display.set_caption('RPi Game Shuttle')
screen = pygame.display.set_mode((1920,1080))
image = pygame.image.load(r'out.jpg')
screen.fill(BLUE)
pygame.display.flip()
display_image = screen.blit(image, (0, 0))
pygame.display.update()

while True:
    pygame.event.get()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if display_image.collidepoint(x, y):
                data = requests.get(url = issDataURL)
                finalData = data.json()
                lat = float(finalData['iss_position']['latitude'])
                lon = float(finalData['iss_position']['longitude'])
                xCo = (int)(6 * lon + 540)
                yCo = (int)(3 * lat + 540)
                dist = round(math.sqrt((xCo - x)**2 + (yCo - y)**2))
                imageBlack = Image.new('RGB', (1080, 1080))
                imageMap = Image.open('out.jpg').convert('RGBA')
                imageBlack.paste(imageMap, (0,0))
                draw = ImageDraw.Draw(imageBlack)
                draw.rectangle([xCo, yCo, xCo+15, yCo+15], fill='blue', outline=None, width=20)
                draw.rectangle([x, y, x+15, y+15], fill='red', outline=None, width=20)
                imageBlack.save("finalOut.jpg", "JPEG")
                newImage = pygame.image.load(r'finalOut.jpg')
                screen.fill(BLUE)
                newImage_display = screen.blit(newImage, (0, 0))
                pygame.display.update()


                
