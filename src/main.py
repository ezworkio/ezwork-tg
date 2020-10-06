import logging
import websockets
import asyncio
from src.models.server import Server


if __name__ == "__main__":
    server = Server()
    loop = asyncio.get_event_loop()
    print('Good luck!')
    start_communication = websockets.serve(server.accept_request, host='localhost', port=4000)
    loop.run_until_complete(start_communication)
    loop.run_forever()

