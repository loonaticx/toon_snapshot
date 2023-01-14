"""
A mini Context object for storing and retrieving a User's requested DNA
"""
from modtools.extensions.toon_snapshot.pets.PetEnums import *


class PetDNAContext(object):
    disid = 0  # discord id

    # session-based values
    _PET_GENDER: PetGender = PetGender.Random
    _HEAD_TYPE: HeadType = HeadType.Empty
    _EAR_TYPE: EarType = EarType.Empty
    _NOSE_TYPE: NoseType = NoseType.Empty
    _TAIL_TYPE: TailType = TailType.Empty
    # _BODY_TYPE: GenericBodyType | SpecificBodyType = 0
    _BODY_TYPE: GenericBodyType = 0
    _COLOR = 0
    _COLOR_SCALE = 0
    _EYES = 0

    def getDNA(self):
        """
        :return: [head, ears, nose, tail, body, color, colorScale, eyes, gender]
        """
        return [
            self._HEAD_TYPE, self._EAR_TYPE, self._NOSE_TYPE,
            self._TAIL_TYPE, self._BODY_TYPE, self._COLOR,
            self._COLOR_SCALE, self._EYES, self._PET_GENDER
        ]

    @property
    def PET_GENDER(self):
        return self._PET_GENDER

    @PET_GENDER.setter
    def PET_GENDER(self, id: IntEnum):
        self._PET_GENDER = id

    @property
    def EAR_TYPE(self):
        return self._EAR_TYPE

    @EAR_TYPE.setter
    def EAR_TYPE(self, id: IntEnum):
        self._EAR_TYPE = id

    @property
    def NOSE_TYPE(self):
        return self._NOSE_TYPE

    @EAR_TYPE.setter
    def NOSE_TYPE(self, id: IntEnum):
        self._NOSE_TYPE = id

    @property
    def TAIL_TYPE(self):
        return self._TAIL_TYPE

    @TAIL_TYPE.setter
    def TAIL_TYPE(self, id: IntEnum):
        self._TAIL_TYPE = id

    @property
    def BODY_TYPE(self):
        return self._BODY_TYPE

    @BODY_TYPE.setter
    def BODY_TYPE(self, id: IntEnum):
        self._BODY_TYPE = id

    @property
    def COLOR(self):
        return self._COLOR

    @COLOR.setter
    def COLOR(self, id: IntEnum):
        self._COLOR = id
