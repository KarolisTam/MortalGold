#gameclient.py
import pygame
from character import Character
from background import AnimatedBackground
from login import LoginScreen

login = LoginScreen()
login.run()

pygame.init()

# Game window
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mortal Gold")

clock = pygame.time.Clock()
FPS = 60

#define colours
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# define character variables
PUTIN_SIZE = 200
PUTIN_SCALE = 1
PUTIN_OFFSET = [62, 20]
PUTIN_DATA = [PUTIN_SIZE, PUTIN_SCALE, PUTIN_OFFSET]

MUSK_SIZE = 200
MUSK_SCALE = 1
MUSK_OFFSET = [62, 20]
MUSK_DATA = [MUSK_SIZE, MUSK_SCALE, MUSK_OFFSET]

# Load background image
bg_image = pygame.image.load("assets/images/background/bg.png").convert_alpha()
scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load spritesheets
putin_sheet = pygame.image.load("assets/images/putin/sprites/putin.png").convert_alpha()
musk_sheet = pygame.image.load("assets/images/musk/sprites/musk.png").convert_alpha()

# define number of steps in each animation
PUTIN_ANIMATION_STEPS = [7, 4, 1, 5, 5, 4, 9, 1]
MUSK_ANIMATION_STEPS = [7, 6, 1, 5, 5, 4, 10, 1]

background = AnimatedBackground()

#  function for drawing character health bars
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))

# Create two instances of characters
character_1 = Character(200, 450, False, PUTIN_DATA, putin_sheet, PUTIN_ANIMATION_STEPS)
character_2 = Character(700, 450, True, MUSK_DATA, musk_sheet, MUSK_ANIMATION_STEPS)

run = True
while run:

    clock.tick(FPS)

    # Update the background animation
    background.update()

    # Draw background
    background.draw(screen)

    # Character movement
    character_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, character_2)
    # character_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, character_1)

    # show player stats
    draw_health_bar(character_1.health, 20, 20)
    draw_health_bar(character_2.health, 860, 20)

    # update characters
    character_1.update()
    character_2.update()

    # draw character
    character_1.draw(screen)
    character_2.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    # Update display
    pygame.display.update()

# Exit Pygame
pygame.quit()


