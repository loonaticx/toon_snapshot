import asyncio
import time

from random import random

import websockets
import json

from . import SNAPSHOT_HOST, SNAPSHOT_PORT

host = SNAPSHOT_HOST
port = SNAPSHOT_PORT

global response
response = "none"


async def requestRender(renderParams: dict):
    global response
    response = "none"
    if not renderParams:
        return
    # try to mitigate dupe picture sending?
    await asyncio.sleep(1)
    async with websockets.connect(f'ws://{host}:{port}') as websocket:
        await websocket.send(json.dumps(renderParams))
        response = await websocket.recv()
    return response

import nest_asyncio

nest_asyncio.apply()
queueServ = asyncio.Queue()

testDict = {
    "TEST": f"{random()}"
}
# coroutine to generate work
async def producer(queue, inputData):
    print('Producer: Running')
    # generate work
    # for i in range(10):
    # generate a value
    value = random()
    # block to simulate work
    await asyncio.sleep(1)

    # await asyncio.sleep(value)
    # add to the queue
    test = {
        "TEST": f"{time.time()}"
    }
    await queue.put(inputData)
    # send an all done signal
    # await queue.put(None)
    print('Producer: Done')


# coroutine to consume work
async def consumer(queue):
    print('Consumer: Running')
    # consume work
    while True:
        # get a unit of work
        item = await queue.get()
        print(item)

        # await asyncio.sleep(5)

        # check for stop signal
        if item is None:
            break

        # result = json.loads(asyncio.get_event_loop().run_until_complete(requestRender(item)))
        result = await requestRender(item)
        # report
        # result = json.loads(requestRender.response)
        print(f'>got {result}')
    # all done
    print('Consumer: Done')


# entry point coroutine
async def main():
    # create the shared queue
    # run the producer and consumers
    inputData = {
        "TEST": f"{time.time()}"
    }
    await asyncio.gather(producer(queueServ, inputData), consumer(queueServ))


# start the asyncio program
# asyncio.run(main())

# asyncio.get_event_loop().run_until_complete(test())
