import pygame
import asyncio
import websockets
import json
import logging

from character import Character
from opponent import Opponent
from background import AnimatedBackground
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

        # Define colours
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 255, 0)
        self.WHITE = (255, 255, 255)

        # Define character variables
        self.PUTIN_SIZE = 200
        self.PUTIN_SCALE = 1
        self.PUTIN_OFFSET = [62, 20]
        self.PUTIN_DATA = [self.PUTIN_SIZE, self.PUTIN_SCALE, self.PUTIN_OFFSET]

        self.MUSK_SIZE = 200
        self.MUSK_SCALE = 1
        self.MUSK_OFFSET = [62, 20]
        self.MUSK_DATA = [self.MUSK_SIZE, self.MUSK_SCALE, self.MUSK_OFFSET]

        # Load background image
        bg_image = pygame.image.load("assets/images/background/bg.png").convert_alpha()
        self.scaled_bg = pygame.transform.scale(bg_image, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        # Load spritesheets
        self.putin_sheet = pygame.image.load("assets/images/putin/sprites/putin.png").convert_alpha()
        self.musk_sheet = pygame.image.load("assets/images/musk/sprites/musk.png").convert_alpha()

        # Define number of steps in each animation
        self.PUTIN_ANIMATION_STEPS = [7, 4, 1, 5, 5, 4, 9, 1]
        self.MUSK_ANIMATION_STEPS = [7, 6, 1, 5, 5, 4, 10, 1]

    def draw_health_bar(self, health, x, y):
        ratio = health / 100
        pygame.draw.rect(self.screen, self.WHITE, (x - 2, y - 2, 404, 34))
        pygame.draw.rect(self.screen, self.RED, (x, y, 400, 30))
        pygame.draw.rect(self.screen, self.YELLOW, (x, y, 400 * ratio, 30))

    async def connect_to_server(self):
        self.last_sent_data = None
        login = LoginScreen()
        self.match = login.run()
        self.match_id = self.match["id"]
        logging.debug(f"Match ID: {self.match_id}")
        logging.debug(f"Match data: {self.match}")
        if not self.match_id:
            return

        self.player = self.match["current player"]
        self.opponent = int(not self.match["current player"])

        background = AnimatedBackground()

        if not self.player:
            player = Character(200, 300, True, self.MUSK_DATA, self.musk_sheet, self.MUSK_ANIMATION_STEPS)
            opponent = Opponent(700, 300, True, self.PUTIN_DATA, self.putin_sheet, self.PUTIN_ANIMATION_STEPS)
        else:
            opponent = Opponent(200, 300, True, self.MUSK_DATA, self.musk_sheet, self.MUSK_ANIMATION_STEPS)
            player = Character(700, 300, True, self.PUTIN_DATA, self.putin_sheet, self.PUTIN_ANIMATION_STEPS)

        uri = f"ws://localhost:8001/ws/game/{self.match_id}/"
        try:
            async with websockets.connect(uri) as websocket:
                logging.debug("WebSocket connection established.")
                run = True
                while run:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            run = False

                    self.clock.tick(self.FPS)

                    self.screen.blit(self.scaled_bg, (0, 0))

                    background.update()
                    background.draw(self.screen)

                    player.draw(self.screen)
                    opponent.draw(self.screen)

                    if not self.player:
                        self.draw_health_bar(player.health, 20, 20)
                        self.draw_health_bar(opponent.health, 860, 20)
                    else:
                        self.draw_health_bar(opponent.health, 20, 20)
                        self.draw_health_bar(player.health, 860, 20)

                    player.move(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.screen, opponent)

                    if player.rect.centerx > opponent.rect.centerx:
                        opponent.flip = False
                    else:
                        opponent.flip = True

                    player.update()
                    opponent.update_animation()
                    pygame.display.update()

                    game_data = {
                        "player_id": self.match["current player"],
                        "player_position_x": player.rect.x,
                        "player_position_y": player.rect.y,
                        "player_health": player.health,
                        "player_action": player.action,

                        "opponent_health": opponent.health,
                        "opponent_action": opponent.action,
                    }

                    if game_data != self.last_sent_data:
                        game_data_json = json.dumps(game_data)
                        logging.debug(f"Sending game data to the server: {game_data_json}")
                        await websocket.send(game_data_json)
                        self.last_sent_data = game_data

                    try:
                        player_id = self.match["current player"]
                        opponent_id = int(not self.match["current player"])
                        server_data_json = await asyncio.wait_for(websocket.recv(), timeout=0.06)
                        server_data = json.loads(server_data_json)

                        opponent.rect.x = server_data.get(f"player{opponent_id}_position_x", int(opponent.rect.x))
                        opponent.rect.y = server_data.get(f"player{opponent_id}_position_y", int(opponent.rect.y))
                        opponent.action = server_data.get(f"player{opponent_id}_action", int(opponent.action))

                        if not self.player:
                            player.health = server_data.get(f"player{player_id}_health", int(opponent.health))
                        else:
                            opponent.health = server_data.get(f"player{opponent_id}_health", int(player.health))
                            player.health = server_data.get(f"player{player_id}_health", int(opponent.health))
                    except asyncio.TimeoutError:
                        continue
                    except websockets.ConnectionClosed:
                        logging.debug("WebSocket connection closed.")
                        break
                    except Exception as e:
                        logging.debug(f"An error occurred while receiving game data: {e}")
                        break
        except Exception as e:
            logging.error(f"Error occurred during connection: {e}")
            raise
        pygame.quit()

if __name__ == "__main__":
    client = GameClient()
    asyncio.get_event_loop().run_until_complete(client.connect_to_server())
