from subSections.SubSection import SubSection
from subSections.TPLLib import *
from struct import Struct
from PyQt5.QtGui import QImage

class Tex0Header:
    def __init__(self):
        self.unk0 = 0
        self.width = 0
        self.height = 0
        self.format = 0
        self.numberOfImages = 0
        self.unk1 = 0
        self.numberOfMipmaps = 0 #(numberOfImages -1)
        self.unk2 = 0
        
    def unpack(self, data):
        self.unk0, self.width, self.height, self.format, self.numberOfImages, self.unk1, self.numberOfMipmaps, self.unk2 = Struct(">IHHIIIII").unpack(data)
        #print("width: {}\nheight: {}\nformat: {}\nnumberOfImages: {}\n".format(self.width, self.height, self.format, self.numberOfImages))
        
    def pack(self, *args):
        pass



class Tex0(SubSection):
    """
    TEX0-subfile of a brres, represents images and textures
    """

    TAG = 'TEX0'
    EXTENSION = 'tex0'
    FORMATS = {0: 'I4', 1: 'I8', 2: 'IA4', 3: 'IA8',
               4: 'RGB565', 5: 'RGB5A3', 6: 'RGBA32',
               8: 'C4', 9: 'C8', 10: 'C14X2', 14: 'CMPR'}     #is C14X2 really needed -> BrawlCrate doesn't contain it

    def __init__(self, name, parent):
        super(Tex0, self).__init__(name, parent)
        self.images = []


    def unpack(self, data):
        super().unpackSubSectionHeader(data)
        subHeader = Tex0Header()
        subHeader.unpack(data[0x14+self.header.n*4:0x30+self.header.n*4])
        for offset in self.header.sectionOffsets:
            decoder = getDecoder(subHeader.format)
            decoder = decoder(data[offset:], subHeader.width, subHeader.height)
            newdata = decoder.run()
            img = QImage(newdata, subHeader.width, subHeader.height, 4 * subHeader.width, QImage.Format_ARGB32)
        
            self.images.append(img)


    def pack(self):
        pass
