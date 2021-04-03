from subSections.SubSection import SubSection
from struct import Struct


class Scn0Header:
    def __init__(self):
        self.unk0 = 0
        self.unk1 = 0
        self.frames = 0
        self.specularLightCount = 0
        self.looping = False
        self.sectionCounts = [0, 0, 0, 0, 0, 0]
        
    def unpack(self, data):
        self.unk0, self.unk1, self.frames, self.specularLightCount, looping = Struct(">IIIHH").unpack(data)
        self.looping = True if looping == 0x01 else False
        self.sectionCounts = list(Struct(">HHHHHH").unpack(data[0x10:]))
        
    def pack(self, *args):
        pass


class Scn0(SubSection):
    TAG = 'SCN0'
    EXTENSION = 'scn0'

    def __init__(self, item, parent):
        super(Scn0, self).__init__(item, parent)
        self.animations = []
        self.framecount = 1
        self.loop = True
        self.scaling_rule = 0

    def unpack(self, data):
        pass

    def pack(self):
        pass