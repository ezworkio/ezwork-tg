from websockets import WebSocketServerProtocol
import asyncio
import websockets
import logging
import json

logging.basicConfig(level=logging.INFO)


async def produce(message: str, host: str, port: int) -> None:
    async with websockets.connect(f"ws://{host}:{port}") as websocket:
        await websocket.send(message)
        ans = await websocket.recv()
        print(ans)

'''
actions:
get_all_dialogs (username, limit=None)
send_message (username, send_to, text)
send_number (username, phone)
send_code (username, phone, code)
info
'''

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    m = {
        'action': 'send_message',
        'send_to': 'constaat',
        'text': 'курлык',
        'phone': '89969383408',
        'code': '46075',
        'username': 'constaat',
        'limit': '5'
        }
    m_json = json.dumps(m)
    loop.run_until_complete(produce(m_json, host='localhost', port=4000))
    loop.run_forever()
