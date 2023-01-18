from panda3d.core import Filename, StreamReader

from toontown.makeatoon.NameGenerator import NameGenerator
from toontown.toonbase import TTLocalizer


class NameGeneratorExtended(NameGenerator):
    def __init__(self, filename=None, sourcePath=None):
        self.filename = filename
        self.sourcePath = sourcePath
        super().__init__()

    def generateLists(self):
        self.boyTitles = []
        self.girlTitles = []
        self.neutralTitles = []
        self.boyFirsts = []
        self.girlFirsts = []
        self.neutralFirsts = []
        self.capPrefixes = []
        self.lastPrefixes = []
        self.lastSuffixes = []
        self.nameDictionary = {}

        if self.filename:
            filename = Filename(self.filename)
        else:
            filename = Filename(TTLocalizer.NameShopNameMaster)

        found = base.vfs.resolveFilename(filename, self.sourcePath)

        if not found:
            self.notify.error("NameGenerator: Error opening name list text file '%s.'" % filename)

        input = StreamReader(base.vfs.openReadFile(filename, 1), 1)

        currentLine = input.readline()
        while currentLine:
            if currentLine.lstrip()[0:1] != bytes('#'):
                a1 = currentLine.find(bytes('*'))
                a2 = currentLine.find(bytes('*'), a1 + 1)
                self.nameDictionary[int(currentLine[0:a1])] = (
                    int(currentLine[a1 + 1:a2]), currentLine[a2 + 1:].rstrip().decode('utf-8'))

            currentLine = input.readline()

        masterList = [
            self.boyTitles, self.girlTitles, self.neutralTitles,
            self.boyFirsts, self.girlFirsts, self.neutralFirsts,
            self.capPrefixes, self.lastPrefixes, self.lastSuffixes
        ]
        for tu in list(self.nameDictionary.values()):
            masterList[tu[0]].append(tu[1])

        return 1

    def totalNames(self):
        totalNames = []
        firsts = len(self.boyFirsts) + len(self.girlFirsts) + len(self.neutralFirsts)
        totalNames.append('Total firsts: ' + str(firsts))
        lasts = len(self.lastPrefixes) * len(self.lastSuffixes)
        totalNames.append('Total lasts: ' + str(lasts))

        neutralTitleFirsts = len(self.neutralTitles) * len(self.neutralFirsts)
        boyTitleFirsts = len(self.boyTitles) * (len(self.neutralFirsts) + len(self.boyFirsts)) + len(
            self.neutralTitles) * len(self.boyFirsts)
        girlTitleFirsts = len(self.girlTitles) * (len(self.neutralFirsts) + len(self.girlFirsts)) + len(
            self.neutralTitles) * len(self.girlFirsts)
        totalTitleFirsts = neutralTitleFirsts + boyTitleFirsts + girlTitleFirsts
        totalNames.append('Total title firsts: ' + str(totalTitleFirsts))

        neutralTitleLasts = len(self.neutralTitles) * lasts
        boyTitleLasts = len(self.boyTitles) * lasts
        girlTitleLasts = len(self.girlTitles) * lasts
        totalTitleLasts = neutralTitleLasts + boyTitleFirsts + girlTitleLasts
        totalNames.append('Total title lasts: ' + str(totalTitleLasts))

        neutralFirstLasts = len(self.neutralFirsts) * lasts
        boyFirstLasts = len(self.boyFirsts) * lasts
        girlFirstLasts = len(self.girlFirsts) * lasts
        totalFirstLasts = neutralFirstLasts + boyFirstLasts + girlFirstLasts

        totalNames.append('Total first lasts: ' + str(totalFirstLasts))
        neutralTitleFirstLasts = neutralTitleFirsts * lasts
        boyTitleFirstLasts = boyTitleFirsts * lasts
        girlTitleFirstLasts = girlTitleFirsts * lasts
        totalTitleFirstLasts = neutralTitleFirstLasts + boyTitleFirstLasts + girlTitleFirstLasts
        totalNames.append('Total title first lasts: ' + str(totalTitleFirstLasts))
        totalNames = firsts + lasts + totalTitleFirsts + totalTitleLasts + totalFirstLasts + totalTitleFirstLasts
        totalNames.append('Total Names: ' + str(totalNames))
        return totalNames
