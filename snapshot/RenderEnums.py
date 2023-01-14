from enum import IntEnum


class ChatBubbleType(IntEnum):
    Random = 0
    Normal = 1  # CFSpeech
    Thought = 2  # CFThought


class ChatFlag(IntEnum):
    Timeout = 8  # CFTimeout, only here for accommodation


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


class LanguageType(IntEnum):
    Random = 0
    English = 1
    French = 2
    German = 3
    Japanese = 4
    Castillan = 5
    Portuguese = 6
