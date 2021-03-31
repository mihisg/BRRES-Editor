from subSections.SubSection import SubSection
from struct import Struct


class Shp0(SubSection):
    TAG = 'SHP0'
    EXTENSION = 'shp0'

    def __init__(self, name, parent):
        super(Shp0, self).__init__(name, parent)
        self.animations = []
        self.framecount = 1
        self.loop = True
        self.scaling_rule = 0

    def unpack(self, data):
        pass

    def pack(self):
        pass