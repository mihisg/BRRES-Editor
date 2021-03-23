from subSections.SubSection import SubSection
from struct import Struct


class Srt0(SubSection):
    TAG = 'CHR0'
    EXTENSION = 'chr0'

    def __init__(self, name, parent):
        super(Srt0, self).__init__(name, parent)
        self.animations = []
        self.framecount = 1
        self.loop = True
        self.scaling_rule = 0

    def unpack(self, data):
        super()._unpack(data, {4: 1, 5: 2})

    def pack(self):
        pass