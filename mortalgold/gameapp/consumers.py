from channels.generic.websocket import AsyncWebsocketConsumer
import json


class GameConsumer(AsyncWebsocketConsumer):
    player = [
        {
            "x": int(200),
            "y": int(450) ,
            "action": int(0),
        }, {
            "x": int(700),
            "y": int(450) ,
            "action": int(0),
        },
    ]

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
        player_id = game_data.get("player_id")
        opponent_id = int(not player_id)
        print(opponent_id)
        print(player_id, opponent_id)
        print("opponent action:", self.player[opponent_id]['action'])
        print("player action:", self.player[player_id]['action'])

        if game_data.get('player_position_x') is not None:
            self.player[player_id]['x'] = game_data.get('player_position_x')
        else:
            pass
            # self.player[player_id]['x'] = 200

        if game_data.get('player_position_y') is not None:
            self.player[player_id]['y'] = game_data.get('player_position_y')
        else:
            pass
            # self.player[player_id]['y'] =450

        if game_data.get('player_action') is not None:
            self.player[player_id]['action'] = game_data.get('player_action')
        else:
            pass
            # self.player[player_id]['action'] = 0

        if  game_data.get('opponent_position_x') is not None:
            self.player[opponent_id]['x'] = game_data.get('opponent_position_x')
        else:
            pass
            # self.player[opponent_id]['x'] = 700

        if game_data.get('opponent_position_y') is not None:
            self.player[opponent_id]['y'] = game_data.get('opponent_position_y')
        else:
            pass
            # self.player[opponent_id]['y'] = 450

        if game_data.get('opponent_action') is not None:
            self.player[opponent_id]['action'] = game_data.get('opponent_action')
        else:
            pass
            # self.player[opponent_id]['action'] = 0
        
        # Send the updated game data to the client
        await self.send(text_data=json.dumps({
            # "player_id": self.player_id,
            "player_position_x":  self.player[player_id]['x'],
            "player_position_y":  self.player[player_id]['y'],
            "player_action":  self.player[player_id]['action'],

            "opponent_position_x": self.player[opponent_id]['x'],
            "opponent_position_y": self.player[opponent_id]['y'],
            "opponent_action": self.player[opponent_id]['action'],
        }))
        print("player_position_x",  self.player[player_id]['x'],)
        print("player_position_y",  self.player[player_id]['y'],)
        print("player_action",  self.player[player_id]['action'],)

        print("opponent_position_x", self.player[opponent_id]['x'])
        print("opponent_position_y", self.player[opponent_id]['y'])
        print("opponent_action", self.player[opponent_id]['action'])
