from subSections.SubSection import SubSection
from struct import Struct


class Mdl0(SubSection):
    TAG = 'MDL0'
    EXTENSION = 'mdl0'

    def __init__(self, name, parent):
        super(Mdl0, self).__init__(name, parent)
        self.animations = []
        self.framecount = 1
        self.loop = True
        self.scaling_rule = 0

    def unpack(self, data):
        super()._unpack(data, {8: 11, 11: 14})

    def pack(self):
        pass