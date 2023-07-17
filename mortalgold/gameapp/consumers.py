# consumers.py
import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer

# Set up the logger to the root logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class GameConsumer(AsyncWebsocketConsumer):
    players = [
        {"x": 200, "y": 450, "action": 0},
        {"x": 700, "y": 450, "action": 0}
    ]

    async def connect(self):
        # Get the match_id from the URL route parameters
        self.match_id = self.scope["url_route"]["kwargs"]["match_id"]
        self.match_group_name = f"game_{self.match_id}"
        await self.channel_layer.group_add(self.match_group_name, self.channel_name)
        await self.accept()
        await self.notify_player_connected()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.match_group_name, self.channel_name)
        await self.notify_player_disconnected()

    async def receive(self, text_data):
        game_data = json.loads(text_data)
        await self.send_game_data_to_group(game_data)
        logger.debug("Received data: %s", game_data)

    async def player_event(self, event):
        event_type = event["event"]
        player_id = event["player_id"]
        if event_type == "player_connected":
            logger.info("Player %s connected.", player_id)
        elif event_type == "player_disconnected":
            logger.info("Player %s disconnected.", player_id)

    async def game_event(self, event):
        game_data = event["game_data"]
        player_id = game_data.get("player_id")
        opponent_id = int(not player_id)

        logger.debug("Received game event with data: %s", game_data)

        self.update_player_data(game_data, player_id, opponent_id)
        await self.send_updated_game_data(player_id, opponent_id)
        logger.debug("Sent updated game data to client.")
        logger.debug(game_data)

    async def notify_player_connected(self):
        await self.channel_layer.group_send(
            self.match_group_name,
            {"type": "player_event", "event": "player_connected", "player_id": self.channel_name}
        )

    async def notify_player_disconnected(self):
        await self.channel_layer.group_send(
            self.match_group_name,
            {"type": "player_event", "event": "player_disconnected", "player_id": self.channel_name}
        )

    async def send_game_data_to_group(self, game_data):
        await self.channel_layer.group_send(
            self.match_group_name,
            {"type": "game_event", "game_data": game_data}
        )

    def update_player_data(self, game_data, player_id, opponent_id):
        # Update opponent position and action if available
        if player_id == 0:
            if game_data.get('opponent_position_x') is not None:
                self.players[opponent_id]['x'] = game_data.get('opponent_position_x')
            if game_data.get('opponent_position_y') is not None:
                self.players[opponent_id]['y'] = game_data.get('opponent_position_y')
            if game_data.get('opponent_action') is not None:
                self.players[opponent_id]['action'] = game_data.get('opponent_action')

        # Update player position and action if available
        if player_id == 1:
            if game_data.get('player_position_x') is not None:
                self.players[player_id]['x'] = game_data.get('player_position_x')
            if game_data.get('player_position_y') is not None:
                self.players[player_id]['y'] = game_data.get('player_position_y')
            if game_data.get('player_action') is not None:
                self.players[player_id]['action'] = game_data.get('player_action')

        logger.debug("Updated Opponent Data: %s", self.players[opponent_id])


    async def send_updated_game_data(self, player_id, opponent_id):
        await self.send(text_data=json.dumps({
            "player_position_x": self.players[player_id]['x'],
            "player_position_y": self.players[player_id]['y'],
            "player_action": self.players[player_id]['action'],

            "opponent_position_x": self.players[opponent_id]['x'],
            "opponent_position_y": self.players[opponent_id]['y'],
            "opponent_action": self.players[opponent_id]['action']
        }))
