import json

from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer

from sav.models import emailbox


class Calculator(WebsocketConsumer):
    def connect(self):
        self.channel_name = 'livec'
        self.accept()

    def disconnect(self, close_code):
        self.close()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        expression = text_data_json['expression']
        try:
            result = eval(expression)
        except Exception as e:
            result = "Invalid Expression"
        self.send(text_data=json.dumps({
            'result': result
        }))

@sync_to_async
def get_all_email():
    return emailbox.objects.all().count()

class Websock_Mails(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'all'

        await self.channel_layer.group_add('all', self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if 'totalmail' in text_data_json:
            await self.channel_layer.group_send('all', {'type':'chatroom_message', 'nbmail':await get_all_email()})

    async def chatroom_message(self, event):
        await self.send(text_data=json.dumps(event))