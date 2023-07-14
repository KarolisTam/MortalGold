#gameclient.py
import pygame
import asyncio
import websockets
import json

from character import Character
from background import AnimatedBackground
from character_selection import CharacterSelectionScreen
from login import LoginScreen


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
        self.match = login.run()
        self.match_id = self.match["id"]
        print(self.match_id)
        print(self.match)
        if not self.match_id:
            return

        # Create animated background
        background = AnimatedBackground()

        # # Create an instance of the character selection screen
        # character_selection = CharacterSelectionScreen()
        # character_selection.run()
        player = Character(1, 200, 450, True, self.MUSK_DATA, self.musk_sheet, self.MUSK_ANIMATION_STEPS)
        opponent = Character(2, 700, 450, True, self.PUTIN_DATA, self.putin_sheet, self.PUTIN_ANIMATION_STEPS)
        
        # # Check the selected character and create instances accordingly
        # if self.match["current player"] == 0:
        #     player =  musk
        #     opponent = putin
        # else:
        #     opponent = musk
        #     player = putin



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

                    if self.match["current player"] == 0:
                    # Character movement
                        player.move(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.screen, opponent)
                    else:
                        opponent.move(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.screen, player)

                    # Show player stats
                    self.draw_health_bar(player.health, 20, 20)
                    self.draw_health_bar(opponent.health, 860, 20)

                    # Update characters
                    player.update()
                    print("player movement", player.rect.x, player.rect.y)
                    opponent.update()
                    print("opponent movement", opponent.rect.x, opponent.rect.y)

                    # Draw characters
                    player.draw(self.screen)
                    opponent.draw(self.screen)

                    # Construct game data
                    game_data = {
                        "player_id": self.match["current player"],
                        # "player action": player.action,
                        "player_health": player.health,
                        "player_position_x": player.rect.x,
                        "player_position_y": player.rect.y,


                        "opponent_health": opponent.health,
                        "opponent_position_x": opponent.rect.x,
                        "opponent_position_y": opponent.rect.y
                    }
                    # Convert game data to JSON format
                    game_data_json = json.dumps(game_data)
                    print("sending", game_data_json)


                    # Send game data to the server
                    # if player.action > 0:
                    await websocket.send(game_data_json)

                    # Receive game data from the server
                    # async for server_data_json in websocket:
                    server_data_json = await websocket.recv()
                    server_data = json.loads(server_data_json)
                    print("receve", server_data)
                        # Update the characters' health based on the received data
                    player.health = server_data.get("player_health", player.health)
                    player.rect.x = server_data.get("player_position_x", player.health)
                    player.rect.y = server_data.get("player_position_y", player.health)

                    opponent.health = server_data.get("opponent_health", opponent.health)
                    opponent.rect.x = server_data.get("opponent_position_x", opponent.rect.x)
                    opponent.rect.y = server_data.get("opponent_position_y", opponent.rect.y)
                    pygame.display.update()

                    # Update display

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
