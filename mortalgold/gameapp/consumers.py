# consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json


class GameConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player = None

    async def connect(self):
        self.match_id = self.scope["url_route"]["kwargs"]["match_id"]
        self.match_group_name = f"game_{self.match_id}"

        # Join room group
        await self.channel_layer.group_add(self.match_group_name, self.channel_name)

        await self.accept()
        print("Player connected!")

        # Notify the group that a player has connected
        await self.channel_layer.group_send(
            self.match_group_name,
            {
                "type": "game_event",
                "event": "player_connected",
                "player_id": self.channel_name
            }
        )

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.match_group_name, self.channel_name)

        # Notify the group that a player has disconnected
        await self.channel_layer.group_send(
            self.match_group_name,
            {
                "type": "game_event",
                "event": "player_disconnected",
                "player_id": self.channel_name
            }
        )

    async def receive(self, text_data):
        # Process received data
        game_data = json.loads(text_data)

        # Perform actions with the game data

        # Example: Update player health
        player_health = game_data.get("player_health")
        opponent_health = game_data.get("opponent_health")

        # Send response back to the client
        response_data = {
            "player_health": player_health,
            "opponent_health": opponent_health,
        }
        response_json = json.dumps(response_data)
        await self.send(text_data=response_json)
        # print(game_data)
        # print("player health", player_health)
        # print("opponent health", opponent_health)

    async def game_event(self, event):
        # Handle game events sent from the server
        event_type = event.get("event")

        if event_type == "player_connected":
            # Retrieve the player ID from the event
            player_id = event.get("player_id")
            print("player: ", player_id)

            # Broadcast the player connection to other players
            if player_id != self.channel_name:
                response_data = {
                    "event": "player_connected",
                    "player_id": player_id,
                    # "player_health": self.player.health if self.player else 0,
                }
                response_json = json.dumps(response_data)
                await self.send(text_data=response_json)


        elif event_type == "player_disconnected":
            # Retrieve the player ID from the event
            player_id = event.get("player_id")

            # Broadcast the player disconnection to other players
            if player_id != self.channel_name:
                response_data = {
                    "event": "player_disconnected",
                    "player_id": player_id
                }
                response_json = json.dumps(response_data)
                await self.send(text_data=response_json)
