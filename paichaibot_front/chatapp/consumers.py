from asgiref.sync import async_to_sync

from channels.generic.websocket import WebsocketConsumer
import json

from . import dialogflow_api
from . import host_observer

class ChatConsumer(WebsocketConsumer):
    __observer = host_observer.HostObserver.instance()

  	# websocket 연결 시 실행
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
          self.room_group_name,
          self.channel_name
        )
        
        self.accept()

	  # websocket 연결 종료 시 실행 
    def disconnect(self, close_code):
        # self.room_group_name -> chat_* 형태이므로 5:
        print(self.__observer.remove(self.room_group_name[5:]))
        async_to_sync(self.channel_layer.group_discard)(
          self.room_group_name,
          self.channel_name
        )

	# 클라이언트로부터 메세지를 받을 시 실행
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        text_to_be_analyzed = text_data_json['message']
		# 클라이언트로부터 받은 메세지를 다시 클라이언트로 보내준다.
        '''
        async_to_sync(self.channel_layer.group_send)(
          self.room_group_name, {
            'type': 'chat_message',
            'message': '>> ' + text_to_be_analyzed
          }
        )
        '''

        result = dialogflow_api.read_dialogflow(text_to_be_analyzed)

        async_to_sync(self.channel_layer.group_send)(
          self.room_group_name, {
            'type': 'chat_message',
            'message': dialogflow_api.read_dialogflow(text_to_be_analyzed)
          }
        )

    # room group에서 메시지 receive
    def chat_message(self, event):
        message = event['message']

        # Websocket에게 메시지 전송
        self.send(text_data=json.dumps({
            'message': message
        }))
