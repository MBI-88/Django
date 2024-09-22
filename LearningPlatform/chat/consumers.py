from email import message
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone

# Classes

class ChatCounsumer(AsyncWebsocketConsumer):
   async def connect(self) -> None:
        self.user = self.scope['user']
        self.id = self.scope['url_route']['kwargs']['course_id']
        self.room_group_name = 'chat_%s' % self.id
        await self.channel_layer.group_add(self.room_group_name,self.channel_name)
        await self.accept()
    
   async def disconnect(self, close_code:int) -> None:
        await self.channel_layer.group_discard(self.room_group_name,self.channel_name)
    
   async def receive(self, text_data=None) -> None:
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        now = timezone.now()
        await self.channel_layer.group_send(self.room_group_name,{
            'type':'chat_message',
            'message':message,
            'user':self.user.username,
            'datetime':now.isoformat()
        })
        
   async def chat_message(self,event) -> None:
        await self.send(text_data=json.dumps(event))