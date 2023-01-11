"""
Module that holds various dictionaries for actor expression values.
"""

"""
# Toon Expressions #
{ expressionID : [animName, frame, eyeType, muzzleType, offXYZ, offHPR, offsXsYsZ }
eyeType = default, sad, angry, shocked, default-closed, sad-closed, angry-closed
muzzleType = default, sad, smile, angry, shocked, laugh

offScale = aren't added on, but used as a multiplier instead (please don't do negative numbers)
"""
ToonExpressions = {
    1: ["neutral", 0, "default", "default", (0, 0, 0), (0, 0, 0), (1, 1, 1)],  # Default
    2: ["good-putt", 11, "default", "smile", (0, 0, 0), (0, 0, 0), (1, 1, 1)],  # YEAH!!
    3: ["bored", 94, "default", "default", (0, 0, 0), (0, 0, 0), (1, 1, 1)],  # Bored (1)
    4: ["bored", 141, "default", "default", (0, 0, 0), (0, 0, 0), (1, 1, 1)],  # Bored (2)
    5: ["smooch", 137, "default", "shocked", (0, 0, 0), (0, 0, 0), (1, 1, 1)],  # Look at this!
    6: ["hypnotize", 9, "default", "default", (0, 0, 0), (0, 0, 0), (1, 1, 1)],  # I don't meany any trouble...
    7: ["toss", 31, "default", "default", (0, 0, 0), (0, 0, 0), (0.9, 0.9, 0.9)],  # Gimmie it. Now.
    8: ["duck", 13, "shocked", "shocked", (0, 0, 0), (0, 0, 0), (1, 1, 1)],  # WOAAH there...
    9: ["victory", 8, "default", "default", (0, 0, 0), (0, 0, 0), (0.85, 0.85, 0.85)],  # VICTORY!
    10: ["victory", 112, "default", "default", (0, 0, 0), (0, 0, 0), (1, 1, 1)],  # The W pose.
    11: ["wave", 58, "default", "smile", (0, 0, 0), (0, 0, 0), (1, 1, 1)],  # Hello!
    12: ["think", 33, "default", "default", (0, 0, 0), (0, 0, 0), (1, 1, 1)],  # Hmm..
    13: ["applause", 22, "default-closed", "laugh", (0, 0, 0), (0, 0, 0), (1, 1, 1)],  # Applause!
    14: ["sidestep-left", 38, "default-closed", "default", (-2.5, 0, 0), (-15, 0, 0), (0.85, 0.85, 0.85)],  # On side.

}

"""
# Doodle Expressions
{ expressionID : [animName, frame, ... offXYZ, offHPR, offsXsYsZ] }
"""
DoodleExpressions = {
    1: ["neutral", 0, "default", "default", (0, 0, 0), (0, 0, 0), (1, 1, 1)],  # Default
    2: ["speak", 21, "default", "default", (0, 0, 0), (0, 0, 0), (1, 1, 1)],  # Default
    3: ["playDead", 121, "default", "default", (0, 1.5, -0.25), (-5, 0, 0), (1, 1, 1)],  # Default
    4: ["jump", 9, "default", "default", (0, 0.55, -0.3), (0, 0, 0), (1, 1, 1)],  # Default
    5: ["jump", 29, "default", "default", (0, 0, 0), (0, 0, 0), (1, 1, 1)],  # Default
    6: ["eat", 22, "default", "default", (0, 0, 0), (0, 0, 0), (1, 1, 1)],  # Default
    7: ["disappear", 18, "default", "default", (0, 1, 0), (0, 0, 0), (1, 1, 1)],  # Default
    8: ["dance", 65, "default", "default", (-0.3, 1.2, 0), (5, 0, 0), (1, 1, 1)],  # Default
    9: ["toBall", 26, "default", "default", (0, 0.5, 0), (0, 0, 0), (1, 1, 1)],  # Default
    10: ["toPet", 118, "default", "default", (0, 1, 0), (-60, 0, 0), (1, 1, 1)],  # Default
    11: ["rollover", 40, "default", "default", (0, 0, 0), (0, 0, 0), (1, 1, 1)],  # Default
    12: ["reappear", 0, "default", "default", (0, 3, 1), (0, 0, 0), (1, 1, 1)],  # Default
    13: ["run", 4, "default", "default", (0, 0, 0), (5, 0, 0), (1, 1, 1)],  # Default
    14: ["dance", 32, "default", "default", (-0.2, 0.6, 0), (0, 0, 0), (1, 1, 1)],  # Default
    15: ["jump", 8, "default", "default", (0, 0.55, -0.3), (-15, 0, 0), (1, 1, 1)],  # Default
    16: ["reappear", 1, "default", "default", (0, 0, 0), (0, 0, 0), (1, 1, 1)],  # Default
    17: ["dance", 126, "default", "default", (0, 0, 0), (-5, 0, 0), (1, 1, 1)],  # Default
    18: ["dance", 156, "default", "default", (0, 0, 0), (0, 0, 0), (1, 1, 1)],  # Default
    19: ["jump", 30, "default", "default", (0, 0, 0), (0, 0, 0), (1, 1, 1)],  # Default
    20: ["playDead", 64, "default", "default", (0, 0, 0), (0, 0, 0), (1, 1, 1)],  # Default
    21: ["playDead", 210, "default", "default", (0, 0, 0), (0, 0, 0), (1, 1, 1)],  # Default
    22: ["fromPlayDead", 19, "default", "default", (0, 0, 0), (0, 0, 0), (1, 1, 1)],  # Default
    23: ["speak", 18, "default", "default", (0, 0, 0), (0, 0, 0), (1, 1, 1)],  # Default
    24: ["walkHappy", 7, "default", "default", (0, 0, 0), (0, 0, 0), (1, 1, 1)],  # Default
}


"""
# Suit Expressions #
{ expressionID : [animName, frame, ... offXYZ, offHPR, offsXsYsZ] }
"""
SuitExpressions = {
    'a': {
        1: ["neutral", 0, "default", "default", (0, 0, 0), (0, 0, 0), (1, 1, 1)],  # Default
    },
    'b': {
        1: ["neutral", 0, "default", "default", (0, 0, 0), (0, 0, 0), (1, 1, 1)],  # Default
    },
    'c': {
        1: ["neutral", 0, "default", "default", (0, 0, 0), (0, 0, 0), (1, 1, 1)],  # Default
        2: ["flail", 31, "c", "default", (0, 0, 0), (0, 0, 0), (1, 1, 1)],  # Default
        3: ["rake-react", 55, "c", "default", (0, 0, 0), (0, 0, 0), (1, 1, 1)],  # Default
        4: ["soak", 61, "c", "default", (0, 0, 0), (0, 0, 0), (1, 1, 1)],  # Default
        5: ["soak", 65, "c", "default", (0, 0, 0), (0, 0, 0), (1, 1, 1)],  # Default
        6: ["throw-paper", 67, "c", "default", (0, 0, 0), (0, 0, 0), (1, 1, 1)],  # Default
        7: ["drop-react", 43, "c", "default", (0, 2, -1), (0, 0, 0), (1, 1, 1)],  # Default
        8: ["slip-forward", 13, "c", "default", (0, 2, -1), (0, 0, 0), (1, 1, 1)],  # Default
        9: ["slip-backward", 59, "c", "default", (0, 2, -1), (0, 0, 0), (1, 1, 1)],  # Default
        10: ["victory", 28, "c", "default", (0, 2, -1), (0, 0, 0), (1, 1, 1)],  # Default
        11: ["rake-react", 59, "c", "default", (0, 0, 0), (0, 0, 0), (1, 1, 1)],  # Default
        12: ["squirt-small-react", 25, "c", "default", (0, 0, 0), (0, 0, 0), (1, 1, 1)],  # Default
        13: ["squirt-forward", 48, "c", "default", (0, 0, 0), (0, 0, 0), (1, 1, 1)],  # Default
        14: ["squirt-forward", 72, "c", "default", (0, 0, 0), (0, 0, 0), (1, 1, 1)],  # Default
    },
}