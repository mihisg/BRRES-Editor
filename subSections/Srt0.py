from subSections.SubSection import SubSection
from struct import Struct
from brres.BRRESIndexGroup import BRRESIndexGroup


class Srt0Header:
    def __init__(self):
        self.unk0 = 0
        self.frames = 0
        self.animations = 0
        self.matrixMode = 0
        self.looping = False
        
    def unpack(self, data):
        self.unk0, self.frames, self.animations, self.matrixMode, looping = Struct(">IHHII").unpack(data)
        self.looping = True if looping == 0x01 else False
        
    def pack(self, *args):
        pass


# Enums for Srt0
Texture0 = 0x01
Texture1 = 0x02
Texture2 = 0x04
Texture3 = 0x08
Texture4 = 0x10
Texture5 = 0x20
Texture6 = 0x40
Texture7 = 0x80

Indirect0 = 0x01
Indirect1 = 0x02
Indirect2 = 0x04

class TextureAnimDataEntry:
    def __init__(self):
        self.animationTypeCode = 0
        self.unk10to31 = False
        self.yFixed = False
        self.xFixed = False
        self.rotationFixed = False
        self.scaleFixed = False
        self.unknownFixed = False
        self.hasUnknown = False
        self.hasTranslation = False
        self.hasRotation = False
        self.hasScale = False
        self.unknownBit = False

        self.unknown = 0
        self.scale = 0
        self.rotation = 0
        self.translationX = 0
        self.translationY = 0


    def unpack(self, data):
        self.animationTypeCode = Struct(">I").unpack(data[:0x4])[0]
        self.unk10to31 = self.animationTypeCode >> 0xA
        self.yFixed = True if self.animationTypeCode & 0x200 else False
        self.xFixed = True if self.animationTypeCode & 0x100 else False
        self.rotationFixed = True if self.animationTypeCode & 0x80 else False
        self.scaleFixed = True if self.animationTypeCode & 0x40 else False
        self.unknownFixed = True if self.animationTypeCode & 0x20 else False
        self.hasUnknown = True if self.animationTypeCode & 0x10 else False
        self.hasTranslation = True if self.animationTypeCode & 0x8 else False
        self.hasRotation = True if self.animationTypeCode & 0x4 else False
        self.hasScale = True if self.animationTypeCode & 0x2 else False
        self.unknownBit = True if self.animationTypeCode & 0x1 else False

        print(self.animationTypeCode)
        print(self.unk10to31)
        print(self.yFixed)
        print(self.xFixed)
        print(self.rotationFixed)
        print(self.scaleFixed)
        print(self.unknownFixed)
        print(self.hasUnknown)
        print(self.hasTranslation)
        print(self.hasRotation)
        print(self.hasScale)
        print(self.unknown)

    def pack(self):
        pass

class TextureAnimData:
    def __init__(self):
        self.nameOffset = 0
        self.name = ""
        self.m = 0
        self.unk0 = 0
        self.entryOffsets = []
        self.entries = []

    def unpack(self, data):
        self.nameOffset, self.m, self.unk0 = Struct(">III").unpack(data[0x00:0x0C])
        nameLength = data[self.nameOffset - 1]
        data[self.nameOffset:self.nameOffset + nameLength].decode("utf-8")
        for i in range(0, self.m):
            self.entryOffsets.append(Struct(">I").unpack(data[0x0C + i * 4:0x10 + i * 4])[0])
            entry = TextureAnimDataEntry()
            entry.unpack(data[self.entryOffsets[i]:])
            self.entries.append(entry)
        print(self.nameOffset)
        print(self.name)
        print(self.m)
        print(self.unk0)
        print(self.entryOffsets)
        print(self.entries)

    def pack(self, *args):
        pass

class Srt0Section0:
    def __init__(self):
        self.indexGroup = None
        self.texAnimDatas = []
        
    def unpack(self, data):
        self.indexGroup = BRRESIndexGroup()
        self.indexGroup.unpack(data)
        for i in range(0, self.indexGroup.n_entries):
            newTexAnimData = TextureAnimData()
            newTexAnimData.unpack(data[self.indexGroup.brres_entries[i].data_offset:])
            self.texAnimDatas.append(newTexAnimData)
        
    def pack(self, *args):
        pass

class Srt0Section1:

    # currently unknown
    def unpack(self, data):
        pass

    # currently unknown
    def pack(self, data):
        pass



class Srt0(SubSection):
    TAG = 'SRT0'
    EXTENSION = 'srt0'

    def __init__(self, name, parent):
        super(Srt0, self).__init__(name, parent)
        self.subHeader = None
        self.section0 = None
        self.section1 = None
        self.animations = []
        self.framecount = 1
        self.loop = True
        self.scaling_rule = 0

    def unpack(self, data):
        super().unpackSubSectionHeader(data)
        self.subHeader = Srt0Header()
        self.subHeader.unpack(data[0x14+self.header.n*4:0x24+self.header.n*4])
        if self.header.n == 1:
            #just section0
            self.section0 = Srt0Section0()
            self.section0.unpack(data[self.header.sectionOffsets[0]:])
        elif self.header.n == 2:
            # section0 and section1
            self.section0 = Srt0Section0()
            self.section0.unpack(data[self.header.sectionOffsets[0]:])
            self.section1 = Srt0Section1()
            self.section1.unpack(data[self.header.sectionOffsets[1]:])
        print("Srt unpacked")

    def pack(self):
        pass