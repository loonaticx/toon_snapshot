from enum import IntEnum


class DNAFields(IntEnum):
    Head = 0
    Ears = 1
    Nose = 2
    Tail = 3
    Body = 4
    Color = 5
    ColorScale = 6
    Eyes = 7
    Gender = 8


class PetGender(IntEnum):
    Female = 0
    Male = 1
    Random = 2


class HeadType(IntEnum):
    Empty = -1
    Feathers = 0


class EarType(IntEnum):
    Empty = -1
    Horns = 0
    Antennae = 1
    Dog = 2
    Cat = 3
    Bunny = 4


class NoseType(IntEnum):
    Empty = -1
    Clown = 0
    Dog = 1
    Oval = 2
    Pig = 3


class TailType(IntEnum):
    Empty = -1
    Cat = 0
    Long = 1
    Bird = 2
    Bunny = 3


class GenericBodyType(IntEnum):
    """
    these are generic critters and can have any color
    """
    Dots = 0
    ThreeStripe = 1
    TigerStripe = 2
    Tummy = 3


class SpecificBodyType(IntEnum):
    """
    these are specific animals and have a restricted color palette
    """
    Turtle = 0
    Giraffe = 1
    Leopard = 2
