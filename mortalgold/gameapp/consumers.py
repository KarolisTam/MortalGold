

from channels.generic.websocket import SyncConsumer

class EchoConsumer(SyncConsumer):
    def websocket_connect(self, event):
        self.send({
            "type": "websocket.accept"
        })
        print("Connected")

    def websocket_disconnect(self, event):
        pass

    def websocket_receive(self, event):
        text_data = event["text"]
        self.send({
            "type": "websocket.send",
            "text": text_data
        })
        print("Sent")
