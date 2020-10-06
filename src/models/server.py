from telethon.sync import TelegramClient
from websockets import WebSocketServerProtocol
from telethon.errors.rpcerrorlist import AuthKeyUnregisteredError
from src.models.client import Client
import websockets
import json

class Server:
    def __init__(self):
        self.user_client = dict()

    async def get_all_dialogs(self, websocket: WebSocketServerProtocol, message: dict):
        client = await self.get_client(websocket, message['username'])
        try:
            dialogs = await client.get_dialogs()
        except AuthKeyUnregisteredError:
            answer = {'status': 'Warning', 'action': 'send_number',
                      'text': 'Need authorize, please send telegram phone number!'}
            answer_json = json.dumps(answer)
            return answer_json

        view_dialogs = []
        limit = 50
        if 'limit' in message:
            if message['limit']:
                limit = message['limit']
        for i, dialog in enumerate(dialogs):
            dialog_common_data = {
                'dialog_id': str(dialog.id),
                'dialog_name': str(dialog.name),
                'date_last_message': str(dialog.date),
                'unread_count': str(dialog.unread_count),
                'first_message_text': str(dialog.message.message)
            }
            view_dialogs.append(dialog_common_data)
            if i == limit:
                break

        answer = {'action': 'show_all_dialogs', 'text': view_dialogs}
        answer_json = json.dumps(answer, ensure_ascii=False)
        return answer_json

    async def get_client(self, websocket: WebSocketServerProtocol, username):
        if username not in self.user_client.keys():
            client = Client(websocket, username)
            client.websocket = websocket
            await client.connect_to_telegram()
            self.user_client[username] = client.connection

        return self.user_client[username]

    async def send_code_to_telegram(self, websocket: WebSocketServerProtocol, message: dict):
        client = await self.get_client(websocket, message['username'])
        try:
            await client.sign_in(message['phone'], message['code'])
        except:
            answer = {'status': 'Error', 'text': 'incorrect data'}
            answer_json = json.dumps(answer)
            return answer_json

        answer = {'status': 'OK', 'text': 'you are authorized!'}
        answer_json = json.dumps(answer)
        return answer_json

    async def send_phone_to_telegram(self, websocket: WebSocketServerProtocol, message: dict):
        client = await self.get_client(websocket, message['username'])
        await client.send_code_request(message['phone'])

        answer = {'status': 'Warning', 'action': 'send_code', 'text': 'Need authorize, please send code from telegram!'}
        answer_json = json.dumps(answer)
        return answer_json

    async def send_message(self, websocket: WebSocketServerProtocol, message: dict):
        send_to = message['send_to']
        text = message['text']
        client = await self.get_client(websocket, message['username'])

        if not await client.is_user_authorized():
            answer = {'status': 'Warning', 'action': 'send_number',
                      'text': 'Need authorize, please send telegram phone number!'}
            answer_json = json.dumps(answer)
            return answer_json

        await client.send_message(send_to, text)
        return {'status': 'OK', 'action': 'Send message'}

    async def accept_request(self, websocket: WebSocketServerProtocol, uri: str):
        message = await websocket.recv()
        json_message = json.loads(message)
        answer = None
        if json_message['action'] == 'get_all_dialogs':
            answer = await self.get_all_dialogs(websocket, json_message)
        elif json_message['action'] == 'send_message':
            answer = await self.send_message(websocket, json_message)
        elif json_message['action'] == 'send_number':
            answer = await self.send_phone_to_telegram(websocket, json_message)
        elif json_message['action'] == 'send_code':
            answer = await self.send_code_to_telegram(websocket, json_message)
        elif json_message['action'] == 'info':
            print(self.user_client)
        if answer:
            await websocket.send(answer)
