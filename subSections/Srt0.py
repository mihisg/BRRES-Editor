from subSections.SubSection import SubSection
from struct import Struct


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


class Srt0Section0Material:
    def __init__(self):
        self.nameOffset = 0
        self.name = ""
        self.m = 0
        self.unk0 = 0
        self.entryOffsets = []
        self.entries = []
        
        
    def unpack(self, data):
        self.nameOffset, self.m, self.unk0 = Struct(">IHHII").unpack(data[0x00:0x0C])
        for i in range(0, self.m):
            self.entryOffsets.append(Struct(">I").unpack(data[0x0C + i*4:0x10 + i*4]))
            entry = Srt0Section0MaterialEntry()
            entry.unpack(data[self.entryOffsets[i]:])
            entries.append(entry)

        
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

class Srt0Section0MaterialEntry:
    def __init__(self):
        self.animationType = 0
        self.animationData = []
        
    def unpack(self, data):
        print(data[:0x10])
        pass#self.

    def pack(self, *args):
        pass


class Srt0Section0MaterialEntryAnimation:
    def __init__(self):
        self.unk0 = 0
        
    def unpack(self, data):
        pass

    def pack(self, *args):
        pass


class Srt0Section0:
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



class Srt0(SubSection):
    TAG = 'SRT0'
    EXTENSION = 'srt0'

    def __init__(self, name, parent):
        super(Srt0, self).__init__(name, parent)
        self.animations = []
        self.framecount = 1
        self.loop = True
        self.scaling_rule = 0

    def unpack(self, data):
        super().unpackSubSectionHeader(data)
        subHeader = Srt0Header()
        subHeader.unpack(data[0x14+self.header.n*4:0x24+self.header.n*4])

    def pack(self):
        pass