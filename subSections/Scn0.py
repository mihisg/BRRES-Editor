from subSections.SubSection import SubSection
from struct import Struct


class Scn0(SubSection):
    TAG = 'SCN0'
    EXTENSION = 'scn0'

    def __init__(self, name, parent):
        super(Scn0, self).__init__(name, parent)
        self.animations = []
        self.framecount = 1
        self.loop = True
        self.scaling_rule = 0

    def unpack(self, data):
        pass

    def pack(self):
        pass