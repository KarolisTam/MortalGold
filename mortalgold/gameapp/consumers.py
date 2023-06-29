    # consumers.py

from channels.generic.websocket import WebsocketConsumer
import pygame

class GameConsumer(WebsocketConsumer):
    def connect(self):
        # Initialize your Pygame game here
        pygame.init()
        # ...

        self.accept()

    def disconnect(self, close_code):
        # Clean up your Pygame game here
        pygame.quit()

    def receive(self, text_data):
        # Handle incoming WebSocket messages here
        # ...

        # Send updates to the client
        self.send(text_data)
