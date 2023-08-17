import time

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer


import json
from channels.generic.websocket import WebsocketConsumer


class Cartcreating(WebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            'cartcreating',
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        print("Closed websocket with code: ", close_code)
        async_to_sync(self.channel_layer.group_discard)(
            'cartcreating',
            self.channel_name
        )
        self.close()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        expression = text_data_json['expression']
        try:
            result = eval(expression)
        except Exception as e:
            result = "Invalid Expression"
        self.send(text_data=json.dumps({
            'message': result
        }))

    def channel_message(self, event):
        del event['type']

        # Send message to WebSocket
        self.send(text_data=json.dumps(event))

class production(WebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            'production',
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        print("Closed websocket with code: ", close_code)
        async_to_sync(self.channel_layer.group_discard)(
            'production',
            self.channel_name
        )
        self.close()

    def channel_message(self, event):
        # del event['type']

        # Send message to WebSocket
        self.send(text_data=json.dumps(event))

class updateDB(WebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            'updateDB',
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        print("Closed websocket with code: ", close_code)
        async_to_sync(self.channel_layer.group_discard)(
            'updateDB',
            self.channel_name
        )
        self.close()

    def channel_message(self, event):
        # del event['type']

        # Send message to WebSocket
        self.send(text_data=json.dumps(event))