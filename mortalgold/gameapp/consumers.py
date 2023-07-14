from channels.generic.websocket import AsyncWebsocketConsumer
import json


class GameConsumer(AsyncWebsocketConsumer):
    player = [
        {
            "health": 100,
            "x": 200,
            "y": 450 
        }, {
            "health": 100,
            "x": 700,
            "y": 450 
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
            if self.player_id is None:
                self.player_id = player_id
                print(f"Player {player_id} connected as the main player.")
            elif self.second_player_id is None:
                self.second_player_id = player_id
                print(f"Player {player_id} connected as the second player.")
            else:
                print(f"Player {player_id} connected but the game is full.")
        elif event_type == "player_disconnected":
            if player_id == self.player_id:
                self.player_id = None
                print(f"Player {player_id} disconnected as the main player.")
            elif player_id == self.second_player_id:
                self.second_player_id = None
                print(f"Player {player_id} disconnected as the second player.")
            else:
                print(f"Unknown player {player_id} disconnected.")




    async def game_event(self, event):
        # Update the game state based on the received game data
        game_data = event["game_data"]
        
        player_id = game_data.get("player_id")
        opponent_id = int(not player_id)
        print(player_id, opponent_id)

        self.player[player_id]['health'] = game_data.get('player_health')
        self.player[opponent_id]['health'] = game_data.get('opponent_health')
        self.player[player_id]['x'] = game_data.get('player_position_x')
        self.player[opponent_id]['x'] = game_data.get('opponent_position_x')
        self.player[player_id]['y'] = game_data.get('player_position_y')
        self.player[opponent_id]['y'] = game_data.get('opponent_position_y')
        


        # self.player_health = 100
        # self.player_position_x = 200
        # self.player_position_y = 450

        # self.opponent_health = 100
        # self.opponent_position_x = 700
        # self.opponent_position_y = 450

        # self.player_id = game_data.get("player_id")

        # self.player_health = game_data.get("player_health")
        # self.player_position_x = game_data.get("player_position_x")
        # self.player_position_y = game_data.get("player_position_y")

        # self.opponent_health = game_data.get("opponent_health")
        # self.opponent_position_x = game_data.get("opponent_position_x")
        # self.opponent_position_y = game_data.get("opponent_position_y")
        # print("self.player_health", self.player_health)
        # print("self.player_position_x",  self.player_position_x)
        # print("self.player_position_y", self.player_position_y)
        # print("sending data", self.player_id)
        # print("self.opponent_health", self.opponent_health)
        # print("self.opponent_position_x",  self.opponent_position_x)
        # print("self.opponent_position_y", self.opponent_position_y)
        # print("sending data", self.player_id)

        # Send the updated game data to the client
        await self.send(text_data=json.dumps({
            # "player_id": self.player_id,
            "player_health": self.player[player_id]['health'],
            "player_position_x":  self.player[player_id]['x'],
            "player_position_y":  self.player[opponent_id]['y'],

            "opponent_health": self.player[opponent_id]['health'],
            "opponent_position_x": self.player[opponent_id]['x'],
            "opponent_position_y": self.player[opponent_id]['y']
            
        }))

