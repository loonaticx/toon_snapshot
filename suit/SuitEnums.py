from enum import IntEnum, Enum
from strenum import StrEnum

from panda3d.core import VBase4

from modtools.extensions.toon_snapshot import OP_DIR


class SuitDNAType(IntEnum):
    Random = 0
    Haphazard = 1
    # Normal = 2


class SuitDepartmentID(IntEnum):
    """
    WRT constants defined in SuitDNA
    """
    Bossbot = 0
    Lawbot = 1
    Cashbot = 2
    Sellbot = 3


class SuitDepartment(StrEnum):
    Bossbot = 'c'
    Lawbot = 'l'
    Cashbot = 'm'
    Sellbot = 's'


class SpecialSuitDepartmentID(IntEnum):
    Statue = 4


class SpecialSuitDepartment(StrEnum):
    """
    These aren't all necessarily registered as official departments,
    more so to differentiate the suit blazers that can be chosen.
    """
    Statue = 'statue'
    Sales = 'sales'
    Waiter = 'waiter_m'
    Clown = 'clown'



class SuitBodyType(StrEnum):
    SuitA = 'a',
    SuitB = 'b',
    SuitC = 'c'

class SuitHeadColor(Enum):
    ColdCaller = VBase4(0.25, 0.35, 1.0, 1.0)

class SuitHandColor(Enum):
    Default = VBase4(1.0, 1.0, 1.0, 1.0)
    Bossbot = VBase4(0.95, 0.75, 0.75, 1.0)
    Lawbot = VBase4(0.75, 0.75, 0.95, 1.0)
    Cashbot = VBase4(0.65, 0.95, 0.85, 1.0)
    Sellbot = VBase4(0.95, 0.75, 0.95, 1.0)

class SuitHandTexture(StrEnum):
    StatueWhite = f"img/textures/statue_hand_1.png"
    StatueBlue = f"img/textures/statue_hand_feeder.png"


class SuitDNADefinitions(IntEnum):
    SUIT_DEPT_INDEX: int = 0
    # SUIT_DEPT = SuitDepartment
    # SUIT_DEPT_ID = SuitDepartmentID
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
    SUIT_HAND_TEXTURE: int = 11



class SuitHeadAttribute(IntEnum):
    HEAD_TEXTURES: int = 0
    HEAD_COLORS: int = 1
    HEAD_SIZE: int = 2


class SuitName(StrEnum):
    # bossbots
    Flunky = 'f'
    PencilPusher = 'p'
    Yesman = 'ym'
    Micromanager = 'mm'
    Downsizer = 'ds'
    HeadHunter = 'hh'
    CorporateRaider = 'cr'
    TheBigCheese = 'tbc'

    # lawbots
    BottomFeeder = 'bf'
    Bloodsucker = 'b'
    DoubleTalker = 'dt'
    AmbulanceChaser = 'ac'
    BackStabber = 'bs'
    SpinDoctor = 'sd'
    LegalEagle = 'le'
    BigWig = 'bw'

    # special, but don't use
    StatueBottomFeeder = 'xx'


class SuitFullName(StrEnum):
    Flunky = 'flunky'
    PencilPusher = 'pencilpusher'
    Yesman = 'yesman'
    Micromanager = 'micromanager'
    Downsizer = 'beancounter'
    HeadHunter = 'headhunter'
    CorporateRaider = 'corporateraider'
    TheBigCheese = 'bigcheese'

    Tightwad = 'tightwad'

    StatueBottomFeeder = 'statue_bottom_feeder'


