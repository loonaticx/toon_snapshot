from math import tan

import time

from panda3d.core import LVecBase3f, deg2Rad, Vec3

import random

from modtools.extensions.toon_snapshot import SNAPSHOT_DEBUG
from modtools.extensions.toon_snapshot.snapshot.RenderEnums import RenderType, ChatBubbleType, ChatFlag
from modtools.extensions.toon_snapshot.snapshot.SnapshotBase import SnapshotBase

try:
    from panda3d.otp import CFSpeech, CFTimeout
except:
    CFSpeech = ChatBubbleType.Speech
    CFTimeout = ChatFlag.Timeout


if __name__ == "__main__":
    from modtools.modbase import ModularStart
    from modtools.modbase.ModularBase import ModularBase

    base = ModularBase(wantHotkeys = False)
    base.initNametagGlobals()

from toontown.suit import SuitDNAExtended, Suit, SuitDNA

from direct.directnotify import DirectNotifyGlobal
from modtools.extensions.toon_snapshot.snapshot.SnapshotExpressions import SuitExpressions


class SuitSnapshot(SnapshotBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('SuitSnapshot')
    notify.showTime = 1

    if SNAPSHOT_DEBUG:
        notify.setDebug(1)

    # notify.setDebug(1)

    def __init__(self, x=1024, y=1024, headless=False, filename="suit.png"):
        """
        :param int x: Width resolution of buffer image.
        :param int y: Height resolution of buffer image.
        :param bool headless: If true, will reparent the Toon to be viewable on the displayed window.
        :param str filename: Filename to save the image render to. (You can change this attrib after init as well.)
        """
        super().__init__(x, y, headless, filename)
        self.type = RenderType.Suit

    def doSnapshot(self):
        """
        Calls the OffscreenRenderBuffer class, rendering the actual offscreen buffer image.
        If headless=true, the offscreen render buffer *won't* be called, and the Toon will be reparented instead.
        """
        super().doSnapshot()

    def loadSuit(self, randomDNA=True, haphazardDNA=False, expressionID=1, randomExpression=True, wantNametag=True,
                 suitName=None, bodyShot=True, customPhrase=True, chatBubbleType=ChatBubbleType.Normal):
        # Don't load in a new Suit if one already exists right now
        if self.actor:
            return

        self.actor = Suit.Suit()

        if haphazardDNA:
            self.generateHaphazardSuit()
        else:
            self.actorDNA = SuitDNA.SuitDNA()
            if randomDNA:
                self.actorDNA.newSuitRandom()
            else:
                self.actorDNA.newSuit(suitName)
            self.actor.setDNA(self.actorDNA)
            self.actor.dna = self.actorDNA

        self.prepareActor(wantNametag)

        if suitName:
            self.actor.setName(suitName)

        # Use a certain expression set depending on the suit body type
        expressionSet = SuitExpressions[self.actor.dna.body]
        if randomExpression:
            expressionID = random.randint(1, len(expressionSet.keys()))
            self.notify.debug(f"expressionID: {expressionID}")
        self.poseShot(expressionSet.get(expressionID), wantNametag, bodyShot = bodyShot, customPhrase=customPhrase, chatBubbleType = chatBubbleType)


    def generateHaphazardSuit(self, rmin=1, rmax=1000):
        random.seed(random.random())
        suitId = random.randrange(rmin, rmax)
        suitName = f'random_{suitId}'
        suitInfo = SuitDNAExtended.getSuit(suitName)
        suitDept = suitInfo[SuitDNAExtended.SUIT_DEPT]
        battleInfo = suitInfo[SuitDNAExtended.SUIT_BATTLE_INFO]
        suitType = battleInfo['level']

        self.actor = Suit.Suit()
        self.actorDNA = SuitDNAExtended.SuitDNAExtended()
        self.actorDNA.newSuitRandom(suitType, suitDept)
        self.actor.dna = self.actorDNA
        self.actor.dna.dept = suitDept
        self.actor.dna.name = suitName
        self.actor.setDNA_random(self.actorDNA)

    def poseShot(self, expression, wantNametag, bodyShot, customPhrase, chatBubbleType):
        """
        Image that contains the fullbody of the Toon.

        :param dict expression: Refer to SnapshotExpressions
        """
        # Unpack
        anim = expression[0]
        frame = expression[1]
        eyeType = expression[2]
        muzzleType = expression[3]
        offTrans = expression[4]
        offRot = expression[5]
        offScale = expression[6]

        # putting this higher up to evade some tpose circumstances
        self.actor.pose(anim, frame)

        # todo: only apply if cog is like tbc
        extraY = 3
        # TODO: FINE TUNE ME LATER
        if SuitDNAExtended.getSuitBodyType(self.actor.dna.name) == "c":
            pass
        lazyY = 8
        offsetY = 12 + (1 * wantNametag) + extraY + lazyY
        extraZ = -1.15
        offsetZ = -4 + extraZ

        self.actor.setPos(offTrans[0], offsetY + offTrans[1], offsetZ + offTrans[2])
        self.actor.setHpr(180 + offRot[0], offRot[1], offRot[2])

        target = 'head' if not bodyShot else ''
        self.lookAtSuit(target)
        # Configure custom dialog if any
        if customPhrase:
            self.actor.setChatAbsolute(customPhrase, chatBubbleType | CFTimeout)


    def lookAtSuit(self, lookAtTarget='head'):
        fillFactor = 0.6
        fov = 50
        # effectiveFOV is the approximate FOV of the ring
        # effectiveFOV = fov * 0.75
        effectiveFOV = fov

        def calcBodyBounds():
            p1, p2 = self.actor.getTightBounds()
            c = Vec3((p2 + p1) / 2.0)
            delta = p2 - p1
            return c, delta[2]

        def calcHeadBounds():
            head = self.actor.getHeadParts()[0]
            headParent = head.getParent()
            # Temporarily reparent head to render to get bounds aligned with render
            head.wrtReparentTo(self.render)

            # Where is center of head in render space?
            p1, p2 = head.getTightBounds()
            c = Vec3((p2 + p1) / 2.0)
            delta = p2 - p1

            # Restore orientation
            head.wrtReparentTo(headParent)
            return c, delta[2]

        if lookAtTarget == 'head':
            c, height = calcHeadBounds()
        else:
            c, height = calcBodyBounds()

        # Move camera there
        camera.setHpr(self.render, 0, 0, 0)
        camera.setPos(self.render, c)
        # Move it back to fit around the target
        offset = ((height / 2.0) / tan(deg2Rad((fillFactor * effectiveFOV) / 2.0)))
        camera.setY(camera, -offset)

    def cleanup(self):
        """
        Start over and clear the Toon information
        """
        super().cleanup()


if __name__ == "__main__":
    # X and Y should be the same res (1:1), else there will be weird aspect ratio issues.
    x = y = 1024
    headless = False
    snapshot = SuitSnapshot(x, y, headless)

    base.accept('1', snapshot.loadSuit, extraArgs = [False, True])
    base.accept('2', snapshot.doSnapshot)
    base.accept('3', snapshot.cleanup)
    # snapshot.loadSuit(randomDNA=False, haphazardDNA = True)
    # snapshot.doSnapshot()
    # if headless:
    #     snapshot.cleanup()
    base.run()
