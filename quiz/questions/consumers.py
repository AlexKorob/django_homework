from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)('notifications', self.channel_name)
        self.accept()
        print('user:', self.scope["user"], "connected")

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)('notifications', self.channel_name)
        print('user:', self.scope["user"], "was disconnect")
        self.close()

    def send_msg(self, event):
        self.send(text_data=event["message"])
