import os

from modtools.modbase import ModularStart
from modtools.modbase.ModularBase import ModularBase

base = ModularBase()
base.initCR()


from toontown.pets import Pet
from toontown.pets import PetDNA
doodle = Pet.Pet()
dna = PetDNA.getRandomPetDNA()
dna = [
    0, 1, 1,
    1, 1, 0,
    1, 1, 1
]
doodle.setDNA(dna)
# doodle.generatePet()
doodle.reparentTo(render)
base.cam.reparentTo(render)
base.cam.setY(-5)
base.cam.setZ(1)
doodle.setH(180)

doodle.deleteDropShadow()


doodle.explore()
base.run()