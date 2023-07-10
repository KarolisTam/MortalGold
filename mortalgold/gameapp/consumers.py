from channels.generic.websocket import SyncConsumer
import json
from . import models

class GameConsumer(SyncConsumer):
    def websocket_connect(self, event):
        self.send({
            "type": "websocket.accept"
        })
        print("Connected")

    def websocket_disconnect(self, event):
        pass

    def websocket_receive(self, event):
        text_data = event["text"]
        game_data = json.loads(text_data)
        
        # Process the received game data
        # Update game state based on the received data
        
        # Example: Update player positions
        player1_position_x = game_data.get("player1_position_x")
        player1_position_y = game_data.get("player1_position_y")
        player2_position_x = game_data.get("player2_position_x")
        player2_position_y = game_data.get("player2_position_y")
        
        models.GameAction
        # Example: Update player health
        player1_health = game_data.get("player1_health")
        player2_health = game_data.get("player2_health")
        
        # Update game state and perform other game logic here
        
        # Prepare the server response
        response_data = {
            "status": "success",
            "message": "Game state updated successfully",
            # Include any other relevant data to send back to the client
        }
        response_text = json.dumps(response_data)
        
        # Send the response back to the client
        self.send({
            "type": "websocket.send",
            "text": response_text
        })
        print(f"Sent {game_data, response_text}")
        print(f"Sent {response_text}")
