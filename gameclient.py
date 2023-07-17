#gameclient.py
import pygame
import asyncio
import websockets
import json
import logging

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

        # Initialize logging
        logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s]: %(message)s")

    def draw_health_bar(self, health, x, y):
        ratio = health / 100
        pygame.draw.rect(self.screen, self.WHITE, (x - 2, y - 2, 404, 34))
        pygame.draw.rect(self.screen, self.RED, (x, y, 400, 30))
        pygame.draw.rect(self.screen, self.YELLOW, (x, y, 400 * ratio, 30))

    async def connect_to_server(self):
        self.last_sent_data = None  # Add this variable to track the last sent data
        login = LoginScreen()
        self.match = login.run()
        self.match_id = self.match["id"]
        logging.debug(f"Match ID: {self.match_id}")
        logging.debug(f"Match data: {self.match}")
        if not self.match_id:
            return

        # Create animated background
        background = AnimatedBackground()

        player = Character(self.match["current player"], 300, 300, True, self.MUSK_DATA, self.musk_sheet, self.MUSK_ANIMATION_STEPS)
        opponent = Character(self.match["current player"], 300, 300, True, self.PUTIN_DATA, self.putin_sheet, self.PUTIN_ANIMATION_STEPS)

        uri = f"ws://localhost:8001/ws/game/{self.match_id}/"
        try:
            async with websockets.connect(uri) as websocket:
                logging.debug("WebSocket connection established.")
                run = True
                while run:
                    self.clock.tick(self.FPS)
                    logging.debug("Inside the game loop.")

                    # Draw background
                    self.screen.blit(self.scaled_bg, (0, 0))

                    # Update display
                    background.update()

                    # Draw characters
                    player.draw(self.screen)
                    opponent.draw(self.screen)

                    # Show player stats
                    self.draw_health_bar(player.health, 20, 20)
                    self.draw_health_bar(opponent.health, 860, 20)

                    # player movement check
                    if self.match["current player"] == 0:
                        player.move(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.screen, opponent)
                    else:
                        opponent.move(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.screen, player)

                    # Update characters
                    player.update()
                    opponent.update()

                    pygame.display.update()

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            run = False

                    # Send game data to the server only if there are changes
                    if self.match["current player"] == 0:
                        game_data = {
                            "player_id": self.match["current player"],
                            "player_position_x": player.rect.x,
                            "player_position_y": player.rect.y,
                            "player_action": player.action,
                        }
                    else:
                        game_data = {
                            "player_id": self.match["current player"],
                            "opponent_position_x": opponent.rect.x,
                            "opponent_position_y": opponent.rect.y,
                            "opponent_action": opponent.action,
                        }

                    if game_data != self.last_sent_data:
                        game_data_json = json.dumps(game_data)

                        # After sending game data to the server
                        logging.debug(f"Sending game data to the server: {game_data_json}")
                        await websocket.send(game_data_json)
                        self.last_sent_data = game_data

                    # Receive game data from the server
                    logging.debug("Waiting to receive game data from the server.")
                    try:
                        # After receiving game data from the server
                        server_data_json = await asyncio.wait_for(websocket.recv(), timeout=0.05)
                        logging.debug(f"Received game data from the server: {server_data_json}")
                        server_data = json.loads(server_data_json)

                        if self.match["current player"] == 0:
                            opponent.rect.x = server_data.get("opponent_position_x", int(opponent.rect.x))
                            opponent.rect.y = server_data.get("opponent_position_y", int(opponent.rect.y))
                            opponent.action = server_data.get("opponent_action", int(opponent.action))
                        else:
                            player.rect.x = server_data.get("player_position_x", int(player.rect.x))
                            player.rect.y = server_data.get("player_position_y", int(player.rect.y))
                            player.action = server_data.get("player_action", int(player.action))

                        logging.debug("Updated player and opponent positions.")
                    except asyncio.TimeoutError:
                        logging.debug("Timeout while waiting for game data.")
                        continue
                    except websockets.ConnectionClosed:
                        logging.debug("WebSocket connection closed.")
                        break
                    except Exception as e:
                        logging.debug(f"An error occurred while receiving game data: {e}")
                        break
                    pygame.display.update()
        except Exception as e:
            logging.error(f"Error occurred during connection: {e}")
            raise

        pygame.quit()


if __name__ == "__main__":
    client = GameClient()
    asyncio.get_event_loop().run_until_complete(client.connect_to_server())



