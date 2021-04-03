from subSections.SubSection import SubSection
from struct import Struct


class Clr0Header:
    def __init__(self):
        self.frames = 0
        self.entries = 0
        self.unk0 = 0
        self.looping = False
        self.relativeOffset = 0
        
    def unpack(self, data):
        padding, self.frames, self.entries, self.unk0, looping, self.relativeOffset = Struct(">IHHHHI").unpack(data)
        self.looping = True if looping == 0x01 else False
        
    def pack(self, *args):
        pass


class Clr0(SubSection):
    TAG = 'CLR0'
    EXTENSION = 'clr0'

    def __init__(self, item, parent):
        super(Clr0, self).__init__(item, parent)
        self.animations = []
        self.framecount = 1
        self.loop = True
        self.scaling_rule = 0

    def unpack(self, data):
        pass

    def pack(self):
        pass