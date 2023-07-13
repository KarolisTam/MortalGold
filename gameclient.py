
#gameclient.py
import pygame
import sys
import asyncio
import websockets
import json

from character import Character
from background import AnimatedBackground
from character_selection import CharacterSelectionScreen
from login import LoginScreen
from mortalgold.gameapp.consumers import GameConsumer


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

    def draw_health_bar(self, health, x, y):
        ratio = health / 100
        pygame.draw.rect(self.screen, self.WHITE, (x - 2, y - 2, 404, 34))
        pygame.draw.rect(self.screen, self.RED, (x, y, 400, 30))
        pygame.draw.rect(self.screen, self.YELLOW, (x, y, 400 * ratio, 30))

    def run(self):
        login = LoginScreen()
        self.match_id = login.run()
        print(self.match_id)
        if not self.match_id:
            return

        # Create animated background
        background = AnimatedBackground()

        # # Create an instance of the character selection screen
        # character_selection = CharacterSelectionScreen()
        # character_selection.run()

        # Check the selected character and create instances accordingly
        player = Character(200, 450, False, self.PUTIN_DATA, self.putin_sheet, self.PUTIN_ANIMATION_STEPS)
        opponent = Character(700, 450, True, self.MUSK_DATA, self.musk_sheet, self.MUSK_ANIMATION_STEPS)

        # Create an instance of the GameConsumer and pass the player instance
        game_consumer = GameConsumer(player=player)

        async def connect_to_server(self):
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
                    player.move(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.screen, opponent)
                    # opponent.move(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.screen, player)

                    # Show player stats
                    self.draw_health_bar(player.health, 20, 20)
                    self.draw_health_bar(opponent.health, 860, 20)

                    # Update characters
                    player.update()
                    opponent.update()

                    # Draw characters
                    player.draw(self.screen)
                    opponent.draw(self.screen)

                    # Update the characters' positions and health based on the received data
                    game_consumer.player = player
                    game_consumer.opponent = opponent

                    # Update display
                    pygame.display.update()


                    # Construct game data
                    game_data = {
                        # Player 1
                        "player_health": player.health,
                        "opponent_health": opponent.health,
                    }

                    # Convert game data to JSON format
                    game_data_json = json.dumps(game_data)

                    # Send game data to the server
                    await websocket.send(game_data_json)

                    # Receive game data from the server
                    server_data_json = await websocket.recv()
                    server_data = json.loads(server_data_json)

                    # Update the characters' positions and health based on the received data
                    player.health = server_data.get("player_health", player.health)
                    opponent.health = server_data.get("opponent_health", opponent.health)

                    #print("player1", player.health)
                    print("opponent", opponent.health)

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            run = False

                    # Handle game logic
                    # ...

                # Exit Pygame
                pygame.quit()

        # Run the game client
        asyncio.get_event_loop().run_until_complete(connect_to_server(self))


if __name__ == "__main__":
    # Run the game client
    client = GameClient()
    client.run()
