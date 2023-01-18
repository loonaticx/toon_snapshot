"""
ToonSnapshot

Renders a transparent image of a Toon using an offscreen buffer.

@author Loonatic

Todo features:
    Eyes (sad, angry, shock)
    Cheesy Effects
    Toon DNA String support

"""
from panda3d.core import LVecBase3f, Vec3, deg2Rad

import random
from math import tan
from modtools.extensions.toon_snapshot.snapshot.RenderEnums import RenderType, ChatBubbleType, ChatFlag, MuzzleType

if __name__ == "__main__":
    from modtools.modbase import ModularStart
    from modtools.modbase.ModularBase import ModularBase

    base = ModularBase()
    base.initNametagGlobals()

from direct.directnotify import DirectNotifyGlobal
from toontown.toon import Toon
# from toontown.toon import ToonDNA
from modtools.extensions.toon_snapshot.toon import ToonDNAExtended
from toontown.toon import NPCToons
from modtools.extensions.toon_snapshot.snapshot.SnapshotBase import SnapshotBase
from modtools.extensions.toon_snapshot.snapshot.SnapshotExpressions import ToonExpressions
from toontown.makeatoon.NameGenerator import NameGenerator

try:
    from panda3d.otp import CFSpeech, CFTimeout
except:
    CFSpeech = ChatBubbleType.Speech
    CFTimeout = ChatFlag.Timeout
from .. import SNAPSHOT_DEBUG, OP_DIR


class ToonSnapshot(SnapshotBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('ToonSnapshot')
    notify.showTime = 1

    if SNAPSHOT_DEBUG:
        notify.setDebug(1)

    # notify.setDebug(1)

    def __init__(self, x=1024, y=1024, headless=False, filename="toon.png"):
        """
        :param int x: Width resolution of buffer image.
        :param int y: Height resolution of buffer image.
        :param bool headless: If true, will reparent the Toon to be viewable on the displayed window.
        :param str filename: Filename to save the image render to. (You can change this attrib after init as well.)
        """
        super().__init__(x, y, headless, filename)
        # searchDir = OP_DIR + "localization/"
        # self.nameGenerator = NameGenerator(filename="NameMaster_japanese.txt")
        self.nameGenerator = NameGenerator()
        # Even though RenderType.NPCs use ToonSnapshot, they generally go through the same process.
        self.type = RenderType.Toon

    def doSnapshot(self):
        """
        Calls the OffscreenRenderBuffer class, rendering the actual offscreen buffer image.
        If headless=true, the offscreen render buffer *won't* be called, and the Toon will be reparented instead.
        """
        super().doSnapshot()

    def loadToon(self, randomDNA=True, npcID=None, dnaString=None, accData=None, expressionID=1, randomExpression=True,
                 bodyShot=True, wantNametag=True, customName=None, customPhrase=None, speedchatPhrase=None,
                 chatBubbleType=ChatBubbleType.Normal, muzzleType=None, randomAccessories=False
                 ):
        """
        Loads a specified Toon to be rendered out.

        note: is not LocalToon nor localAvatar

        :param bool randomDNA: Generate a toon with random DNA. (Overrides NPC/dnaString)
        :param int npcID: ID of NPC from NPCToons (if not None)
        :param dnaString: resultant makeNetString() else None
        :type accData: list
        :param int expressionID: key id for SnapshotExpressions dict
        :param muzzleType: Override muzzle type
        """
        # Don't load in a new Toon if one already exists right now
        if self.actor:
            return

        if randomExpression:
            expressionID = random.choice(list(ToonExpressions.keys()))

        self.notify.info(f"{self.notify.getTime()}Loading Toon with properties: {(randomDNA, npcID, dnaString)}")
        self.actorDNA = ToonDNAExtended.ToonDNAExtended()
        self.actor = Toon.Toon()

        if customName:
            self.actor.setName(customName)
        else:
            self.actor.setName(self.nameGenerator.randomName())

        if randomDNA:
            self.actorDNA.newToonRandom()
            self.actorDNA.topTex, self.actorDNA.topTexColor, self.actorDNA.sleeveTex, self.actorDNA.sleeveTexColor = ToonDNAExtended.getRandomTop(self.actorDNA.gender)
            self.actorDNA.botTex, self.actorDNA.botTexColor = ToonDNAExtended.getRandomBottom(self.actorDNA.gender)
        elif npcID:
            self.actor = NPCToons.createLocalNPC(npcID)
            dnaString = 1
        else:
            self.actor.setDNAString(dnaString)  # do we need to do makeNetString here instead? idk

        if dnaString is None:
            # temp bc idk what to do here just yettt
            self.actor.setDNA(self.actorDNA)

        self.loadAccessories(accData, randomAccessories)
        self.prepareActor(wantNametag)

        # Tall toons are too tall for the window. If they fall under this, we'll shrink their scale down a bit.
        longTorso = self.actor.style.torso in ["ld", "ls"]
        longLegs = self.actor.style.legs == "l"
        self.notify.debug(self.actor.style)
        self.notify.debug(f"longTorso = {longTorso}, longLegs = {longLegs}")
        # note: Scaling might be relative to the resolution of the image. (Default is x1024)
        if longTorso and longLegs:
            # We have to scale because of horses & dogs
            self.actor.setScale(0.85, 0.85, 0.85)
        elif longLegs:
            # Scaling for accessories
            self.actor.setScale(0.80, 0.80, 0.80)

        # Once the Toon class is initialize and DNA is set, you can make your own adjustments as needed.
        # Pose avatar, adjust expression, etc.
        self.poseShot(
            expression = ToonExpressions.get(expressionID),
            bodyShot = bodyShot, wantNametag = wantNametag, customPhrase = customPhrase,
            chatBubbleType = chatBubbleType, muzzleType=muzzleType
        )

        # useful functions for later
        # reapplyCheesyEffect
        # putOnSuit

    def loadAccessories(self, accData, randomAccessories=False):
        """
        Since accessories aren't binded to ToonDNA, we need to set them manually

        :param list accData: [hat, hattex, aux, glasses, glassestex, aux, bp, bptex, aux, shoes, shoestex, shoestype]
                             aux = auxillary for potential future usage, should be 0 by default.
        """
        if randomAccessories:
            accData = []
            for entry in random.choice(list(ToonDNAExtended.HatStyles.values())):
                accData.append(entry)

            for entry in random.choice(list(ToonDNAExtended.GlassesStyles.values())):
                accData.append(entry)

            for entry in random.choice(list(ToonDNAExtended.BackpackStyles.values())):
                accData.append(entry)

            for entry in random.choice(list(ToonDNAExtended.ShoesStyles.values())):
                accData.append(entry)

        if accData is None:
            return
        ad = accData
        self.actor.setHat(ad[0], ad[1], ad[2])
        self.actor.setGlasses(ad[3], ad[4], ad[5])
        self.actor.setBackpack(ad[6], ad[7], ad[8])
        self.actor.setShoes(ad[9], ad[10], ad[11])

    def poseShot(self, expression, wantNametag, bodyShot=True, customPhrase=None, speedchatPhrase=None,
                 chatBubbleType=ChatBubbleType.Normal, muzzleType=None):
        """
        Image that contains the fullbody of the Toon.

        :param dict expression: Refer to SnapshotExpressions
        """
        # Unpack
        anim = expression[0]
        frame = expression[1]
        eyeType = expression[2]
        if not muzzleType:
            muzzleType = expression[3]
        offTrans = expression[4]
        offRot = expression[5]
        offScale = expression[6]

        # These are manual offsets
        # note: this is outdated code superseded by lookAtToon
        if bodyShot:
            # 10 is good but not for super large toons; their scale is adjusted in loadToon
            offsetY = 10 + (5 * wantNametag)
            self.actor.setPos(offTrans[0], offsetY + offTrans[1], -2.25 + offTrans[2])
        else:
            # headshot instead
            self.actor.setPos(offTrans[0], 6 + offTrans[1], -3.15 + offTrans[2])

        self.actor.setHpr(180 + offRot[0], offRot[1], offRot[2])

        # TODO: rework
        # self.actor.setScale(LVecBase3f(self.actor.getScale().__mul__(offScale[0])))
        self.actor.pose(anim, frame)
        self.makeMuzzle(muzzleType)

        target = 'head' if not bodyShot else ''
        self.lookAtToon(target)

        # Configure custom dialog if any
        if customPhrase:
            self.actor.setChatAbsolute(customPhrase, chatBubbleType | CFTimeout)
            # self.actor.displayTalk(customPhrase)

    def makeMuzzle(self, muzzleType):
        """
        :param str muzzleType: random, smile, sad, angry, laugh, shocked, normal
        """
        if muzzleType == MuzzleType.Random:
            muzzleType = random.choice([
                MuzzleType.Smile, MuzzleType.Shock, MuzzleType.Angry, MuzzleType.Laugh,
                MuzzleType.Neutral, MuzzleType.Sad
            ])
        if muzzleType == MuzzleType.Smile:
            self.actor.showSmileMuzzle()
        elif muzzleType == MuzzleType.Sad:
            self.actor.showSadMuzzle()
        elif muzzleType == MuzzleType.Angry:
            self.actor.showAngryMuzzle()
        elif muzzleType == MuzzleType.Laugh:
            self.actor.showLaughMuzzle()
        elif muzzleType == MuzzleType.Shock:
            self.actor.showSurpriseMuzzle()

    def lookAtToon(self, lookAtTarget='head'):
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
            head = self.actor.getPart('head', '1000')
            headParent = head.getParent()
            # Temporarily reparent head to render to get bounds aligned with render
            head.wrtReparentTo(self.render)
            # Look for explicitly named ears and stash them
            ears = head.findAllMatches('**/ear*')
            # And stash them before computing bounds
            for ear in ears:
                ear.stash()
            stashed = []

            # If this is a horse and we didn't find any ears, stash nodes with empty string names
            if ears.isEmpty() and (self.actor.style.head[0] == 'h'):
                # Now stash all unnamed nodes
                for child in head.getChildrenAsList():
                    if child.getName() == '':
                        stashed.append(child)
                        child.stash()

            # Where is center of head in render space?
            p1, p2 = head.getTightBounds()
            # Put all stashed things back
            for ear in ears:
                ear.unstash()
            for child in stashed:
                child.unstash()
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
        self.camera.setHpr(self.render, 0, 0, 0)
        self.camera.setPos(self.render, c)
        # Move it back to fit around the target
        offset = ((height / 2.0) / tan(deg2Rad((fillFactor * effectiveFOV) / 2.0)))
        self.camera.setY(self.camera, -offset)

    def cleanup(self):
        """
        Start over and clear the Toon information
        """
        super().cleanup()


if __name__ == "__main__":
    # For debugging / modifying, set headless to False for opening a window instead (does not screenshot)
    x = y = 1024
    headless = False
    snapshot = ToonSnapshot(x, y, headless)
    # snapshot.loadToon(random = True, expressionID = random.randint(1, 14))  # loads in random toon w/ random pose
    randNpcID = random.choice(list(NPCToons.NPCToonDict.items()))[0]
    # loads in random npc w/ random pose
    # snapshot.loadToon(random = False, npcID = randNpcID, expressionID = random.randint(1, 14))
    # snapshot.loadToon(random = False, npcID = randNpcID, expressionID = 1)
    base.accept('1', snapshot.loadToon)
    base.accept('2', snapshot.doSnapshot)
    base.accept('3', snapshot.cleanup)

    # snapshot.loadToon(randomDNA = True, expressionID = 1)
    # snapshot.doSnapshot()
    # if headless:
    #     snapshot.cleanup()
    base.run()
