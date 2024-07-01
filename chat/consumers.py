import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from datetime import datetime

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = "test"
        
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        
        
        
        self.send(text_data=json.dumps({
            "type":"connection_established",
            "message":"You are now connected!!!",
            "message_list": ["test", "test2",] 
        }))
        
        
    
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        user_name = text_data_json["user_name"]
        email = text_data_json["email"]
        home_page = text_data_json["home_page"]
        message = text_data_json["message"]
        date_time = datetime.now().strftime('%Y.%m.%d %H:%M')
        
        
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                'user_name': user_name,
                'email': email,
                'home_page': home_page,
                'date_time': date_time,
                'message': message,
            }
        )
        
        
        # print("Message:", message)
        
        # self.send(text_data=json.dumps({
        #     "type":"chat",
        #     "message": message,
        # }))
        
    def chat_message(self, event):
        user_name = event["user_name"]
        email = event["email"]
        home_page = event["home_page"]
        date_time = event["date_time"]
        message = event["message"]
        
        self.send(text_data=json.dumps({
            "type": "chat",
            'user_name': user_name,
            'email': email,
            'home_page': home_page,
            'date_time': date_time,
            'message': message,
        }))
        
        
    # def disconnect(self, close_code):
    #     pass
    