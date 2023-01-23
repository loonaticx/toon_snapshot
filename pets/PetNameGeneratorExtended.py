from panda3d.core import Filename, DSearchPath, StreamReader
import random

from toontown.pets import PetNameGenerator
from toontown.toonbase import TTLocalizer


class PetNameGeneratorExtended(PetNameGenerator.PetNameGenerator):
    def __init__(self):
        self.generateLists()

    def generateLists(self):
        """ This method looks in a text file specified in the localizer and loads
            in all the names into the 8 lists as well as populating self.nameDictionary
            which has uniqueIDs mapped to a tuple of category and name
            """
        self.boyFirsts = []
        self.girlFirsts = []
        self.neutralFirsts = []
        self.nameDictionary = {}

        # Look for the name master file and read it in.
        searchPath = DSearchPath()
        searchPath.appendDirectory(Filename('resources/phase_3/etc'))

        filename = Filename(TTLocalizer.PetNameMaster)
        found = base.vfs.resolveFilename(filename, searchPath)

        if not found:
            self.notify.error("PetNameGenerator: Error opening name list text file.")

        input = StreamReader(base.vfs.openReadFile(filename, 1), 1)

        currentLine = input.readline()
        while currentLine:
            if currentLine.lstrip()[0:1] != bytes('#', 'utf-8'):
                a1 = currentLine.find(bytes('*', 'utf-8'))
                a2 = currentLine.find(bytes('*', 'utf-8'), a1 + 1)
                self.nameDictionary[int(currentLine[0:a1])] = (
                    int(currentLine[a1 + 1:a2]), currentLine[a2 + 1:len(currentLine) - 1].strip()
                )
            currentLine = input.readline()

        masterList = [self.boyFirsts, self.girlFirsts, self.neutralFirsts]
        for tu in self.nameDictionary.values():
            masterList[tu[0]].append(tu[1])
        return 1

    def randomName(self, gender = None, seed = None):
        S = random.getstate()
        if seed is not None:
            random.seed(seed)
        if gender is None:
            gender = random.choice([0, 1])
        retString = ''
        firstList = self.neutralFirsts[:]
        if gender == 0:
            firstList += self.boyFirsts
        elif gender == 1:
            firstList += self.girlFirsts
        else:
            self.error('Must be boy or girl.')
        retString += random.choice(firstList).decode('utf-8')
        random.setstate(S)
        return retString