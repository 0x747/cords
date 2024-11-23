import json
from django.template import loader
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .utils.snowflake import Snowflake

snowflake = Snowflake()

class ChatConsumer(WebsocketConsumer):

    def connect(self):
        from .models import Chat

        self.user = self.scope['user']
        self.root_url = str(self.scope["headers"][6][1])[2:-1]
        self.room_name = self.scope["url_route"]["kwargs"]["pk"]
        self.chat = Chat.objects.get(id=self.room_name)
        self.room_group_name = f'chat_{self.room_name}'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

        self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'Connected!'
        }))
    
    def receive(self, text_data):
        from .models import Message, Notification
        text_data_json = json.loads(text_data)
        chat_message = text_data_json['message']

        print(f'{self.user.username}: {chat_message}')

        if chat_message:
            message = Message.objects.create(id=snowflake.generate_id(), chat=self.chat, author=self.user, content=chat_message)
            message.save()

            if self.user != self.chat.recipient:
                notification = Notification.objects.create(id=snowflake.generate_id(), notification_type=3, initiator=self.user, recipient=self.chat.recipient, message=message)
            else:
                notification = Notification.objects.create(id=snowflake.generate_id(), notification_type=3, initiator=self.user, recipient=self.chat.initiator, message=message)

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'user': self.user,
                    'message': message,
                    'chat': self.chat,
                    'root_url': self.root_url
                }
            )
    
    def chat_message(self, event):
        #notification = loader.get_template('chat_notification.html').render(context={'chat': event['chat']})
        message_html = loader.get_template('chat_message.html').render(context={'message': event['message'], 'current_user': event['user'], 'root_url': event['root_url']})

        self.send(text_data=message_html)

    def disconnect(self, close_code):
        pass
