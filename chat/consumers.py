import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from datetime import datetime
from django.core.paginator import Paginator
from .models.messages import Message

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = "test"
        
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        
        messages = Message.objects.all().order_by("-created")
        paginator = Paginator(messages, 6)
        try:
            current_page_mes = paginator.page(1)
        except:
            current_page_mes = []
        
        message_list = []
        for message in current_page_mes:
            message_list.append({
                'user_name': message.user_name,
                'email': message.email,
                'home_page': message.home_page,
                'created': message.created.strftime('%d.%m.%Y %H:%M'),
                'message': message.text,
            })
        
        # print(message_list)
        
        self.send(text_data=json.dumps({
            "type":"connection_established",
            "message":"You are now connected!!!",
            "message_list": message_list, 
        }))
        
        
    
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        user_name = text_data_json["user_name"]
        email = text_data_json["email"]
        home_page = text_data_json["home_page"]
        message = text_data_json["message"]
        created = datetime.now().strftime('%d.%m.%Y %H:%M')
        
        
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                'user_name': user_name,
                'email': email,
                'home_page': home_page,
                'created': created,
                'message': message,
            }
        )
        
    def chat_message(self, event):
        user_name = event["user_name"]
        email = event["email"]
        home_page = event["home_page"]
        created = event["created"]
        message = event["message"]
        
        Message.objects.create(
            user_name=user_name,
            email=email,
            home_page=home_page,
            text=message,
            created=created,
            # reply=None,
        )
        
        self.send(text_data=json.dumps({
            "type": "chat",
            'user_name': user_name,
            'email': email,
            'home_page': home_page,
            'created': created,
            'message': message,
        }))
        
        
    # def disconnect(self, close_code):
    #     pass
    