import pygame
from character import Character

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

ZUCKENBERG_SIZE = 200
ZUCKENBERG_SCALE = 1
ZUCKENBERG_OFFSET = [62, 20]
ZUCKENBERG_DATA = [ZUCKENBERG_SIZE, ZUCKENBERG_SCALE, ZUCKENBERG_OFFSET]

# Load background image
bg_image = pygame.image.load("assets/images/background/bg.png").convert_alpha()
scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load spritesheets
putin_sheet = pygame.image.load("assets/images/putin/sprites/putin.png").convert_alpha()
zuckenberg_sheet = pygame.image.load("assets/images/zuckenberg/sprites/zuckenberg.png").convert_alpha()

# define number of steps in each animation
PUTIN_ANIMATION_STEPS = [7, 4, 1, 1, 1, 1, 1]
ZUCKENBERG_ANIMATION_STEPS = [7, 8, 1, 8, 8, 3, 7]

# Function for drawing background
def draw_bg():
    screen.blit(bg_image, (0, 0))

#  function for drawing character health bars
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))

# Create two instances of characters
character_1 = Character(200, 450, False, PUTIN_DATA, putin_sheet, PUTIN_ANIMATION_STEPS)
character_2 = Character(700, 450, True, ZUCKENBERG_DATA, zuckenberg_sheet, ZUCKENBERG_ANIMATION_STEPS)

run = True
while run:

    clock.tick(FPS)

    # Draw background
    draw_bg()

    # Character movement
    character_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, character_2)
    # character_2.move()

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
