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
        pass

    def pack(self):
        pass