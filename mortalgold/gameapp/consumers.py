from channels.generic.websocket import AsyncWebsocketConsumer
import json


class GameConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.match_id = self.scope["url_route"]["kwargs"]["match_id"]
        self.match_group_name = f"game_{self.match_id}"

        # Join room group
        await self.channel_layer.group_add(self.match_group_name, self.channel_name)

        await self.accept()

        # Notify the group that a player has connected
        await self.channel_layer.group_send(
            self.match_group_name,
            {
                "type": "player_event",
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
                "type": "player_event",
                "event": "player_disconnected",
                "player_id": self.channel_name
            }
        )

    async def receive(self, text_data):
        # Process received data
        game_data = json.loads(text_data)

        # Send the received game data to the group
        await self.channel_layer.group_send(
            self.match_group_name,
            {
                "type": "game_event",
                "game_data": game_data
            }
        )
        print("received data.", game_data)


    async def player_event(self, event):
        # Handle player events (e.g., player connected, player disconnected)
        event_type = event["event"]
        player_id = event["player_id"]

        # Custom logic based on event type
        if event_type == "player_connected":
            print(f"Player {player_id} connected.")
        elif event_type == "player_disconnected":
            print(f"Player {player_id} disconnected.")




    async def game_event(self, event):
        # Update the game state based on the received game data
        game_data = event["game_data"]
        self.player_id = game_data.get("player_id")

        self.player_health = game_data.get("player_health")
        self.player_position_x = game_data.get("player_position_x")
        self.player_position_y = game_data.get("player_position_y")

        self.opponent_health = game_data.get("opponent_health")
        self.opponent_position_x = game_data.get("opponent_position_x")
        self.opponent_position_y = game_data.get("opponent_position_y")

        print("sending data", self.player_id)

        # Send the updated game data to the client
        await self.send(text_data=json.dumps({
            "player_id": self.player_id,

            "player_health": self.player_health,
            "player_position_x": self.player_position_x,
            "player_position_y": self.player_position_y,

            "opponent_health": self.opponent_health,
            "opponent_position_x": self.opponent_position_x,
            "opponent_position_y": self.opponent_position_y
            
        }))

