
from modtools.modbase import ModularStart
from modtools.modbase.ModularBase import ModularBase

base = ModularBase()
base.initCR()


from panda3d.core import *
# from toontown.toon import ToonDNA
# from modtools.extensions.toon_snapshot.toon import ToonDNAExtended
#
# print(ToonDNAExtended.getRandomTop('m'))
filename = Filename("PetNameMasterEnglish.txt")

vfs = VirtualFileSystem.getGlobalPtr()
input = StreamReader(vfs.openReadFile(f'modtools/extensions/toon_snapshot/localization/{filename}', 1), 1)
# f = open("README.md", "r")
#
# input = StreamReader(f.read(), 1)
print(input)

base.run()