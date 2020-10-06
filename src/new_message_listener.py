import asyncio
import websockets
import logging
import json

logging.basicConfig(level=logging.INFO)


async def listen(host: str, port: int) -> None:
    async with websockets.connect(f"ws://{host}:{port}") as websocket:
        ans = await websocket.recv()
        print(ans)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    start_communication = websockets.serve(listen, host='localhost', port=4001)
    loop.run_until_complete(start_communication)
    loop.run_forever()
