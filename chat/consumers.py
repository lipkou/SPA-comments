import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from captcha.models import CaptchaStore
from datetime import datetime
from .models.messages import Message

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = "test"
        
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        
    
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        user_name = text_data_json["user_name"]
        email = text_data_json["email"]
        home_page = text_data_json["home_page"]
        message = text_data_json["message"]
        created = datetime.now().strftime('%d.%m.%Y %H:%M')
        captcha:list[str] = text_data_json["captcha"]
        
        
        try:
            captcha_0 = CaptchaStore.objects.get(hashkey=captcha[0])
            if captcha_0.response != captcha[1].lower():
                self.send(text_data=json.dumps({
                    "type": "error",
                    "errors": "Неверная капча",
                }))
                return
            # captcha_0.delete()
        except CaptchaStore.DoesNotExist:
            self.send(text_data=json.dumps({
                "type": "error",
                "errors": "Капча устарела или недействительна",
            }))
            return

        
        Message.objects.create(
            user_name=user_name,
            email=email,
            home_page=home_page,
            text=message,
            created=created,
            # reply=None,
        )
        
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
        self.send(text_data=json.dumps({
            "type": "chat",
            'user_name': event["user_name"],
            'email': event["email"],
            'home_page': event["home_page"],
            'created': event["created"],
            'message': event["message"],
        }))
        
        
    # def disconnect(self, close_code):
    #     pass
    