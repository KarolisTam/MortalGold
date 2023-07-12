# gameclient.py
import pygame
from character import Character
from background import AnimatedBackground
from character_selection import CharacterSelectionScreen
from login import LoginScreen
import asyncio
import websockets
import json

class GameClient:
    def __init__(self):
        pygame.init()

        # Game window
        self.SCREEN_WIDTH = 1280
        self.SCREEN_HEIGHT = 720

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Mortal Gold")

        self.clock = pygame.time.Clock()
        self.FPS = 60

        # define colours
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 255, 0)
        self.WHITE = (255, 255, 255)

        # define character variables
        self.PUTIN_SIZE = 200
        self.PUTIN_SCALE = 1
        self.PUTIN_OFFSET = [62, 20]
        self.PUTIN_DATA = [self.PUTIN_SIZE, self.PUTIN_SCALE, self.PUTIN_OFFSET]

        self.MUSK_SIZE = 200
        self.MUSK_SCALE = 1
        self.MUSK_OFFSET = [62, 20]
        self.MUSK_DATA = [self.MUSK_SIZE, self.MUSK_SCALE, self.MUSK_OFFSET]

        self.TRUMP_SIZE = 200
        self.TRUMP_SCALE = 1
        self.TRUMP_OFFSET = [62, 20]
        self.TRUMP_DATA = [self.TRUMP_SIZE, self.TRUMP_SCALE, self.TRUMP_OFFSET]

        # Load background image
        bg_image = pygame.image.load("assets/images/background/bg.png").convert_alpha()
        self.scaled_bg = pygame.transform.scale(bg_image, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        # Load spritesheets
        self.putin_sheet = pygame.image.load("assets/images/putin/sprites/putin.png").convert_alpha()
        self.musk_sheet = pygame.image.load("assets/images/musk/sprites/musk.png").convert_alpha()
        self.trump_sheet = pygame.image.load("assets/images/trump/sprites/trump.png").convert_alpha()

        # define number of steps in each animation
        self.PUTIN_ANIMATION_STEPS = [7, 4, 1, 5, 5, 4, 9, 1]
        self.MUSK_ANIMATION_STEPS = [7, 6, 1, 5, 5, 4, 10, 1]
        self.TRUMP_ANIMATION_STEPS = [10, 5, 1, 5, 1, 1, 1, 1]

    def run(self):
        login = LoginScreen()
        self.match_id = login.run()
        print(self.match_id)
        if not self.match_id:
            return

        # Create animated background
        background = AnimatedBackground()

        # Create an instance of the character selection screen
        character_selection = CharacterSelectionScreen()
        character_selection.run()

        # Check the selected character and create instances accordingly
        if character_selection.selected_character == 0:
            character_1 = Character(200, 450, False, self.PUTIN_DATA, self.putin_sheet, self.PUTIN_ANIMATION_STEPS)
            character_2 = Character(700, 450, True, self.MUSK_DATA, self.musk_sheet, self.MUSK_ANIMATION_STEPS)
        elif character_selection.selected_character == 1:
            character_1 = Character(200, 450, False, self.MUSK_DATA, self.musk_sheet, self.MUSK_ANIMATION_STEPS)
            character_2 = Character(700, 450, True, self.PUTIN_DATA, self.putin_sheet, self.PUTIN_ANIMATION_STEPS)
        elif character_selection.selected_character == 2:
            character_1 = Character(200, 450, False, self.TRUMP_DATA, self.trump_sheet, self.TRUMP_ANIMATION_STEPS)
            character_2 = Character(700, 450, True, self.PUTIN_DATA, self.putin_sheet, self.PUTIN_ANIMATION_STEPS)

        async def connect_to_server():
            uri = f"ws://localhost:8001/ws/game/{self.match_id}/"
            async with websockets.connect(uri) as websocket:
                run = True
                while run:
                    self.clock.tick(self.FPS)

                    # Update the background animation
                    background.update()

                    # Draw background
                    self.screen.blit(self.scaled_bg, (0, 0))

                    # Character movement
                    character_1.move(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.screen, character_2)
                    character_2.move(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.screen, character_1)

                    # Show player stats
                    self.draw_health_bar(character_1.health, 20, 20)
                    self.draw_health_bar(character_2.health, 860, 20)

                    # Update characters
                    character_1.update()
                    character_2.update()

                    # Draw characters
                    character_1.draw(self.screen)
                    character_2.draw(self.screen)

                    # Update display
                    pygame.display.update()

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            run = False

                    # Construct game data
                    game_data = {
                        # Player 1
                        "player1_position_x": character_1.rect.x,
                        "player1_position_y": character_1.rect.y,
                        "player1_health": character_1.health,
                        "player1_jump": character_1.jump,
                        # "player1_action": character_1.action,

                        # Player 2
                        "player2_position_x": character_2.rect.x,
                        "player2_position_y": character_2.rect.y,
                        "player2_health": character_2.health,
                        "player2_jump": character_2.jump,
                        # "player2_action": character_2.action,

                        # Include any other relevant game data
                    }

                    # Convert game data to JSON format
                    game_data_json = json.dumps(game_data)

                    # Send game data to the server
                    await websocket.send(game_data_json)

                    # Receive game data from the server
                    server_data = await websocket.recv()

                    # Process the received data
                    # ...

                # Exit Pygame
                pygame.quit()

        # Run the game client
        asyncio.get_event_loop().run_until_complete(connect_to_server())

    def draw_health_bar(self, health, x, y):
        ratio = health / 100
        pygame.draw.rect(self.screen, self.WHITE, (x - 2, y - 2, 404, 34))
        pygame.draw.rect(self.screen, self.RED, (x, y, 400, 30))
        pygame.draw.rect(self.screen, self.YELLOW, (x, y, 400 * ratio, 30))

# Run the game client
client = GameClient()
client.run()
