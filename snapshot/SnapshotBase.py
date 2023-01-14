from modtools.extensions.toon_snapshot.snapshot.RenderEnums import RenderType
from .. import SNAPSHOT_PREFIX

if __name__ == "__main__":
    from modtools.modbase import ModularStart
    from modtools.modbase.ModularBase import ModularBase

    base = ModularBase()
    base.initNametagGlobals()

from direct.directnotify import DirectNotifyGlobal
from modtools.extensions.toon_snapshot.snapshot.OffscreenRenderBuffer import OffscreenRenderBuffer

import typing

if typing.TYPE_CHECKING:
    try:
        from otp.avatar.Avatar import Avatar
        from otp.avatar.AvatarDNA import AvatarDNA
        from toontown.makeatoon.NameGenerator import NameGenerator
        from toontown.pets.PetNameGenerator import PetNameGenerator
    except:
        pass


class SnapshotBase(OffscreenRenderBuffer):
    notify = DirectNotifyGlobal.directNotify.newCategory('SnapshotBase')
    notify.showTime = 1

    # X and Y should be the same res (1:1), else there will be weird aspect ratio issues.
    def __init__(self, x=1024, y=1024, headless=False, filename="render.png"):
        """
        :param int x: Width resolution of buffer image.
        :param int y: Height resolution of buffer image.
        :param bool headless: If true, will reparent the Toon to be viewable on the displayed window.
        :param str filename: Filename to save the image render to. (You can change this attrib after init as well.)
        """
        self.buff = super().__init__(x, y)
        # Since we already initialized ShowBase and explicitly defined headless, we can set the value here.
        self.headless = headless
        self.filename = SNAPSHOT_PREFIX + filename
        self.actor = None  # type: Avatar
        self.actorDNA = None  # type: AvatarDNA
        self.nameGenerator = None  # type: NameGenerator | PetNameGenerator
        self.type = RenderType.Random
        self.extraInfo = dict()  # The server can grab this to see if we need to send additional info out to the user.

    def prepareActor(self, wantNametag):
        """
        Perform common operations for setting up a Render actor.
        """
        # Parent our actor to our special render.
        self.actor.reparentTo(self.render)

        # All actors are initially facing away from the camera. Let's fix this.
        # self.actor.faceTowardsViewer()
        self.actor.setH(180)

        # Drop shadows don't really look good in renders.
        self.actor.deleteDropShadow()

        # Not really needed, but just in case we want to do any fancy calls:
        self.actor.doId = -1

        # Should we display the nametag?
        if wantNametag:
            self.actor.nametag.manage(base.marginManager)
            self.actor.setNameVisible(1)

    def doSnapshot(self):
        """
        Calls the OffscreenRenderBuffer class, rendering the actual offscreen buffer image.
        If headless=true, the offscreen render buffer *won't* be called, and the Toon will be reparented instead.
        """
        if self.headless:
            self.renderFrame()
            self.snapshot(self.filename)
        else:
            # Used for debugging the offscreen buffer.
            # Reparents the offscreen buffer nodes to the normally visible/workable nodes
            self.render.reparentTo(render)
            self.cam.reparentTo(camera)

    def getInfo(self):
        return [
            self.actor.getName()
        ]

    def cleanup(self):
        """
        Start over and clear the Actor information
        """
        camera.setHpr(0, 0, 0)
        camera.setPos(0, 0, 0)
        if hasattr(self.actor, 'delete'):
            self.actor.delete()
        if hasattr(self.actor, 'cleanup'):
            self.actor.cleanup()
        self.actor = None
        if self.actorDNA:
            self.actorDNA = None
