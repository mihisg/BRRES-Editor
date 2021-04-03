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


# enums for direct and indirect textures
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

class KeyFrameList:
    def __init__(self):
        self.frameCount = 0
        self.unknown = 0
        self.frameScale = 0.0
        self.frames = []

    def unpack(self, data):
        self.frameCount, self.unknown, self.frameScale = Struct(">HHf").unpack(data[0:8])
        for i in range(self.frameCount):
            tangent, value, index = Struct("> fff").unpack(data[0x8 + i * 0xC: 0x14 + i * 0xC])
            self.frames.append([tangent, value, index])
        print(f"KeyFrameList frameCount: {self.frameCount}")
        print(f"KeyFrameList unknown: {self.unknown}")
        print(f"KeyFrameList frameScale: {self.frameScale}")
        print(f"KeyFrameList frames: {self.frames}")

class Srt0TextureEntry:
    def __init__(self):
        self.animationTypeCode = 0
        self.scaleDefault = 0
        self.rotationDefault = 0
        self.translationDefault = 0
        self.scaleIsotropic = 0
        self.xScaleFixed = 0
        self.yScaleFixed = 0
        self.rotationFixed = 0
        self.xTranslationFixed = 0
        self.yTranslationFixed = 0
        self.unknownBit = 0

        self.unknown = 0
        self.xScale = []
        self.yScale = []
        self.rotation = []
        self.xTranslation = []
        self.yTranslation = []

    def parseAnimationCode(self, code):
        self.unknownBit = code & 1
        code >>= 1
        flags = []
        for i in range(9):
            flags.append(code & 1)
            code >>= 1
        self.scaleDefault = flags[0]
        self.rotationDefault = flags[1]
        self.translationDefault = flags[2]
        self.scaleIsotropic = flags[3]
        self.xScaleFixed = flags[4]
        self.yScaleFixed = flags[5]
        self.rotationFixed = flags[6]
        self.xTranslationFixed = flags[7]
        self.yTranslationFixed = flags[8]
        self.unknown = code

    def unpackKeyFrameList(self, data):
        newList = KeyFrameList()
        newList.unpack(data)
        return newList

    def unpackScale(self, data):
        if self.scaleDefault:
            self.xScale.append(1.0)
            self.yScale.append(1.0)
            return 0
        elif self.scaleIsotropic:
            if self.xScaleFixed:
                scale = Struct("> f").unpack(data[:0x4])[0]
                self.xScale.append(scale)
                self.yScale.append(scale)
            else:
                scalePointer = Struct("> I").unpack(data[:0x4])[0]
                keyFrameList = self.unpackKeyFrameList(data[scalePointer:])
                self.xScale.append(keyFrameList)
                self.yScale.append(keyFrameList)
            return 0x4
        else:
            if self.xScaleFixed:
                scale = Struct("> f").unpack(data[:0x4])[0]
                self.xScale.append(scale)
            else:
                scalePointer = Struct("> I").unpack(data[:0x4])[0]
                keyFrameList = self.unpackKeyFrameList(data[scalePointer:])
                self.xScale.append(keyFrameList)
            if self.yScaleFixed:
                scale = Struct("> f").unpack(data[0x4:0x8])[0]
                self.yScale.append(scale)
            else:
                scalePointer = Struct("> I").unpack(data[0x4:0x8])[0]
                keyFrameList = self.unpackKeyFrameList(data[scalePointer:])
                self.yScale.append(keyFrameList)
            return 0x8

    def unpackRotation(self, data):
        if not self.rotationDefault:
            if self.rotationFixed:
                rot = Struct(">f").unpack(data[:0x4])[0]
                self.rotation.append(rot)
            else:
                rotPointer = Struct(">I").unpack(data[:0x4])[0]
                keyFrameList = self.unpackKeyFrameList(data[rotPointer:])
                self.yScale.append(keyFrameList)
            return 0x4
        else:
            self.rotation.append(0.0)
            return 0x0

    def unpackTranslation(self, data):
        if self.translationDefault:
            self.xTranslation.append(0.0)
            self.yTranslation.append(0.0)
        else:
            if self.xTranslationFixed:
                xTrans = Struct(">f").unpack(data[:0x4])[0]
                self.xTranslation.append(xTrans)
            else:
                transPointer = Struct(">I").unpack(data[:0x4])[0]
                keyFrameList = self.unpackKeyFrameList(data[transPointer:])
                self.xTranslation.append(keyFrameList)
            if self.yTranslationFixed:
                yTrans = Struct(">f").unpack(data[0x4:0x8])[0]
                self.yTranslation.append(yTrans)
            else:
                transPointer = Struct(">I").unpack(data[0x4:0x8])[0]
                keyFrameList = self.unpackKeyFrameList(data[transPointer:])
                self.yTranslation.append(keyFrameList)

    def unpack(self, data):
        self.animationTypeCode = Struct(">I").unpack(data[:0x4])[0]
        self.parseAnimationCode(self.animationTypeCode)
        scaleOffset = self.unpackScale(data[0x4:])
        rotationOffset = self.unpackRotation(data[0x4 + scaleOffset:])
        self.unpackTranslation(data[0x4 + scaleOffset + rotationOffset:])

        print(f"Texture Entry animationCode: {self.animationTypeCode}")
        print(f"Texture Entry unknownBit: {self.unknownBit}")
        print(f"Texture Entry scaleDefault: {self.scaleDefault}")
        print(f"Texture Entry rotationDefault: {self.rotationDefault}")
        print(f"Texture Entry translationDefault: {self.translationDefault}")
        print(f"Texture Entry scaleIsotropic: {self.scaleIsotropic}")
        print(f"Texture Entry xScaleFixed: {self.xScaleFixed}")
        print(f"Texture Entry yScaleFixed: {self.yScaleFixed}")
        print(f"Texture Entry rotationFixed: {self.rotationFixed}")
        print(f"Texture Entry xTranslationFixed: {self.xTranslationFixed}")
        print(f"Texture Entry yTranslationFixed: {self.yTranslationFixed}")
        print(f"Texture Entry unknown: {self.unknown}")
        print(f"Texture Entry xScale: {self.xScale}")
        print(f"Texture Entry yScale: {self.yScale}")
        print(f"Texture Entry rotation: {self.rotation}")
        print(f"Texture Entry xTranslation: {self.xTranslation}")
        print(f"Texture Entry yTranslation: {self.yTranslation}")

    def pack(self):
        pass

class Srt0Material:
    def __init__(self):
        self.nameOffset = 0
        self.name = ""
        self.m = 0              #direct textures (see enums above)
        self.w = 0              #indirect textures (see enums above)
        self.entryOffsets = []
        self.entries = []
        self.texEnabled = [False, False, False, False, False, False, False, False, False, False, False] #direct and indirect textures

    def unpack(self, data):
        self.nameOffset, self.m, self.w = Struct(">III").unpack(data[0x00:0x0C])
        nameLength = data[self.nameOffset - 1]
        self.name = data[self.nameOffset:self.nameOffset + nameLength].decode("utf-8")
        bit = 1
        count = 0
        for i in range(8):
            if bit & self.m:
                self.texEnabled[i] = True
                self.entryOffsets.append(Struct(">I").unpack(data[0x0C + count * 4:0x10 + count * 4])[0])
                entry = Srt0TextureEntry()
                entry.unpack(data[self.entryOffsets[count]:])
                self.entries.append(entry)
                count += 1
            bit <<= 1

        bit = 1
        for i in range(3):
            if bit & self.w:
                self.texEnabled[8+i] = True
                self.entryOffsets.append(Struct(">I").unpack(data[0x0C + count * 4:0x10 + count * 4])[0])
                entry = Srt0TextureEntry()
                entry.unpack(data[self.entryOffsets[count]:])
                self.entries.append(entry)
                count += 1
            bit <<= 1

        print(f"Material name offset: ${self.nameOffset}")
        print(f"Material name: ${self.name}")
        print(f"Material texture count: ${self.m}")
        print(f"Material ind texture count: ${self.w}")
        print(f"Material entry offsets: ${self.entryOffsets}")
        print(f"Material entries: ${self.entries}")
        print(f"Material texEnabled: ${self.texEnabled}")

    def pack(self, *args):
        pass

class Srt0Section0:
    def __init__(self):
        self.indexGroup = None
        self.srt0materials = []
        
    def unpack(self, data):
        self.indexGroup = BRRESIndexGroup()
        self.indexGroup.unpack(data)
        for i in range(0, self.indexGroup.n_entries):
            newMaterial = Srt0Material()
            newMaterial.unpack(data[self.indexGroup.brres_entries[i].data_offset:])
            self.srt0materials.append(newMaterial)
        
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

    def unpack(self, data):
        super().unpackSubSectionHeader(data)
        self.subHeader = Srt0Header()
        self.subHeader.unpack(data[0x14+self.header.n*4:0x24+self.header.n*4])
        # just section0
        self.section0 = Srt0Section0()
        self.section0.unpack(data[self.header.sectionOffsets[0]:])
        if self.header.n == 2:
            # section0 and section1
            self.section1 = Srt0Section1()
            self.section1.unpack(data[self.header.sectionOffsets[1]:])
        print("Srt unpacked")

    def pack(self):
        pass