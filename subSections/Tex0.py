from subSections.SubSection import SubSection
from struct import Struct

class Tex0(SubSection):
    """
    TEX0-subfile of a brres, represents images and textures
    """

    TAG = 'TEX0'
    EXTENSION = 'tex0'
    FORMATS = {0: 'I4', 1: 'I8', 2: 'IA4', 3: 'IA8',
               4: 'RGB565', 5: 'RGB5A3', 6: 'RGBA32',
               8: 'C4', 9: 'C8', 10: 'C14X2', 14: 'CMPR'}

    def __init__(self, name, parent):
        super(Tex0, self).__init__(name, parent)
        self.animations = []
        self.framecount = 1
        self.loop = True
        self.scaling_rule = 0

    def unpack(self, data):
        super()._unpack(data, {1: 1, 2: 2, 3: 1})

    def pack(self):
        pass
