import asyncio
import websockets
import json

from . import SNAPSHOT_HOST, SNAPSHOT_PORT

host = SNAPSHOT_HOST
port = SNAPSHOT_PORT

global response
response = "none"


async def requestRender(renderParams: dict):
    global response
    print(renderParams)
    async with websockets.connect(f'ws://{host}:{port}') as websocket:
        await websocket.send(json.dumps(renderParams))
        response = await websocket.recv()
        print(response)

# asyncio.get_event_loop().run_until_complete(test())
