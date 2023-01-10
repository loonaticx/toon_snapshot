from panda3d.core import LVecBase3f

import random

# initial constants #
# X and Y should be the same res (1:1), else there will be weird aspect ratio issues.
from panda3d.otp import CFSpeech, CFTimeout

from modtools.extensions.toon_snapshot.snapshot.RenderEnums import RenderType, ChatBubbleType

x = y = 1024
headless = True

if __name__ == "__main__":
    from modular.toontown.toonbase import ModularStart
    from modular.toontown.toonbase.ModularBase import ModularBase

    base = ModularBase()

from toontown.pets import PetDNA, Pet

from direct.directnotify import DirectNotifyGlobal
from modtools.extensions.toon_snapshot.snapshot.SnapshotExpressions import DoodleExpressions
from toontown.pets.PetNameGenerator import PetNameGenerator
from modtools.extensions.toon_snapshot.snapshot.SnapshotBase import SnapshotBase


class DoodleSnapshot(SnapshotBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('ToonSnapshot')
    notify.showTime = 1

    # notify.setDebug(1)

    def __init__(self, x=1024, y=1024, headless=False, filename="toon.png"):
        """
        :param int x: Width resolution of buffer image.
        :param int y: Height resolution of buffer image.
        :param bool headless: If true, will reparent the Toon to be viewable on the displayed window.
        :param str filename: Filename to save the image render to. (You can change this attrib after init as well.)
        """
        super().__init__(x, y, headless, filename)
        self.nameGenerator = PetNameGenerator()
        self.type = RenderType.Doodle

    def doSnapshot(self):
        """
        Calls the OffscreenRenderBuffer class, rendering the actual offscreen buffer image.
        If headless=true, the offscreen render buffer *won't* be called, and the Toon will be reparented instead.
        """
        super().doSnapshot()

    def loadDoodle(self, randomDNA=True, expressionID=1, randomExpression=True, wantNametag=True,
                   doodleName=None, customPhrase=False, chatBubbleType=ChatBubbleType.Normal):
        # Don't load in a new Doodle if one already exists right now
        if self.actor:
            return

        self.actor = Pet.Pet()

        if randomDNA:
            self.doodleDNA = PetDNA.getRandomPetDNA()
        self.actor.setDNA(self.doodleDNA)

        self.prepareActor(wantNametag)

        if doodleName:
            self.actor.setName(doodleName)
        else:
            self.actor.setName(self.nameGenerator.randomName())

        if randomExpression:
            expressionID = random.randint(1, len(DoodleExpressions.keys()))
        self.poseShot(DoodleExpressions.get(expressionID), wantNametag, customPhrase=customPhrase, chatBubbleType = chatBubbleType)

        print(f"expression id = {expressionID}")

    def poseShot(self, expression, wantNametag, customPhrase, chatBubbleType):
        """
        Image that contains the fullbody of the Doodle.

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

        offsetY = 5 + (5 * wantNametag)
        self.actor.setPos(offTrans[0], offsetY + offTrans[1], offTrans[2] - 1)
        self.actor.setHpr(180 + offRot[0], offRot[1], offRot[2])

        self.actor.pose(anim, frame)

        # Configure custom dialog if any
        if customPhrase:
            self.actor.setChatAbsolute(customPhrase, chatBubbleType | CFTimeout)

    def cleanup(self):
        """
        Start over and clear the Doodle information
        """
        super().cleanup()


if __name__ == "__main__":
    snapshot = DoodleSnapshot(x, y, headless)
    snapshot.loadDoodle()
    snapshot.doSnapshot()
    if headless:
        snapshot.cleanup()
    base.run()
