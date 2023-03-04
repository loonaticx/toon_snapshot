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
        # this is a placeholder value; at the end of the day, DNA_string will dictate if random dna.
        "DNA_RANDOM": True,  # this is useless for toons
        "DNA_HAPHAZARD": False,  # Special cases like the Suits
        "SPEEDCHAT_PHRASE": None,  # speedchat phrase id if not None
        "POSE_PRESET": None,  # context specific, None -> random
        "DNA_STRING": None,  # generate random dna if None, might be a literal dna (list; not netstring)

        # /toon and /npc
        # Note: these are overrides
        "EYE_TYPE": None,
        "MUZZLE_TYPE": None,

        # /npc
        "NPC_ID": None,  # none -> random

    }

    def __init__(self):
        pass
