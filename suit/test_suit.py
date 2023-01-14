from modtools.modbase import ModularStart
from modtools.modbase.ModularBase import ModularBase

base = ModularBase()
base.initCR()

from toontown.suit import Suit
s = Suit.Suit()
from toontown.suit import SuitDNA
d = SuitDNA.SuitDNA()
# d.type = 's'
# d.makeFromNetString(bytes('sle\x00l', 'utf-8'))
d.makeFromNetString(b'sle\x00l')
# d.newSuitRandom()
# d.newSuit('tbc')
# print(d.makeNetString())
s.setDNA(d)
s.loop('neutral')
s.reparentTo(render)
s.setH(180)
# s.setPos(base.localAvatar, 0,0,0)

base.run()