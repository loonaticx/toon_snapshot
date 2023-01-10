"""
SuitDNAExtended

Credit to Benjamin F. for a lot of the suit random generation code.
"""

import time

from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator

from toontown.suit import SuitDNA

import random
from panda3d.core import VBase4

from toontown.suit.SuitDNA import moneyPolyColor, legalPolyColor, corpPolyColor, salesPolyColor, suitDepts, \
    suitsPerDept, suitDeptFullnames, suitDeptFullnamesP, suitsPerLevel
from toontown.toonbase import TTLocalizer

from modtools.extensions.toon_snapshot.suit.SuitDNAEnums import *

dept2PolyColor = {'c': corpPolyColor, 'l': legalPolyColor, 'm': moneyPolyColor, 's': salesPolyColor}

Dept2Dept = {
    's': 'Sellbot',
    'm': 'Cashbot',
    'l': 'Lawbot',
    'c': 'Bossbot'
}
Dept2NameDept = {
    'Sellbot': 's',
    'Cashbot': 'm',
    'Lawbot': 'l',
    'Bossbot': 'c'
}
CogDepts = ['c', 'l', 'm', 's']

# Scale modifiers for different suit sizes
SuitScaleModifiers = {'a': 6.06, 'b': 5.29, 'c': 4.14}

# Suit definitions
SUIT_DEPT = SuitDNADefinitions.SUIT_DEPT
SUIT_BODY = SuitDNADefinitions.SUIT_BODY
SUIT_SCALE = SuitDNADefinitions.SUIT_SCALE
SUIT_BODY_TEXTURES = SuitDNADefinitions.SUIT_BODY_TEXTURES
SUIT_HAND_COLOR = SuitDNADefinitions.SUIT_HAND_COLOR
SUIT_HEAD_COLOR = SuitDNADefinitions.SUIT_HEAD_COLOR
SUIT_HEAD_TEXTURE = SuitDNADefinitions.SUIT_HEAD_TEXTURE
SUIT_HEAD = SuitDNADefinitions.SUIT_HEAD
SUIT_HEIGHT = SuitDNADefinitions.SUIT_HEIGHT
SUIT_ANIM_EXCEPTIONS = SuitDNADefinitions.SUIT_ANIM_EXCEPTIONS
SUIT_BATTLE_INFO = SuitDNADefinitions.SUIT_BATTLE_INFO

SUIT_LARGE = 1

# Slightly modified variant of SuitAttributes from SuitBattleGlobals
# Todo: remove attacks and acc entries since we don't need them for SuitSnapshot.
SuitPresets = {
    'f': ('c', 'c', 4.0, None, corpPolyColor, None, None, ('flunky', 'glasses'), 4.88, (1.0, True),
          {
              'name': TTLocalizer.SuitFlunky,
              'singularname': TTLocalizer.SuitFlunkyS,
              'pluralname': TTLocalizer.SuitFlunkyP,
              'level': 0,
              'acc': (35, 40, 45, 50, 55),
              'attacks': (('PoundKey', (2, 2, 3, 4, 6), (75, 75, 80, 80, 90), (30, 35, 40, 45, 50)),
                          ('Shred', (3, 4, 5, 6, 7), (50, 55, 60, 65, 70), (10, 15, 20, 25, 30)),
                          ('ClipOnTie', (1, 1, 2, 2, 3), (75, 80, 85, 90, 95), (60, 50, 40, 30, 20)))
          }),
    'p': ('c', 'b', 3.35, None, corpPolyColor, None, None, ('pencilpusher',), 5.0, (0.0, False),
          {
              'name': TTLocalizer.SuitPencilPusher,
              'singularname': TTLocalizer.SuitPencilPusherS,
              'pluralname': TTLocalizer.SuitPencilPusherP,
              'level': 1,
              'acc': (45, 50, 55, 60, 65),
              'attacks': (('FountainPen', (2, 3, 4, 6, 9), (75, 75, 75, 75, 75), (20, 20, 20, 20, 20)),
                          ('RubOut', (4, 5, 6, 8, 12), (75, 75, 75, 75, 75), (20, 20, 20, 20, 20)),
                          ('FingerWag', (1, 2, 2, 3, 4), (75, 75, 75, 75, 75), (35, 30, 25, 20, 15)),
                          ('WriteOff', (4, 6, 8, 10, 12), (75, 75, 75, 75, 75), (5, 10, 15, 20, 25)),
                          ('FillWithLead', (3, 4, 5, 6, 7), (75, 75, 75, 75, 75), (20, 20, 20, 20, 20)))
          }),
    'ym': ('c', 'a', 4.125, None, corpPolyColor, None, None, ('yesman',), 5.28, (0.1, False),
           {
               'name': TTLocalizer.SuitYesman,
               'singularname': TTLocalizer.SuitYesmanS,
               'pluralname': TTLocalizer.SuitYesmanP,
               'level': 2,
               'acc': (65, 70, 75, 80, 85),
               'attacks': (('RubberStamp', (2, 2, 3, 3, 4), (75, 75, 75, 75, 75), (35, 35, 35, 35, 35)),
                           ('RazzleDazzle', (1, 1, 1, 1, 1), (50, 50, 50, 50, 50), (25, 20, 15, 10, 5)),
                           ('Synergy', (4, 5, 6, 7, 8), (50, 60, 70, 80, 90), (5, 10, 15, 20, 25)),
                           ('TeeOff', (3, 3, 4, 4, 5), (50, 60, 70, 80, 90), (35, 35, 35, 35, 35)))
           }),
    'mm': ('c', 'c', 2.5, None, corpPolyColor, None, None, ('micromanager',), 3.25, (0.05, False),
           {
               'name': TTLocalizer.SuitMicromanager,
               'singularname': TTLocalizer.SuitMicromanagerS,
               'pluralname': TTLocalizer.SuitMicromanagerP,
               'level': 3,
               'acc': (70, 75, 80, 82, 85),
               'attacks': (('Demotion', (6, 8, 12, 15, 18), (50, 60, 70, 80, 90), (30, 30, 30, 30, 30)),
                           ('FingerWag', (4, 6, 9, 12, 15), (50, 60, 70, 80, 90), (10, 10, 10, 10, 10)),
                           ('FountainPen', (3, 4, 6, 8, 10), (50, 60, 70, 80, 90), (15, 15, 15, 15, 15)),
                           ('BrainStorm', (4, 6, 9, 12, 15), (5, 5, 5, 5, 5), (25, 25, 25, 25, 25)),
                           ('BuzzWord', (4, 6, 9, 12, 15), (50, 60, 70, 80, 90), (20, 20, 20, 20, 20)))
           }),
    'ds': ('c', 'b', 4.5, None, corpPolyColor, None, None, ('beancounter',), 6.08, (0.41, True),
           {
               'name': TTLocalizer.SuitDownsizer,
               'singularname': TTLocalizer.SuitDownsizerS,
               'pluralname': TTLocalizer.SuitDownsizerP,
               'level': 4,
               'acc': (35, 40, 45, 50, 55),
               'attacks': (('Canned', (5, 6, 8, 10, 12), (60, 75, 80, 85, 90), (25, 25, 25, 25, 25)),
                           ('Downsize', (8, 9, 11, 13, 15), (50, 65, 70, 75, 80), (35, 35, 35, 35, 35)),
                           ('PinkSlip', (4, 5, 6, 7, 8), (60, 65, 75, 80, 85), (25, 25, 25, 25, 25)),
                           ('Sacked', (5, 6, 7, 8, 9), (50, 50, 50, 50, 50), (15, 15, 15, 15, 15)))
           }),
    'hh': ('c', 'a', 6.5, None, corpPolyColor, None, None, ('headhunter',), 7.45, (0.8, True),
           {
               'name': TTLocalizer.SuitHeadHunter,
               'singularname': TTLocalizer.SuitHeadHunterS,
               'pluralname': TTLocalizer.SuitHeadHunterP,
               'level': 5,
               'acc': (35, 40, 45, 50, 55),
               'attacks': (('FountainPen', (5, 6, 8, 10, 12), (60, 75, 80, 85, 90), (15, 15, 15, 15, 15)),
                           ('GlowerPower', (7, 8, 10, 12, 13), (50, 60, 70, 80, 90), (20, 20, 20, 20, 20)),
                           ('HalfWindsor', (8, 10, 12, 14, 16), (60, 65, 70, 75, 80), (20, 20, 20, 20, 20)),
                           ('HeadShrink', (10, 12, 15, 18, 21), (65, 75, 80, 85, 95), (35, 35, 35, 35, 35)),
                           ('Rolodex', (6, 7, 8, 9, 10), (60, 65, 70, 75, 80), (10, 10, 10, 10, 10)))
           }),
    'cr': (
        'c', 'c', 6.75, None, VBase4(0.85, 0.55, 0.55, 1.0), None, 'corporate-raider.png', ('flunky',), 8.23,
        (2.1, True),
        {
            'name': TTLocalizer.SuitCorporateRaider,
            'singularname': TTLocalizer.SuitCorporateRaiderS,
            'pluralname': TTLocalizer.SuitCorporateRaiderP,
            'level': 6,
            'acc': (35, 40, 45, 50, 55),
            'attacks': (('Canned', (6, 7, 8, 9, 10), (60, 75, 80, 85, 90), (20, 20, 20, 20, 20)),
                        ('EvilEye', (12, 15, 18, 21, 24), (60, 70, 75, 80, 90), (35, 35, 35, 35, 35)),
                        ('PlayHardball', (7, 8, 12, 15, 16), (60, 65, 70, 75, 80), (30, 30, 30, 30, 30)),
                        ('PowerTie', (10, 12, 14, 16, 18), (65, 75, 80, 85, 95), (15, 15, 15, 15, 15)))
        }),
    'tbc': ('c', 'a', 7.0, None, VBase4(0.75, 0.95, 0.75, 1.0), None, None, ('bigcheese',), 9.34, (1.4, True),
            {
                'name': TTLocalizer.SuitTheBigCheese,
                'singularname': TTLocalizer.SuitTheBigCheeseS,
                'pluralname': TTLocalizer.SuitTheBigCheeseP,
                'level': 7,
                'acc': (35, 40, 45, 50, 55, 60, 65, 70, 70),
                'attacks': (('CigarSmoke', (10, 12, 15, 18, 20, 22, 23, 24, 25), (55, 65, 75, 85, 95, 95, 95, 95, 95),
                             (20, 20, 20, 20, 20, 20, 20, 20, 20)),
                            ('FloodTheMarket', (14, 16, 18, 20, 22, 23, 23, 24, 24),
                             (70, 75, 85, 90, 95, 95, 95, 95, 95), (10, 10, 10, 10, 10, 10, 10, 10, 10)),
                            ('SongAndDance', (14, 15, 17, 19, 20, 21, 22, 23, 24), (60, 65, 70, 75, 80, 85, 90, 90, 90),
                             (20, 20, 20, 20, 20, 20, 20, 20, 20)),
                            ('TeeOff', (8, 11, 14, 17, 20, 21, 21, 22, 22), (55, 65, 70, 75, 80, 85, 90, 90, 90),
                             (50, 50, 50, 50, 50, 50, 50, 50, 50)))
            }),

    'bf': ('l', 'c', 4.0, None, legalPolyColor, None, 'bottom-feeder.png', ('tightwad',), 4.81, (1.0, True),
           {
               'name': TTLocalizer.SuitBottomFeeder,
               'singularname': TTLocalizer.SuitBottomFeederS,
               'pluralname': TTLocalizer.SuitBottomFeederP,
               'level': 0,
               'acc': (35, 40, 45, 50, 55),
               'attacks': (('RubberStamp', (2, 3, 4, 5, 6), (75, 80, 85, 90, 95), (20, 20, 20, 20, 20)),
                           ('Shred', (2, 4, 6, 8, 10), (50, 55, 60, 65, 70), (20, 20, 20, 20, 20)),
                           ('Watercooler', (3, 4, 5, 6, 7), (95, 95, 95, 95, 95), (10, 10, 10, 10, 10)),
                           ('PickPocket', (1, 1, 2, 2, 3), (25, 30, 35, 40, 45), (50, 50, 50, 50, 50)))
           }),
    'b': ('l', 'b', 4.375, None, VBase4(0.95, 0.95, 1.0, 1.0), None, 'blood-sucker.png', ('movershaker',), 6.17,
          (0.41, False),
          {
              'name': TTLocalizer.SuitBloodsucker,
              'singularname': TTLocalizer.SuitBloodsuckerS,
              'pluralname': TTLocalizer.SuitBloodsuckerP,
              'level': 1,
              'acc': (45, 50, 55, 60, 65),
              'attacks': (('EvictionNotice', (1, 2, 3, 3, 4), (75, 75, 75, 75, 75), (20, 20, 20, 20, 20)),
                          ('RedTape', (2, 3, 4, 6, 9), (75, 75, 75, 75, 75), (20, 20, 20, 20, 20)),
                          ('Withdrawal', (6, 8, 10, 12, 14), (95, 95, 95, 95, 95), (10, 10, 10, 10, 10)),
                          ('Liquidate', (2, 3, 4, 6, 9), (50, 60, 70, 80, 90), (50, 50, 50, 50, 50)))
          }),
    'dt': ('l', 'a', 4.25, None, legalPolyColor, None, 'double-talker.png', ('twoface',), 5.63, (0.31, False),
           {
               'name': TTLocalizer.SuitDoubleTalker,
               'singularname': TTLocalizer.SuitDoubleTalkerS,
               'pluralname': TTLocalizer.SuitDoubleTalkerP,
               'level': 2,
               'acc': (65, 70, 75, 80, 85),
               'attacks': (('RubberStamp', (1, 1, 1, 1, 1), (50, 60, 70, 80, 90), (5, 5, 5, 5, 5)),
                           ('BounceCheck', (1, 1, 1, 1, 1), (50, 60, 70, 80, 90), (5, 5, 5, 5, 5)),
                           ('BuzzWord', (1, 2, 3, 5, 6), (50, 60, 70, 80, 90), (20, 20, 20, 20, 20)),
                           ('DoubleTalk', (6, 6, 9, 13, 18), (50, 60, 70, 80, 90), (25, 25, 25, 25, 25)),
                           ('Jargon', (3, 4, 6, 9, 12), (50, 60, 70, 80, 90), (25, 25, 25, 25, 25)),
                           ('MumboJumbo', (3, 4, 6, 9, 12), (50, 60, 70, 80, 90), (20, 20, 20, 20, 20)))
           }),
    'ac': ('l', 'b', 4.35, None, legalPolyColor, None, None, ('ambulancechaser',), 6.39, (0.39, False),
           {
               'name': TTLocalizer.SuitAmbulanceChaser,
               'singularname': TTLocalizer.SuitAmbulanceChaserS,
               'pluralname': TTLocalizer.SuitAmbulanceChaserP,
               'level': 3,
               'acc': (65, 70, 75, 80, 85),
               'attacks': (('Shake', (4, 6, 9, 12, 15), (75, 75, 75, 75, 75), (15, 15, 15, 15, 15)),
                           ('RedTape', (6, 8, 12, 15, 19), (75, 75, 75, 75, 75), (30, 30, 30, 30, 30)),
                           ('Rolodex', (3, 4, 5, 6, 7), (75, 75, 75, 75, 75), (20, 20, 20, 20, 20)),
                           ('HangUp', (2, 3, 4, 5, 6), (75, 75, 75, 75, 75), (35, 35, 35, 35, 35)))
           }),
    'bs': ('l', 'a', 4.5, None, legalPolyColor, None, None, ('backstabber',), 6.71, (0.4, True),
           {
               'name': TTLocalizer.SuitBackStabber,
               'singularname': TTLocalizer.SuitBackStabberS,
               'pluralname': TTLocalizer.SuitBackStabberP,
               'level': 4,
               'acc': (35, 40, 45, 50, 55),
               'attacks': (('GuiltTrip', (8, 11, 13, 15, 18), (60, 75, 80, 85, 90), (40, 40, 40, 40, 40)),
                           ('RestrainingOrder', (6, 7, 9, 11, 13), (50, 65, 70, 75, 90), (25, 25, 25, 25, 25)),
                           ('FingerWag', (5, 6, 7, 8, 9), (50, 55, 65, 75, 80), (35, 35, 35, 35, 35)))
           }),
    'sd': (
        'l', 'b', 5.65, None, VBase4(0.5, 0.8, 0.75, 1.0), None, 'spin-doctor.png', ('telemarketer',), 7.9,
        (1.02, True),
        {
            'name': TTLocalizer.SuitSpinDoctor,
            'singularname': TTLocalizer.SuitSpinDoctorS,
            'pluralname': TTLocalizer.SuitSpinDoctorP,
            'level': 5,
            'acc': (35, 40, 45, 50, 55),
            'attacks': (('ParadigmShift', (9, 10, 13, 16, 17), (60, 75, 80, 85, 90), (30, 30, 30, 30, 30)),
                        ('Quake', (8, 10, 12, 14, 16), (60, 65, 70, 75, 80), (20, 20, 20, 20, 20)),
                        ('Spin', (10, 12, 15, 18, 20), (70, 75, 80, 85, 90), (35, 35, 35, 35, 35)),
                        ('WriteOff', (6, 7, 8, 9, 10), (60, 65, 75, 85, 90), (15, 15, 15, 15, 15)))
        }),
    'le': ('l', 'a', 7.125, None, VBase4(0.25, 0.25, 0.5, 1.0), None, None, ('legaleagle',), 8.27, (1.3, True),
           {
               'name': TTLocalizer.SuitLegalEagle,
               'singularname': TTLocalizer.SuitLegalEagleS,
               'pluralname': TTLocalizer.SuitLegalEagleP,
               'level': 6,
               'acc': (35, 40, 45, 50, 55),
               'attacks': (('EvilEye', (10, 11, 13, 15, 16), (60, 75, 80, 85, 90), (20, 20, 20, 20, 20)),
                           ('Jargon', (7, 9, 11, 13, 15), (60, 70, 75, 80, 90), (15, 15, 15, 15, 15)),
                           ('Legalese', (11, 13, 16, 19, 21), (55, 65, 75, 85, 95), (35, 35, 35, 35, 35)),
                           ('PeckingOrder', (12, 15, 17, 19, 22), (70, 75, 80, 85, 95), (30, 30, 30, 30, 30)))
           }),
    'bw': ('l', 'a', 7.0, None, legalPolyColor, None, None, ('bigwig',), 8.69, (1.4, True),
           {
               'name': TTLocalizer.SuitBigWig,
               'singularname': TTLocalizer.SuitBigWigS,
               'pluralname': TTLocalizer.SuitBigWigP,
               'level': 7,
               'acc': (35, 40, 45, 50, 55, 60, 65, 70, 70),
               'attacks': (('PowerTrip', (10, 11, 13, 15, 16, 18, 20, 21, 23), (75, 80, 85, 90, 95, 95, 95, 95, 95),
                            (50, 50, 50, 50, 50, 50, 50, 50, 50)),
                           ('ThrowBook', (13, 15, 17, 19, 21, 23, 25, 27, 29), (80, 85, 85, 85, 90, 90, 90, 90, 95),
                            (50, 50, 50, 50, 50, 50, 50, 50, 50)))
           }),

    'sc': ('m', 'c', 3.6, None, moneyPolyColor, None, None, ('coldcaller',), 4.77, (0.8, True),
           {
               'name': TTLocalizer.SuitShortChange,
               'singularname': TTLocalizer.SuitShortChangeS,
               'pluralname': TTLocalizer.SuitShortChangeP,
               'level': 0,
               'acc': (35, 40, 45, 50, 55),
               'attacks': (('Watercooler', (2, 2, 3, 4, 6), (50, 50, 50, 50, 50), (20, 20, 20, 20, 20)),
                           ('BounceCheck', (3, 5, 7, 9, 11), (75, 80, 85, 90, 95), (15, 15, 15, 15, 15)),
                           ('ClipOnTie', (1, 1, 2, 2, 3), (50, 50, 50, 50, 50), (25, 25, 25, 25, 25)),
                           ('PickPocket', (2, 2, 3, 4, 6), (95, 95, 95, 95, 95), (40, 40, 40, 40, 40)))
           }),
    'pp': ('m', 'a', 3.55, None, VBase4(1.0, 0.5, 0.6, 1.0), None, None, ('pennypincher',), 5.26, (0.04, False),
           {
               'name': TTLocalizer.SuitPennyPincher,
               'singularname': TTLocalizer.SuitPennyPincherS,
               'pluralname': TTLocalizer.SuitPennyPincherP,
               'level': 1,
               'acc': (45, 50, 55, 60, 65),
               'attacks': (('BounceCheck', (4, 5, 6, 8, 12), (75, 75, 75, 75, 75), (45, 45, 45, 45, 45)),
                           ('FreezeAssets', (2, 3, 4, 6, 9), (75, 75, 75, 75, 75), (20, 20, 20, 20, 20)),
                           ('FingerWag', (1, 2, 3, 4, 6), (50, 50, 50, 50, 50), (35, 35, 35, 35, 35)))
           }),
    'tw': ('m', 'c', 4.5, None, moneyPolyColor, None, None, ('tightwad',), 5.41, (1.3, False),
           {
               'name': TTLocalizer.SuitTightwad,
               'singularname': TTLocalizer.SuitTightwadS,
               'pluralname': TTLocalizer.SuitTightwadP,
               'level': 2,
               'acc': (65, 70, 75, 80, 85),
               'attacks': (('Fired', (3, 4, 5, 5, 6), (75, 75, 75, 75, 75), (75, 5, 5, 5, 5)),
                           ('GlowerPower', (3, 4, 6, 9, 12), (95, 95, 95, 95, 95), (10, 15, 20, 25, 30)),
                           ('FingerWag', (3, 3, 4, 4, 5), (75, 75, 75, 75, 75), (5, 70, 5, 5, 5)),
                           ('FreezeAssets', (3, 4, 6, 9, 12), (75, 75, 75, 75, 75), (5, 5, 65, 5, 30)),
                           ('BounceCheck', (5, 6, 9, 13, 18), (75, 75, 75, 75, 75), (5, 5, 5, 60, 30)))
           }),
    'bc': ('m', 'b', 4.4, None, moneyPolyColor, None, None, ('beancounter',), 5.95, (0.36, False),
           {
               'name': TTLocalizer.SuitBeanCounter,
               'singularname': TTLocalizer.SuitBeanCounterS,
               'pluralname': TTLocalizer.SuitBeanCounterP,
               'level': 3,
               'acc': (70, 75, 80, 82, 85),
               'attacks': (('Audit', (4, 6, 9, 12, 15), (95, 95, 95, 95, 95), (20, 20, 20, 20, 20)),
                           ('Calculate', (4, 6, 9, 12, 15), (75, 75, 75, 75, 75), (25, 25, 25, 25, 25)),
                           ('Tabulate', (4, 6, 9, 12, 15), (75, 75, 75, 75, 75), (25, 25, 25, 25, 25)),
                           ('WriteOff', (4, 6, 9, 12, 15), (95, 95, 95, 95, 95), (30, 30, 30, 30, 30)))
           }),
    'nc': ('m', 'a', 5.25, None, moneyPolyColor, None, None, ('numbercruncher',), 7.22, (0.6, True),
           {
               'name': TTLocalizer.SuitNumberCruncher,
               'singularname': TTLocalizer.SuitNumberCruncherS,
               'pluralname': TTLocalizer.SuitNumberCruncherP,
               'level': 4,
               'acc': (35, 40, 45, 50, 55),
               'attacks': (('Audit', (5, 6, 8, 10, 12), (60, 75, 80, 85, 90), (15, 15, 15, 15, 15)),
                           ('Calculate', (6, 7, 9, 11, 13), (50, 65, 70, 75, 80), (30, 30, 30, 30, 30)),
                           ('Crunch', (8, 9, 11, 13, 15), (60, 65, 75, 80, 85), (35, 35, 35, 35, 35)),
                           ('Tabulate', (5, 6, 7, 8, 9), (50, 50, 50, 50, 50), (20, 20, 20, 20, 20)))
           }),
    'mb': ('m', 'c', 5.3, None, moneyPolyColor, None, None, ('moneybags',), 6.97, (1.85, True),
           {
               'name': TTLocalizer.SuitMoneyBags,
               'singularname': TTLocalizer.SuitMoneyBagsS,
               'pluralname': TTLocalizer.SuitMoneyBagsP,
               'level': 5,
               'acc': (35, 40, 45, 50, 55),
               'attacks': (('Liquidate', (10, 12, 14, 16, 18), (60, 75, 80, 85, 90), (30, 30, 30, 30, 30)),
                           ('MarketCrash', (8, 10, 12, 14, 16), (60, 65, 70, 75, 80), (45, 45, 45, 45, 45)),
                           ('PowerTie', (6, 7, 8, 9, 10), (60, 65, 75, 85, 90), (25, 25, 25, 25, 25)))
           }),
    'ls': ('m', 'b', 6.5, None, VBase4(0.5, 0.85, 0.75, 1.0), None, None, ('loanshark',), 8.58, (1.4, True),
           {
               'name': TTLocalizer.SuitLoanShark,
               'singularname': TTLocalizer.SuitLoanSharkS,
               'pluralname': TTLocalizer.SuitLoanSharkP,
               'level': 6,
               'acc': (35, 40, 45, 50, 55),
               'attacks': (('Bite', (10, 11, 13, 15, 16), (60, 75, 80, 85, 90), (30, 30, 30, 30, 30)),
                           ('Chomp', (12, 15, 18, 21, 24), (60, 70, 75, 80, 90), (35, 35, 35, 35, 35)),
                           ('PlayHardball', (9, 11, 12, 13, 15), (55, 65, 75, 85, 95), (20, 20, 20, 20, 20)),
                           ('WriteOff', (6, 8, 10, 12, 14), (70, 75, 80, 85, 95), (15, 15, 15, 15, 15)))
           }),
    'rb': ('m', 'a', 7.0, None, moneyPolyColor, None, 'robber-baron.png', ('yesman',), 8.95, (1.6, True),
           {
               'name': TTLocalizer.SuitRobberBaron,
               'singularname': TTLocalizer.SuitRobberBaronS,
               'pluralname': TTLocalizer.SuitRobberBaronP,
               'level': 7,
               'acc': (35, 40, 45, 50, 55, 60, 65, 70, 70),
               'attacks': (('PowerTrip', (11, 14, 16, 18, 21, 22, 23, 24, 25), (60, 65, 70, 75, 80, 80, 80, 85, 90),
                            (50, 50, 50, 50, 50, 50, 50, 50, 50)),
                           ('TeeOff', (10, 12, 14, 16, 18, 20, 22, 24, 26), (60, 65, 75, 85, 90, 90, 90, 90, 95),
                            (50, 50, 50, 50, 50, 50, 50, 50, 50)))
           }),

    'cc': ('s', 'c', 3.5, None, VBase4(0.55, 0.65, 1.0, 1.0), VBase4(0.25, 0.35, 1.0, 1.0), None, ('coldcaller',), 4.63,
           (0.7, True),
           {
               'name': TTLocalizer.SuitColdCaller,
               'singularname': TTLocalizer.SuitColdCallerS,
               'pluralname': TTLocalizer.SuitColdCallerP,
               'level': 0,
               'acc': (35, 40, 45, 50, 55),
               'attacks': (('FreezeAssets', (1, 1, 1, 1, 1), (90, 90, 90, 90, 90), (5, 10, 15, 20, 25)),
                           ('PoundKey', (2, 2, 3, 4, 5), (75, 80, 85, 90, 95), (25, 25, 25, 25, 25)),
                           ('DoubleTalk', (2, 3, 4, 6, 8), (50, 55, 60, 65, 70), (25, 25, 25, 25, 25)),
                           ('HotAir', (3, 4, 6, 8, 10), (50, 50, 50, 50, 50), (45, 40, 35, 30, 25)))
           }),
    'tm': ('s', 'b', 3.75, None, salesPolyColor, None, None, ('telemarketer',), 5.24, (0.07, False),
           {
               'name': TTLocalizer.SuitTelemarketer,
               'singularname': TTLocalizer.SuitTelemarketerS,
               'pluralname': TTLocalizer.SuitTelemarketerP,
               'level': 1,
               'acc': (45, 50, 55, 60, 65),
               'attacks': (('ClipOnTie', (2, 2, 3, 3, 4), (75, 75, 75, 75, 75), (15, 15, 15, 15, 15)),
                           ('PickPocket', (1, 1, 1, 1, 1), (75, 75, 75, 75, 75), (15, 15, 15, 15, 15)),
                           ('Rolodex', (4, 6, 7, 9, 12), (50, 50, 50, 50, 50), (30, 30, 30, 30, 30)),
                           ('DoubleTalk', (4, 6, 7, 9, 12), (75, 80, 85, 90, 95), (40, 40, 40, 40, 40)))
           }),
    'nd': ('s', 'a', 4.35, None, salesPolyColor, None, 'name-dropper.png', ('numbercruncher',), 5.98, (0.07, False),
           {
               'name': TTLocalizer.SuitNameDropper,
               'singularname': TTLocalizer.SuitNameDropperS,
               'pluralname': TTLocalizer.SuitNameDropperP,
               'level': 2,
               'acc': (65, 70, 75, 80, 85),
               'attacks': (('RazzleDazzle', (4, 5, 6, 9, 12), (75, 80, 85, 90, 95), (30, 30, 30, 30, 30)),
                           ('Rolodex', (5, 6, 7, 10, 14), (95, 95, 95, 95, 95), (40, 40, 40, 40, 40)),
                           ('Synergy', (3, 4, 6, 9, 12), (50, 50, 50, 50, 50), (15, 15, 15, 15, 15)),
                           ('PickPocket', (2, 2, 2, 2, 2), (95, 95, 95, 95, 95), (15, 15, 15, 15, 15)))
           }),
    'gh': ('s', 'c', 4.75, None, salesPolyColor, None, None, ('gladhander',), 5.98, (1.4, True),
           {
               'name': TTLocalizer.SuitGladHander,
               'singularname': TTLocalizer.SuitGladHanderS,
               'pluralname': TTLocalizer.SuitGladHanderP,
               'level': 3,
               'acc': (70, 75, 80, 82, 85),
               'attacks': (('RubberStamp', (4, 3, 3, 2, 1), (90, 70, 50, 30, 10), (40, 30, 20, 10, 5)),
                           ('FountainPen', (3, 3, 2, 1, 1), (70, 60, 50, 40, 30), (40, 30, 20, 10, 5)),
                           ('Filibuster', (4, 6, 9, 12, 15), (30, 40, 50, 60, 70), (10, 20, 30, 40, 45)),
                           ('Schmooze', (5, 7, 11, 15, 20), (55, 65, 75, 85, 95), (10, 20, 30, 40, 45)))
           }),
    'ms': ('s', 'b', 4.75, None, salesPolyColor, None, None, ('movershaker',), 6.7, (0.7, True),
           {
               'name': TTLocalizer.SuitMoverShaker,
               'singularname': TTLocalizer.SuitMoverShakerS,
               'pluralname': TTLocalizer.SuitMoverShakerP,
               'level': 4,
               'acc': (35, 40, 45, 50, 55),
               'attacks': (('BrainStorm', (5, 6, 8, 10, 12), (60, 75, 80, 85, 90), (15, 15, 15, 15, 15)),
                           ('HalfWindsor', (6, 9, 11, 13, 16), (50, 65, 70, 75, 80), (20, 20, 20, 20, 20)),
                           ('Quake', (9, 12, 15, 18, 21), (60, 65, 75, 80, 85), (20, 20, 20, 20, 20)),
                           ('Shake', (6, 8, 10, 12, 14), (70, 75, 80, 85, 90), (25, 25, 25, 25, 25)),
                           ('Tremor', (5, 6, 7, 8, 9), (50, 50, 50, 50, 50), (20, 20, 20, 20, 20)))
           }),
    'tf': ('s', 'a', 5.25, None, salesPolyColor, None, None, ('twoface',), 6.95, (0.75, True),
           {
               'name': TTLocalizer.SuitTwoFace,
               'singularname': TTLocalizer.SuitTwoFaceS,
               'pluralname': TTLocalizer.SuitTwoFaceP,
               'level': 5,
               'acc': (35, 40, 45, 50, 55),
               'attacks': (('EvilEye', (10, 12, 14, 16, 18), (60, 75, 80, 85, 90), (30, 30, 30, 30, 30)),
                           ('HangUp', (7, 8, 10, 12, 13), (50, 60, 70, 80, 90), (15, 15, 15, 15, 15)),
                           ('RazzleDazzle', (8, 10, 12, 14, 16), (60, 65, 70, 75, 80), (30, 30, 30, 30, 30)),
                           ('RedTape', (6, 7, 8, 9, 10), (60, 65, 75, 85, 90), (25, 25, 25, 25, 25)))
           }),
    'm': ('s', 'a', 5.75, None, salesPolyColor, None, 'mingler.png', ('twoface',), 7.61, (0.9, True),
          {
              'name': TTLocalizer.SuitTheMingler,
              'singularname': TTLocalizer.SuitTheMinglerS,
              'pluralname': TTLocalizer.SuitTheMinglerP,
              'level': 6,
              'acc': (35, 40, 45, 50, 55),
              'attacks': (('BuzzWord', (10, 11, 13, 15, 16), (60, 75, 80, 85, 90), (20, 20, 20, 20, 20)),
                          ('ParadigmShift', (12, 15, 18, 21, 24), (60, 70, 75, 80, 90), (25, 25, 25, 25, 25)),
                          ('PowerTrip', (10, 13, 14, 15, 18), (60, 65, 70, 75, 80), (15, 15, 15, 15, 15)),
                          ('Schmooze', (7, 8, 12, 15, 16), (55, 65, 75, 85, 95), (30, 30, 30, 30, 30)),
                          ('TeeOff', (8, 9, 10, 11, 12), (70, 75, 80, 85, 95), (10, 10, 10, 10, 10)))
          }),
    'mh': ('s', 'a', 7.0, None, salesPolyColor, None, None, ('yesman',), 8.95, (1.3, True),
           {
               'name': TTLocalizer.SuitMrHollywood,
               'singularname': TTLocalizer.SuitMrHollywoodS,
               'pluralname': TTLocalizer.SuitMrHollywoodP,
               'level': 7,
               'acc': (35, 40, 45, 50, 55, 60, 65, 70, 70),
               'attacks': (('PowerTrip', (10, 12, 15, 18, 20, 22, 24, 26, 28), (55, 65, 75, 85, 95, 95, 95, 95, 95),
                            (50, 50, 50, 50, 50, 50, 50, 50, 50)),
                           ('RazzleDazzle', (8, 11, 14, 17, 20, 22, 24, 26, 28), (70, 75, 85, 90, 95, 95, 95, 95, 95),
                            (50, 50, 50, 50, 50, 50, 50, 50, 50)))
           }),

}

HEAD_TEXTURES = 0
HEAD_COLORS = 1
HEAD_SIZE = 2

SuitHeadDict = {
    'flunky': (('corporate-raider', None), (None,), 'c'),
    'glasses': ((None,), (None,), 'c'),
    'pencilpusher': ((None,), (None,), 'b'),
    'yesman': (('robber-baron', None), (None,), 'a'),
    'micromanager': ((None,), (None,), 'c'),
    'beancounter': ((None,), (None,), 'b'),
    'headhunter': ((None,), (None,), 'a'),
    'bigcheese': ((None,), (None,), 'a'),
    'tightwad': (('bottom-feeder', None), (None,), 'c'),
    'movershaker': (('blood-sucker', None), (None,), 'b'),
    'twoface': (('double-talker', 'mingler', None), (None,), 'a'),
    'ambulancechaser': ((None,), (None,), 'b'),
    'backstabber': ((None,), (None,), 'a'),
    'telemarketer': (('spin-doctor', None), (None,), 'b'),
    'legaleagle': ((None,), (None,), 'a'),
    'bigwig': ((None,), (None,), 'a'),
    'coldcaller': ((None,), (VBase4(0.25, 0.35, 1.0, 1.0), None), 'c'),
    'pennypincher': ((None,), (None,), 'a'),
    'numbercruncher': (('name-dropper', None), (None,), 'a'),
    'moneybags': ((None,), (None,), 'c'),
    'loanshark': ((None,), (None,), 'b'),
    'gladhander': ((None,), (None,), 'c')
}

HeadModelDict = {
    'a': ('/models/char/suitA-', 4),
    'b': ('/models/char/suitB-', 4),
    'c': ('/models/char/suitC-', 3.5)
}

RandomSuitPrefixes = (
    "Flunky", "Pencil", "Yes", "Micro", "Down", "Head", "Corporate", "The Big", "Bottom", "Blood", "Double",
    "Ambulance", "Back", "Spin", "Legal", "Big", "Short", "Penny", "Tight", "Bean", "Number", "Money", "Loan", "Robber",
    "Cold", "Tele", "Name", "Glad", "Mover &", "Two", "The", "Mr."
)
RandomSuitSuffixes = (
    "Flunky", "Pusher", "Man", "Manager", "Sizer", "Hunter", "Raider", "Cheese", "Feeder", "Sucker", "Talker", "Chaser",
    "Stabber", "Doctor", "Eagle", "Wig", "Change", "Pincher", "Wad", "Counter", "Cruncher", "Bags", "Shark", "Baron",
    "Caller", "Marketer", "Dropper", "Hander", "Shaker", "Face", "Mingler", "Hollywood"
)

AttacksSuitA = (
    'RubberStamp',  # Yesman, Double Talker
    'RazzleDazzle',  # Yesman, Name Dropper, Two-Face, Mr. Hollywood
    'Synergy',  # Yesman, Name Dropper
    'TeeOff',  # Yesman, The Big Cheese, Robber Baron, The Mingler
    'FountainPen',  # Head Hunter
    'GlowerPower',  # Head Hunter
    'HalfWindsor',  # Head Hunter
    'HeadShrink',  # Head Hunter
    'Rolodex',  # Head Hunter, Name Dropper
    'CigarSmoke',  # The Big Cheese (Defaults to Glower Power)
    'FloodTheMarket',  # The Big Cheese (Defaults to Glower Power)
    'SongAndDance',  # The Big Cheese (Defaults to Glower Power)
    'BounceCheck',  # Double Talker, Penny Pincher
    'BuzzWord',  # Double Talker, The Mingler
    'DoubleTalk',  # Double Talker
    'Jargon',  # Double Talker, Legal Eagle
    'MumboJumbo',  # Double Talker
    'GuiltTrip',  # Back Stabber
    'RestrainingOrder',  # Back Stabber
    'FingerWag',  # Back Stabber, Penny Pincher
    'EvilEye',  # Legal Eagle
    'Legalese',  # Legal Eagle
    'PeckingOrder',  # Legal Eagle
    'PowerTrip',  # Big Wig, Robber Baron, The Mingler, Mr. Hollywood
    'ThrowBook',  # Big Wig (Defaults to Finger Wag)
    'FreezeAssets',  # Penny Pincher
    'Audit',  # Number Cruncher
    'Calculate',  # Number Cruncher
    'Crunch',  # Number Cruncher
    'Tabulate',  # Number Cruncher
    'PickPocket',  # Name Dropper
    'EvilEye',  # Two-Face
    'HangUp',  # Two-Face
    'RedTape',  # Two-Face
    'ParadigmShift',  # The Mingler
    'Schmooze'  # The Mingler
)

AttacksSuitB = (
    'FountainPen',  # Pencil Pusher
    'RubOut',  # Pencil Pusher
    'FingerWag',  # Pencil Pusher
    'WriteOff',  # Pencil Pusher, Spin Doctor, Bean Counter, Loan Shark
    'FillWithLead',  # Pencil Pusher
    'Canned',  # Downsizer
    'Downsize',  # Downsizer
    'PinkSlip',  # Downsizer
    'Sacked',  # Downsizer
    'EvictionNotice',  # Bloodsucker
    'RedTape',  # Bloodsucker
    'Withdrawal',  # Bloodsucker
    'Liquidate',  # Bloodsucker
    'Shake',  # Ambulance Chaser
    'RedTape',  # Ambulance Chaser
    'Rolodex',  # Ambulance Chaser, Telemarketer
    'HangUp',  # Ambulance Chaser
    'ParadigmShift',  # Spin Doctor
    'Quake',  # Spin Doctor, Mover & Shaker
    'Spin',  # Spin Doctor
    'Audit',  # Bean Counter
    'Calculate',  # Bean Counter
    'Tabulate',  # Bean Counter
    'Bite',  # Loan Shark
    'Chomp',  # Loan Shark
    'PlayHardball',  # Loan Shark
    'ClipOnTie',  # Telemarketer
    'PickPocket',  # Telemarketer
    'DoubleTalk',  # Telemarketer
    'BrainStorm',  # Mover & Shaker
    'HalfWindsor',  # Mover & Shaker
    'Shake',  # Mover & Shaker
    'Tremor'  # Mover & Shaker
)

AttacksSuitC = (
    'PoundKey',  # Flunky, Cold Caller
    'Shred',  # Flunky, Bottom Feeder
    'ClipOnTie',  # Flunky, Short Change
    'Demotion',  # Micromanager
    'FingerWag',  # Micromanager, Tightwad
    'FountainPen',  # Micromanager, Glad Hander
    'BrainStorm',  # Micromanager
    'BuzzWord',  # Micromanager
    'Canned',  # Corporate Raider
    'EvilEye',  # Corporate Raider
    'PlayHardball',  # Corporate Raider
    'PowerTie',  # Corporate Raider, Money Bags
    'RubberStamp',  # Bottom Feeder
    'Watercooler',  # Bottom Feeder, Short Change
    'PickPocket',  # Bottom Feeder, Short Change
    'BounceCheck',  # Short Change, Tightwad
    'Fired',  # Tightwad
    'GlowerPower',  # Tightwad
    'FreezeAssets',  # Tightwad, Cold Caller
    'Liquidate',  # Money Bags
    'MarketCrash',  # Money Bags
    'DoubleTalk',  # Cold Caller
    'HotAir',  # Cold Caller
    'RubberStamp',  # Glad Hander
    'Filibuster',  # Glad Hander
    'Schmooze'  # Glad Hander
)

body2Attacks = {'a': AttacksSuitA, 'b': AttacksSuitB, 'c': AttacksSuitC}


def generateRandomSuit(seed, stability=0.95):
    # Seed the suit
    random.seed(seed * time.time())

    # Determine a department and body size
    department = random.choice(CogDepts)
    body = random.choice(('a', 'b', 'c'))
    size = round(random.uniform(2, 8), 1)

    suitTextures = None

    # Determine hand color through stability
    if random.random() > stability:
        handColor = random.choice(list(dept2PolyColor.values()))
    else:
        handColor = dept2PolyColor.get(department)

    head = random.choice(list(SuitHeadDict.keys()))
    headInfo = SuitHeadDict[head]
    filePrefix, phase = HeadModelDict[headInfo[HEAD_SIZE]]
    headPath = 'phase_' + str(phase) + filePrefix + 'heads'
    headModel = ((head, headPath),)
    headColor = random.choice(headInfo[HEAD_COLORS])
    headTexture = random.choice(headInfo[HEAD_TEXTURES])

    height = size + 1.5
    rakeOffset = 0.0,
    largeSuit = True if size >= 5.5 else False

    namePrefix = None
    nameSuffix = None
    if random.random() > 0.5:
        for prefix in RandomSuitPrefixes:
            if headTexture:
                headName = headTexture
            else:
                headName = head
            if prefix.lower() in headName:
                namePrefix = prefix
                break
        if not namePrefix:
            namePrefix = random.choice(RandomSuitPrefixes)
        nameSuffix = random.choice(RandomSuitSuffixes)
    else:
        for suffix in RandomSuitSuffixes:
            if headTexture:
                headName = headTexture
            else:
                headName = head
            if suffix.lower() in headName:
                nameSuffix = suffix
                break
        if not nameSuffix:
            nameSuffix = random.choice(RandomSuitSuffixes)
        namePrefix = random.choice(RandomSuitPrefixes)

    name = namePrefix + ' ' + nameSuffix

    nameSingular = 'a {}'.format(name)
    namePlural = '{}s'.format(name)

    level = random.randrange(0, 8)
    generalAccuracy = (35, 40, 45, 50, 55)

    # Generate random attacks
    attacks = []
    numAttacks = random.randrange(2, 6)
    attackChance = 100 / numAttacks
    attackPool = body2Attacks.get(body)
    chosenAttacks = random.sample(attackPool, numAttacks)

    for attack in chosenAttacks:
        baseDamage = max(((level * 2) - 4), 1)
        damageModifier = random.randrange(1, 4)
        damageValues = []
        baseAccuracy = max(((level * 10) - 5), 50)
        accuracyModifier = 5
        accuracyValues = []
        for i in range(5):
            damage = baseDamage + (i * damageModifier)
            damageValues.append(damage)

            accuracy = baseAccuracy + (i * accuracyModifier)
            accuracyValues.append(accuracy)
        attackStruct = (
            attack, damageValues, accuracyValues,
            (attackChance, attackChance, attackChance, attackChance, attackChance))
        attacks.append(attackStruct)

    # Append png to our head texture if we have one
    if headTexture:
        # todo: have this be configurable
        headTexture += '.png'

    # Structure the suit entry into a dictionary
    suitEntry = (
        department, body, size, suitTextures, handColor, headColor, headTexture, headModel, height,
        (rakeOffset, largeSuit),
        {
            'name': name,
            'singularname': nameSingular,
            'pluralname': namePlural,
            'level': level,
            'acc': generalAccuracy,
            'attacks': attacks
        })

    # Save this entry in our preset suits if we need to access it later
    SuitPresets[seed] = suitEntry

    return suitEntry


TotalOriginalPresetSuits = 32


def getOriginalPresetSuits():
    suitTypes = list(SuitPresets.keys())
    return suitTypes[:TotalOriginalPresetSuits]


def getPresetSuits():
    suitTypes = list(SuitPresets.keys())
    return suitTypes


OriginalPresetSuits = getOriginalPresetSuits()
PresetSuits = getPresetSuits()


def getSuit(suitName, stability=0.95):
    # Try to retrieve the suit name from the preset suit dictionary
    suit = SuitPresets.get(suitName)
    if suit:
        return suit

    # If it doesn't exist, that means we should generate a random suit
    suit = generateRandomSuit(suitName, stability)
    if suit:
        return suit

    return None


def getSuitBodyType(name):
    suitInfo = getSuit(name)
    if not suitInfo:
        print('Unknown body type for suit name: ', name)
        return
    suitBody = suitInfo[SUIT_BODY]
    return suitBody


def getSuitDept(name):
    suitInfo = getSuit(name)
    suitDept = suitInfo[SUIT_DEPT]
    return suitDept


def getDeptFullname(dept):
    return suitDeptFullnames[dept]


def getDeptFullnameP(dept):
    return suitDeptFullnamesP[dept]


def getSuitDeptFullname(name):
    return suitDeptFullnames[getSuitDept(name)]


def getSuitType(name):
    suitInfo = getSuit(name)
    suitBattleInfo = suitInfo[SUIT_BATTLE_INFO]
    suitType = suitBattleInfo['level'] + 1
    return suitType


def getRandomSuitType(level, rng=random):
    return random.randint(max(level - 4, 1), min(level, 8))


def getRandomSuitByDept(dept):
    deptNumber = suitDepts.index(dept)
    cogTypes = OriginalPresetSuits
    return cogTypes[suitsPerDept * deptNumber + random.randint(0, 7)]


class SuitDNAExtended(SuitDNA.SuitDNA):
    """
    Portable DLC upgrades for SuitDNA.
    """

    def __init__(self, str=None, type=None, dna=None, r=None, b=None, g=None):
        super().__init__(
            str, type, dna, r, g, b
        )

    def makeFromNetString(self, string):
        dg = PyDatagram(string)
        dgi = PyDatagramIterator(dg)
        self.type = dgi.getFixedString(1)
        if self.type == 's':
            self.name = dgi.getFixedString(5)
            self.dept = dgi.getFixedString(1)
            self.body = getSuitBodyType(self.name)
        elif self.type == 'b':
            self.dept = dgi.getFixedString(1)
        else:
            self.notify.error('unknown avatar type: ', self.type)
        return None

    def __defaultSuit(self):
        self.type = 's'
        self.name = 'ds'
        self.dept = getSuitDept(self.name)
        self.body = getSuitBodyType(self.name)

    def newSuit(self, name=None):
        if name == None:
            self.__defaultSuit()
        else:
            self.type = 's'
            self.name = name
            self.dept = getSuitDept(self.name)
            self.body = getSuitBodyType(self.name)

    def newSuitRandom(self, level=None, dept=None):
        self.type = 's'
        if level == None:
            level = random.choice(range(1, len(suitsPerLevel)))
        elif level < 0 or level > len(suitsPerLevel):
            self.notify.error('Invalid suit level: %d' % level)
        if dept == None:
            dept = random.choice(suitDepts)
        self.dept = dept
        index = suitDepts.index(dept)
        base = index * suitsPerDept
        offset = 0
        if level > 1:
            for i in range(1, level):
                offset = offset + suitsPerLevel[i - 1]
        bottom = base + offset
        top = bottom + suitsPerLevel[level - 1]
        cogTypes = PresetSuits
        self.name = cogTypes[random.choice(range(bottom, top))]
        self.body = getSuitBodyType(self.name)

    # def newSuitInfusion(self, suitHead, suitBody):
    #
    #     self.body = getSuitBodyType()
