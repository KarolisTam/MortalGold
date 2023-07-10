#gameclient.py
import pygame
from character import Character
from background import AnimatedBackground
from login import LoginScreen
from character_selection import CharacterSelectionScreen
import asyncio
import websockets
import json

login = LoginScreen()
login.run()

# Create animated background
background = AnimatedBackground()

# Create an instance of the character selection screen
character_selection = CharacterSelectionScreen()
character_selection.run()

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

TRUMP_SIZE = 200
TRUMP_SCALE = 1
TRUMP_OFFSET = [62, 20]
TRUMP_DATA = [TRUMP_SIZE, TRUMP_SCALE, TRUMP_OFFSET]

# Load background image
bg_image = pygame.image.load("assets/images/background/bg.png").convert_alpha()
scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load spritesheets
putin_sheet = pygame.image.load("assets/images/putin/sprites/putin.png").convert_alpha()
musk_sheet = pygame.image.load("assets/images/musk/sprites/musk.png").convert_alpha()
trump_sheet = pygame.image.load("assets/images/trump/sprites/trump.png").convert_alpha()

# define number of steps in each animation
PUTIN_ANIMATION_STEPS = [7, 4, 1, 5, 5, 4, 9, 1]
MUSK_ANIMATION_STEPS = [7, 6, 1, 5, 5, 4, 10, 1]
TRUMP_ANIMATION_STEPS = [10, 5, 1, 5, 1, 1, 1, 1]

#  function for drawing character health bars
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))

# Check the selected character and create instances accordingly
if character_selection.selected_character == 0:
    character_1 = Character(200, 450, False, PUTIN_DATA, putin_sheet, PUTIN_ANIMATION_STEPS)
    character_2 = Character(700, 450, True, MUSK_DATA, musk_sheet, MUSK_ANIMATION_STEPS)
elif character_selection.selected_character == 1:
    character_1 = Character(200, 450, False, MUSK_DATA, musk_sheet, MUSK_ANIMATION_STEPS)
    character_2 = Character(700, 450, True, PUTIN_DATA, putin_sheet, PUTIN_ANIMATION_STEPS)
elif character_selection.selected_character == 2:
    character_1 = Character(200, 450, False, TRUMP_DATA, trump_sheet, TRUMP_ANIMATION_STEPS)
    character_2 = Character(700, 450, True, PUTIN_DATA, putin_sheet, PUTIN_ANIMATION_STEPS)

async def connect_to_server():
    uri = "ws://localhost:8001/ws/" 
    async with websockets.connect(uri) as websocket:
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

            # Construct game data
            game_data = {
                "player1_position_x": character_1.rect.x,
                "player1_position_y": character_1.rect.y,
                "player2_position_x": character_2.rect.x,
                "player2_position_y": character_2.rect.y,
                "player1_health": character_1.health,
                "player2_health": character_2.health,
                "player1_jump": character_1.jump,
                # Include any other relevant game data
            }

            # Convert game data to JSON format
            game_data_json = json.dumps(game_data)

            # Send game data to the server
            await websocket.send(game_data_json)

            # Receive game data from the server
            server_data = await websocket.recv()

            # Process the received data

            # Update game state based on server data

            # Update display
            pygame.display.update()

        # Exit Pygame
        pygame.quit()

# Run the game client
asyncio.get_event_loop().run_until_complete(connect_to_server())
