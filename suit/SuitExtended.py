import random

import os
from panda3d.core import Texture
from pathlib import Path

from toontown.suit import Suit
from . import SuitDNAExtended
from .SuitEnums import SuitHandColor, SuitHeadColor, SpecialSuitDepartment, SuitDepartment, SuitHandTexture, SuitName
from .. import OP_DIR


class SuitExtended(Suit.Suit):
    def __init__(self):
        super().__init__()

    def generateSuit(self, generateNormally=True, haphazard=False):
        # if generateNormally:
        #     super().generateSuit()
        #     return

        # Well, if we've gotten here, we must be a haphazard Cog.
        dna = self.style
        self.headParts = []
        self.headColor = None
        self.headTexture = None
        self.loseActor = None
        self.isSkeleton = 0
        self.corpMedallion = None

        suitName = dna.name
        suitInfo = SuitDNAExtended.getSuit(suitName)
        suitBody = suitInfo[SuitDNAExtended.SUIT_BODY]

        scaleModifier = SuitDNAExtended.SuitScaleModifiers.get(suitBody)
        self.scale = suitInfo[SuitDNAExtended.SUIT_SCALE] / scaleModifier

        self.handColor = suitInfo[SuitDNAExtended.SUIT_HAND_COLOR]

        self.generateBody(haphazard = haphazard)

        self.headColor = suitInfo[SuitDNAExtended.SUIT_HEAD_COLOR]
        self.headTexture = suitInfo[SuitDNAExtended.SUIT_HEAD_TEXTURE]

        for suitHead in suitInfo[SuitDNAExtended.SUIT_HEAD]:
            if isinstance(suitHead, tuple):
                self.generateHead(*suitHead)
            else:
                self.generateHead(suitHead)

        suitHeight = suitInfo[SuitDNAExtended.SUIT_HEIGHT]
        self.setHeight(suitHeight)

        self.setName(SuitDNAExtended.getSuit(dna.name)[SuitDNAExtended.SUIT_BATTLE_INFO]['name'])
        self.getGeomNode().setScale(self.scale)
        self.generateHealthBar()
        self.generateCorporateMedallion()

    def setDNA_random(self, dna):
        # If a style exists, that means we're replacing the DNA and need to regenerate the suit
        if self.style:
            self.removePart('modelRoot')
            self.style = dna
            self.generateSuit(haphazard = True)
            self.loop('neutral')

        # Otherwise this is a brand new suit, so just generate the DNA normally
        else:
            self.style = dna
            self.generateSuit(haphazard = True)

        # Turn drop shadow and nametag on
        self.initializeDropShadow()
        self.initializeNametag3d()

    def generateBody(self, haphazard=False):
        animDict = self.generateAnimDict()
        filePrefix, bodyPhase = Suit.ModelDict[self.style.body]
        self.loadModel('phase_3.5' + filePrefix + 'mod')
        self.loadAnims(animDict)
        self.setSuitClothes(haphazard = haphazard)

    def setSuitClothes(self, modelRoot=None, haphazard=False):
        base_dir = f'img/textures'

        if not modelRoot:
            modelRoot = self
        if haphazard:
            dept = random.choice(list(SuitDepartment) + list(SpecialSuitDepartment))
        else:
            dept = self.style.dept
            # I dont feel like embedding this into SuitDNA right now, so I'm just plugging it in here for feasibility:
            if dept == SpecialSuitDepartment.Statue:
                if self.name == SuitName.StatueBottomFeeder:
                    texpath = SuitHandTexture.StatueBlue
                else:
                    texpath = SuitHandTexture.StatueWhite
                handTex = loader.loadTexture(Path(texpath.value))
                handTex.setMinfilter(Texture.FTLinearMipmapLinear)
                handTex.setMagfilter(Texture.FTLinear)
                modelRoot.find('**/hands').setTexture(handTex, 1)

        torsoTex = loader.loadTexture(f'{base_dir}/{dept}_blazer.png')
        torsoTex.setMinfilter(Texture.FTLinearMipmapLinear)
        torsoTex.setMagfilter(Texture.FTLinear)
        legTex = loader.loadTexture(f'{base_dir}/{dept}_leg.png')
        legTex.setMinfilter(Texture.FTLinearMipmapLinear)
        legTex.setMagfilter(Texture.FTLinear)
        armTex = loader.loadTexture(f'{base_dir}/{dept}_sleeve.png')
        armTex.setMinfilter(Texture.FTLinearMipmapLinear)
        armTex.setMagfilter(Texture.FTLinear)
        modelRoot.find('**/torso').setTexture(torsoTex, 1)
        modelRoot.find('**/arms').setTexture(armTex, 1)
        modelRoot.find('**/legs').setTexture(legTex, 1)
        # temp hack
        # prob change to if isinstance(self.handColor, SuitHandColor)
        if isinstance(self.handColor, SuitHandColor):
            self.handColor = self.handColor.value
        modelRoot.find('**/hands').setColor(self.handColor)
        self.leftHand = self.find('**/joint_Lhold')
        self.rightHand = self.find('**/joint_Rhold')
        self.shadowJoint = self.find('**/joint_shadow')
        self.nametagJoint = self.find('**/joint_nameTag')

    def generateHead(self, headType, modelOverride=None):
        filePrefix, phase = Suit.ModelDict[self.style.body]
        if modelOverride:
            headModel = loader.loadModel(modelOverride)
        else:
            headModel = loader.loadModel('phase_' + str(phase) + filePrefix + 'heads')
        headReferences = headModel.findAllMatches('**/' + headType)
        for i in range(0, headReferences.getNumPaths()):
            headPart = self.instance(headReferences.getPath(i), 'modelRoot', 'joint_head')
            if self.headTexture:
                # if not os.path.isfile(self.headTexture):
                if "/" not in self.headTexture:
                    path = 'phase_' + str(phase) + '/maps/' + self.headTexture
                    # TODO: Hacky tempfix
                    try:
                        headTex = loader.loadTexture('phase_3.5/maps/' + self.headTexture)
                    except:
                        headTex = loader.loadTexture('phase_4/maps/' + self.headTexture)
                else:
                    path = self.headTexture
                    headTex = loader.loadTexture(path)

                headTex.setMinfilter(Texture.FTLinearMipmapLinear)
                headTex.setMagfilter(Texture.FTLinear)
                headPart.setTexture(headTex, 1)
            if self.headColor:
                if isinstance(self.headColor, SuitHeadColor):
                    self.headColor = self.headColor.value
                headPart.setColor(self.headColor)
            self.headParts.append(headPart)

        headModel.removeNode()

    def generateCorporateMedallion(self):
        icons = loader.loadModel('phase_3/models/gui/cog_icons')
        dept = self.style.dept
        chestNull = self.find('**/joint_attachMeter')
        if dept == 'c':
            self.corpMedallion = icons.find('**/CorpIcon').copyTo(chestNull)
        elif dept == 's':
            self.corpMedallion = icons.find('**/SalesIcon').copyTo(chestNull)
        elif dept == 'l':
            self.corpMedallion = icons.find('**/LegalIcon').copyTo(chestNull)
        elif dept == 'm':
            self.corpMedallion = icons.find('**/MoneyIcon').copyTo(chestNull)
        if self.corpMedallion:
            self.corpMedallion.setPosHprScale(0.02, 0.05, 0.04, 180.0, 0.0, 0.0, 0.51, 0.51, 0.51)
            self.corpMedallion.setColor(self.medallionColors[dept])
        icons.removeNode()
