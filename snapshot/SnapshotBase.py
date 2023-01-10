# initial constants #
# X and Y should be the same res (1:1), else there will be weird aspect ratio issues.
from modtools.extensions.toon_snapshot.snapshot.RenderEnums import RenderType

x = y = 1024
headless = False

if __name__ == "__main__":
    from modular.toontown.toonbase import ModularStart
    from modular.toontown.toonbase.ModularBase import ModularBase
    base = ModularBase()
    base.initNametagGlobals()

from direct.directnotify import DirectNotifyGlobal
from modtools.extensions.toon_snapshot.snapshot.OffscreenRenderBuffer import OffscreenRenderBuffer


class SnapshotBase(OffscreenRenderBuffer):
    notify = DirectNotifyGlobal.directNotify.newCategory('SnapshotBase')
    notify.showTime = 1

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
        self.filename = filename
        self.actor = None
        self.actorDNA = None
        self.nameGenerator = None
        self.type = RenderType.Random

    def prepareActor(self, wantNametag):
        """
        Perform common operations for setting up a Render actor.
        """
        self.actor.reparentTo(self.render)
        self.actor.setH(180)
        self.actor.deleteDropShadow()
        self.actor.doId = -1

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
        if hasattr(self.actor, 'delete'):
            self.actor.delete()
        if hasattr(self.actor, 'cleanup'):
            self.actor.cleanup()
        self.actor = None
        if self.actorDNA:
            self.actorDNA = None
