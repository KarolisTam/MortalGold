from channels.consumer import SyncConsumer

class EchoConsumer(SyncConsumer):

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, data):
        self.send(text_data=data)
# async def main():
#     async with websockets.serve(hello, "localhost", 8765):
#         await asyncio.Future()  # run forever
