import json
import re
from bs4 import BeautifulSoup
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from datetime import datetime
from .models.messages import Message
from channels.generic.websocket import AsyncWebsocketConsumer
from captcha.models import CaptchaStore

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
        reply = text_data_json["reply"]
        
        
        # Validate
        val = MessageFormValidator(text_data_json)
        v_errors = val.start()
        
        if v_errors:
            self.send(text_data=json.dumps({
                "type": "error",
                "errors": " ".join(v_errors),
            }))
            return
        
        reply_for = None
        if reply:
            reply_class = Message.objects.get(id=reply)
            reply_for = reply_class.user_name
            
        else: 
            reply_class = None
        
        new_message = Message.objects.create(
            user_name=user_name,
            email=email,
            home_page=home_page,
            text=message,
            created=created,
            reply=reply_class,
        )
        
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "id": new_message.id,
                'user_name': user_name,
                'email': email,
                'home_page': home_page,
                'created': created,
                'message': message,
                'reply': reply,
                'reply_for': reply_for,
            }
        )

        
    def chat_message(self, event):
        self.send(text_data=json.dumps({
            "type": "chat",
            'id': event["id"],
            'user_name': event["user_name"],
            'email': event["email"],
            'home_page': event["home_page"],
            'created': event["created"],
            'message': event["message"],
            'reply': event["reply"],
            'reply_for': event["reply_for"],
        }))
        


class MessageFormValidator:
    def __init__(self, text_data_json):
        self.text_data_json = text_data_json
    
    def start(self):
        errors = []
        result1 = self.user_name()
        result2 = self.captcha()
        result3 = self.message()
        if result1: 
            errors.append(result1)
        if result2: 
            errors.append(result2)
        if result3: 
            errors.append(result3)
        return errors if errors else False
    
    def user_name(self): 
        user_name = self.text_data_json["user_name"]
        if not re.compile("^[a-zA-Z0-9]+$").match(user_name):
            return "User_name может состоять только из латинских букв и цифр."
        return False
    
    def message(self):
        message = self.text_data_json["message"]
        
        allowed_tags = ['a', 'code', 'i', 'strong']

        soup = BeautifulSoup(message, 'html.parser')
        if str(soup) != message:
            return "Теги не закрыты корректно."
            
        for tag in soup.find_all():
            if tag.name not in allowed_tags:
                return f"Найден неразрешённый тег: {tag.name}"
        return False

    def captcha(self): 
        captcha:list[str] = self.text_data_json["captcha"]
        try:
            captcha_0 = CaptchaStore.objects.get(hashkey=captcha[0])
            if captcha_0.response != captcha[1].lower():
                return "Неверная капча."
            # captcha_0.delete()
        except CaptchaStore.DoesNotExist:
            return "Капча устарела или недействительна."
        
        return False
