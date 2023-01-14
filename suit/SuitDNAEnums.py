from enum import IntEnum


class SuitDepartment(IntEnum):
    """
    WRT constants defined in SuitDNA
    """
    Bossbot = 0
    Lawbot = 1
    Cashbot = 2
    Sellbot = 4


class SuitDNADefinitions(IntEnum):
    SUIT_DEPT: int = 0
    SUIT_BODY: int = 1
    SUIT_SCALE: int = 2
    SUIT_BODY_TEXTURES: int = 3
    SUIT_HAND_COLOR: int = 4
    SUIT_HEAD_COLOR: int = 5
    SUIT_HEAD_TEXTURE: int = 6
    SUIT_HEAD: int = 7
    SUIT_HEIGHT: int = 8
    SUIT_ANIM_EXCEPTIONS: int = 9
    SUIT_BATTLE_INFO: int = 10


class SuitHeadAttribute(IntEnum):
    HEAD_TEXTURES: int = 0
    HEAD_COLORS: int = 1
    HEAD_SIZE: int = 2
