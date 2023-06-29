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

# Load background image
bg_image = pygame.image.load("assets/images/background/bg.png").convert_alpha()
scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Function for drawing background
def draw_bg():
    screen.blit(bg_image, (0, 0))

# Create two instances of characters
character_1 = Character(200, 450)
character_2 = Character(700, 450)

run = True
while run:

    clock.tick(FPS)

    # Draw background
    draw_bg()

    # Character movement
    character_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, character_2)
    # character_2.move()

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
