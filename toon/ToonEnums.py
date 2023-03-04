from enum import IntEnum


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


class AccessoryType(IntEnum):
    Hat = 1
    Glasses = 2
    Backpack = 3
    Shoes = 4
