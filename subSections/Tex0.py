from subSections.SubSection import SubSection
from subSections.TPLLib import *
from struct import Struct
try:
    from PyQt5.QtGui import QImage
except ImportError:
    from PySide2.QtGui import QImage

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
        name = Struct(">4s").unpack(data[:4])[0]
        length = Struct(">I").unpack(data[4:8])[0]
        version = Struct(">I").unpack(data[8:12])[0]
        offsetToBress = Struct(">i").unpack(data[12:16])[0]
        if version == 1 or version == 3:
            n = 1
            sectionOffset = Struct(">I").unpack(data[16:20])[0]
        elif version == 2:
            n = 2
            sectionOffset, sectionOffset2 = Struct(">II").unpack(data[16:24])
        else:
            raise ValueError('Unrecognized version')
        print("\nname: {}\nlength: {}\nversion: {}\noffsetToBrres: {}\n".format(name, length, version, offsetToBress))
        

    def pack(self):
        pass




