from enum import IntEnum


class ChatBubbleType(IntEnum):
    Random = 0
    Normal = 1  # CFSpeech
    Thought = 2  # CFThought


class ChatFlag(IntEnum):
    Timeout = 8  # CFTimeout, only here for accommodation


class EyeType(IntEnum):
    Random = 0
    NormalOpen = 1
    NormalClosed = 2
    AngryOpen = 3
    AngryClosed = 4
    SadOpen = 5
    SadClosed = 6
    ShockOpen = 7
    ShockClosed = 8


class MuzzleType(IntEnum):
    Random = 0
    Neutral = 1
    Angry = 2
    Laugh = 3
    Sad = 4
    Shock = 5
    Smile = 6


class FrameType(IntEnum):
    Random = 0
    Headshot = 1
    Bodyshot = 2
    TopToons = 3


class RenderType(IntEnum):
    Random = 0
    Toon = 1
    NPC = 2
    Doodle = 3
    Suit = 4


class SuitDNAType(IntEnum):
    Random = 0
    Haphazard = 1
    Normal = 2


