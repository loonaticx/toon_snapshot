from toontown.toon.ToonDNA import *

from toontown.toon import ToonDNA

def getRandomTop(gender, tailorId = MAKE_A_TOON, generator = None, collection=None):
    if generator == None:
        generator = random
    # collection = TailorCollections[tailorId]
    return generator.choice(getAllTops(gender))

def getRandomBottom(gender, tailorId = MAKE_A_TOON, generator = None, collection=None):
    if generator == None:
        generator = random
    # collection = TailorCollections[tailorId]
    return generator.choice(getAllBottoms(gender))


class ToonDNAExtended(ToonDNA.ToonDNA):
    def __init__(self, str=None, type=None, dna=None, r=None, b=None, g=None):
        super().__init__(str, type, dna, r, g, b)


    def newToonRandom(self, seed = None, gender = 'm', npc = 0, stage = None):
        if seed:
            generator = random.Random()
            generator.seed(seed)
        else:
            generator = random
        self.type = 't'
        self.legs = generator.choice(toonLegTypes + ['m', 'l', 'l', 'l'])
        self.gender = gender
        if not npc:
            self.head = generator.choice(toonHeadTypes)
        else:
            self.head = generator.choice(toonHeadTypes[:22])
        top, topColor, sleeve, sleeveColor = getRandomTop(gender, generator = generator)
        bottom, bottomColor = getRandomBottom(gender, generator = generator)
        if gender == 'm':
            self.torso = generator.choice(toonTorsoTypes[:3])
            self.topTex = top
            self.topTexColor = topColor
            self.sleeveTex = sleeve
            self.sleeveTexColor = sleeveColor
            self.botTex = bottom
            self.botTexColor = bottomColor
            color = generator.choice(defaultBoyColorList)
            self.armColor = color
            self.legColor = color
            self.headColor = color
        else:
            self.torso = generator.choice(toonTorsoTypes[:6])
            self.topTex = top
            self.topTexColor = topColor
            self.sleeveTex = sleeve
            self.sleeveTexColor = sleeveColor
            if self.torso[1] == 'd':
                bottom, bottomColor = getRandomBottom(gender, generator=generator, girlBottomType=SKIRT)
            else:
                bottom, bottomColor = getRandomBottom(gender, generator=generator, girlBottomType=SHORTS)
            self.botTex = bottom
            self.botTexColor = bottomColor
            color = generator.choice(defaultGirlColorList)
            self.armColor = color
            self.legColor = color
            self.headColor = color
        self.gloveColor = 0