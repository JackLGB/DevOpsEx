import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    room_group_name = None

    async def connect(self):
        self.room_group_name = 'chat_%s' % self.scope['url_route']['kwargs']['room_name']
        # self.setClientInfo()
        self.setRoomGroupName()
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        """
        接收信息
        :param text_data: 字符串信息
        :param bytes_data: 字节信息
        :return:
        """
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        print("====chat_message====")
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    def setClientInfo(self, client: tuple = None) -> None:
        """
        设置客户端信息
        :param client: (host,port)
        :return:
        """
        self.host, self.port = client if client else self.scope['client']

    def getClientInfo(self) -> tuple:
        """
        获取客户端信息
        :return: (host,port)
        """
        return self.host, self.port

    def setRoomGroupName(self, room_group_name: str = None) -> None:
        """
        设置房间组名
        :param room_group_name:
        :return:
        """
        self.room_group_name = room_group_name if room_group_name else \
            'chat_%s' % self.scope['url_route']['kwargs']['room_name']

    def getRoomGroupName(self) -> str:
        return self.room_group_name
