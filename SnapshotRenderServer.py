from panda3d.core import loadPrcFileData

from . import SNAPSHOT_HOST, SNAPSHOT_PORT, SNAPSHOT_RES, SNAPSHOT_EXTENSION, SNAPSHOT_HEADLESS, SNAPSHOT_DIR, \
    SNAPSHOT_TRIM_WHITESPACE

import json

import os
import random
import subprocess
from random import randint

from modtools.modbase import ModularStart
from modtools.modbase.ModularBase import ModularBase
from .snapshot.SnapshotUtils import crop_images

if SNAPSHOT_HEADLESS:
    pipe = 'offscreen'
else:
    pipe = 'pandagl'

# fun little hack to make sure headless can work :)
loadPrcFileData('', 'inactivity-timeout 0')

base = ModularBase(pipe = pipe)
base.initCR()


x, y = [SNAPSHOT_RES] * 2

# ensure we can actually see nametags when we wanna call for them
base.initNametagGlobals()

# base.resetGSG(updateFilters=False)

from modtools.extensions.toon_snapshot.snapshot.ToonSnapshot import ToonSnapshot
from modtools.extensions.toon_snapshot.snapshot.DoodleSnapshot import DoodleSnapshot
from modtools.extensions.toon_snapshot.snapshot.SuitSnapshot import SuitSnapshot

from modtools.extensions.toon_snapshot.snapshot.RenderEnums import *
from modtools.extensions.toon_snapshot.snapshot import SnapshotUtils


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
from toontown.makeatoon.NameGenerator import NameGenerator


###

import asyncio
import websockets


# create handler for each connection
async def handler(websocket, path):
    # just putting this in here for now:
    # cleanup old images (if applicable)
    SnapshotUtils.clean_old_files()

    data = await websocket.recv()
    data = json.loads(data)
    outputData = dict()
    if data.get("TEST"):
        outputData["response"] = "pong"
        await websocket.send(json.dumps(outputData))
        return

    # if data.get("QUERY"):
    #     outputData["response"] = NameGenerator
    #     await websocket.send(json.dumps(outputData))
    #     return

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

    # await asyncio.sleep(0.5)

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
            muzzleType = data.get("MUZZLE_TYPE"),
            randomAccessories = data.get("ACCESSORIES_RANDOM")
        )

    elif data.get("RENDER_TYPE") == RenderType.Doodle:
        dna = data.get("DNA_RANDOM")
        if not dna:
            dna = data.get("DNA_STRING")
        snapshot.loadDoodle(
            doodleName = data.get("NAME"),
            customPhrase = data.get("CUSTOM_PHRASE"),
            wantNametag = data.get("WANT_NAMETAG"),
            chatBubbleType = bubbleType,
            dna = dna,
            expressionID = data.get("POSE_PRESET")
        )
    elif data.get("RENDER_TYPE") == RenderType.Suit:
        snapshot.loadSuit(
            # randomDNA = data.get("DNA_RANDOM"),
            haphazardDNA = data.get("DNA_HAPHAZARD"),
            headDNA = data.get("DNA_STRING"),
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
    name, anim, frame = snapshot.getInfo()
    snapshot.cleanup()
    reply = snapshot.filename
    outputData["RENDER_IMAGE"] = snapshot.filename
    outputData["ACTOR_NAME"] = name
    outputData["ACTOR_ANIM_NAME"] = anim
    outputData["ACTOR_ANIM_FRAME"] = frame

    if SNAPSHOT_TRIM_WHITESPACE:
        await crop_images(reply)
        # Todo: Make trim whitespace script instead of depending on imagemagick
        # hack bc i dont feel like setting up the magickwand library right now on windows
        # https://docs.wand-py.org/en/latest/guide/install.html#install-imagemagick-on-windows
        # if os.name != 'nt':
        #     SnapshotUtils.trim_whitespace(snapshot.filename)
        # else:
        #     imgMagickPath = os.environ.get("IMAGEMAGICK_PATH") + "\\" if os.environ.get("IMAGEMAGICK_PATH") else ""
        #     subprocess.call([f"{imgMagickPath}convert.exe", reply, '-trim', reply])
    await websocket.send(json.dumps(outputData))


start_server = websockets.serve(handler, str(SNAPSHOT_HOST), SNAPSHOT_PORT)

asyncio.get_event_loop().run_until_complete(start_server)

asyncio.get_event_loop().run_forever()
