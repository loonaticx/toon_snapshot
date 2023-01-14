"""
A mini Context object for storing and retrieving a User's requested DNA
"""
from modtools.extensions.toon_snapshot.suit.SuitEnums import *
from modtools.extensions.toon_snapshot.suit.SuitDNAEnums import *


class SuitDNAContext(object):
    _DEPT = SuitDepartment.Bossbot
