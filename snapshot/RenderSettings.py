from modtools.extensions.toon_snapshot.snapshot.RenderEnums import *

class RenderSettings:
    renderConfig = {
    # /render
    "RENDER_TYPE": RenderType.Random,
    "WANT_NAMETAG": True,
    "CHAT_BUBBLE_TYPE": ChatBubbleType.Normal,
    "CUSTOM_PHRASE": None,  # alt to speedchat phrase; not none = user gave input
    "FRAME_TYPE": FrameType.Random,

    # /render: context-specific
    "NAME": None,  # generate random if None
    "DNA_RANDOM": True,
    "DNA_HAPHAZARD": False,  # Special cases like the Suits
    "SPEEDCHAT_PHRASE": None,  # speedchat phrase id if not None
    "POSE_PRESET": None,  # context specific, None -> random
    "DNA_STRING": None,  # generate random dna if None, might be a literal dna (list; not netstring)

    # /toon and /npc
    "EYE_TYPE": EyeType.NormalOpen,
    "MUZZLE_TYPE": MuzzleType.Neutral,

    # /npc
    "NPC_ID": None,  # none -> random


}

    def __init__(self):
        pass