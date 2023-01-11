import json

import os
import random
import subprocess
from random import randint

from modtools.modbase import ModularStart
from modtools.modbase.ModularBase import ModularBase

base = ModularBase()
base.initCR()

from . import SNAPSHOT_HOST, SNAPSHOT_PORT, SNAPSHOT_RES, SNAPSHOT_EXTENSION, SNAPSHOT_HEADLESS, SNAPSHOT_DIR

x, y = [SNAPSHOT_RES] * 2

# ensure we can actually see nametags when we wanna call for them
base.initNametagGlobals()

# base.resetGSG(updateFilters=False)

from modtools.extensions.toon_snapshot.snapshot.ToonSnapshot import ToonSnapshot
from modtools.extensions.toon_snapshot.snapshot.DoodleSnapshot import DoodleSnapshot
from modtools.extensions.toon_snapshot.snapshot.SuitSnapshot import SuitSnapshot

from modtools.extensions.toon_snapshot.snapshot.RenderEnums import *


toonSnapshot = ToonSnapshot(x, y, SNAPSHOT_HEADLESS)
doodleSnapshot = DoodleSnapshot(x, y, SNAPSHOT_HEADLESS)
suitSnapshot = SuitSnapshot(x, y, SNAPSHOT_HEADLESS)

id2snapshot= {
    RenderType.Toon: toonSnapshot,
    RenderType.Doodle: doodleSnapshot,
    RenderType.Suit: suitSnapshot,
    RenderType.NPC: toonSnapshot,
    "toon": toonSnapshot,
    "doodle": doodleSnapshot,
    "suit": suitSnapshot,
    "npc": toonSnapshot,

}

###
from toontown.toon import NPCToons

###

import asyncio
import websockets


# create handler for each connection
async def handler(websocket, path):
    data = await websocket.recv()
    data = json.loads(data)
    outputData = dict()

    toonid = randint(0, 1000)  # should be sent with packet
    snapshot = id2snapshot[data.get("RENDER_TYPE")]
    snapshot.filename = f"{SNAPSHOT_DIR}/{toonid}{SNAPSHOT_EXTENSION}"

    if data.get("FRAME_TYPE") == FrameType.Random:
        # flip a coin
        bodyShot = bool(random.getrandbits(1))
    else:
        bodyShot = data.get("FRAME_TYPE") == FrameType.Bodyshot

    bubbleType = data.get("CHAT_BUBBLE_TYPE")
    # to do clean later
    if bubbleType == ChatBubbleType.Random:
        # flip a coin
        coin = bool(random.getrandbits(1))
        if coin:
            bubbleType = ChatBubbleType.Normal
        else:
            bubbleType = ChatBubbleType.Thought

    if snapshot.type == RenderType.Toon:
        npcID = None
        randomDNA = data.get("DNA_RANDOM")
        if data.get("RENDER_TYPE") == RenderType.NPC:
            npcID = data.get("NPC_ID")
            if not npcID:
                npcID = random.choice(list(NPCToons.NPCToonDict.items()))[0]
            randomDNA = False
        elif data.get("RENDER_TYPE") == RenderType.Toon:
            randomDNA = True
        snapshot.loadToon(
            randomDNA = randomDNA,
            npcID=npcID,
            bodyShot = bodyShot,
            wantNametag = data.get("WANT_NAMETAG"),
            customName = data.get("NAME"),
            customPhrase = data.get("CUSTOM_PHRASE"),
            chatBubbleType = bubbleType,
        )

    elif data.get("RENDER_TYPE") == RenderType.Doodle:
        snapshot.loadDoodle(
            doodleName = data.get("NAME"),
            customPhrase = data.get("CUSTOM_PHRASE"),
            wantNametag = data.get("WANT_NAMETAG"),
            chatBubbleType = bubbleType,
        )
    elif data.get("RENDER_TYPE") == RenderType.Suit:
        snapshot.loadSuit(
            randomDNA = data.get("DNA_RANDOM"),
            haphazardDNA = data.get("DNA_HAPHAZARD"),
            wantNametag = data.get("WANT_NAMETAG"),
            suitName = data.get("NAME"),
            customPhrase = data.get("CUSTOM_PHRASE"),
            bodyShot = bodyShot,
            chatBubbleType = bubbleType,

        )
    else:
        #panic
        snapshot.loadDoodle()

    snapshot.doSnapshot()
    name_temp = snapshot.getInfo()[0]
    snapshot.cleanup()
    reply = snapshot.filename
    outputData["RENDER_IMAGE"] = snapshot.filename
    outputData["ACTOR_NAME"] = name_temp

    imgMagickPath = os.environ.get("IMAGEMAGICK_PATH") + "\\" if os.environ.get("IMAGEMAGICK_PATH") else ""
    subprocess.call([f"{imgMagickPath}convert.exe", reply, '-trim', reply])
    await websocket.send(json.dumps(outputData))


start_server = websockets.serve(handler, str(SNAPSHOT_HOST), SNAPSHOT_PORT)

asyncio.get_event_loop().run_until_complete(start_server)

asyncio.get_event_loop().run_forever()