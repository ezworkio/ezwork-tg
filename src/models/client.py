from websockets import WebSocketServerProtocol
from telethon.sync import TelegramClient, events
import configparser
import websockets
import json

class Client:
    def __init__(self, websocket: WebSocketServerProtocol, username):
        config = configparser.ConfigParser()
        config.read("src/utils/config2.ini")

        # Присваиваем значения внутренним переменным
        self.api_id = int(config['Telegram']['api_id'])
        self.api_hash = config['Telegram']['api_hash']
        self.username = username

        self.host = websocket._host
        self.port = websocket._port

        self.websocket = websocket

        self.connection = TelegramClient(self.username, self.api_id, self.api_hash)

        client = self.connection

        @staticmethod
        @client.on(events.NewMessage())
        async def my_event_handler(event):
            async with websockets.connect(f"ws://localhost:4001") as websocket:
                message = {
                    'from_chat': event._chat_peer.__dict__,
                    'from_id': event.message.from_id,
                    'text': event.message.message
                }
                message = json.dumps(message)
                await websocket.send(message)

    async def connect_to_telegram(self):
        await self.connection.connect()
