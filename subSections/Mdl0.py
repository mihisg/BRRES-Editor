from subSections.SubSection import SubSection
from struct import Struct


class Mdl0(SubSection):
    TAG = 'CHR0'
    EXTENSION = 'chr0'

    def __init__(self, name, parent):
        super(Mdl0, self).__init__(name, parent)
        self.animations = []
        self.framecount = 1
        self.loop = True
        self.scaling_rule = 0

    def unpack(self, data):
        pass

    def pack(self):
        pass