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
        name = Struct(">4s").unpack(data[:4])[0]
        length = Struct(">I").unpack(data[4:8])[0]
        version = Struct(">I").unpack(data[8:12])[0]
        offsetToBress = Struct(">i").unpack(data[12:16])[0]     #this is a negative value
        if version == 1 or version == 3:
            sectionOffset = Struct(">I").unpack(data[16:20])[0]
            header = Tex0Header()
            header.unpack(data[0x18:0x34])
            
            decoder = getDecoder(header.format)
            decoder = decoder(data[sectionOffset:], header.width, header.height)
            newdata = decoder.run()
            img = QImage(newdata, header.width, header.height, 4 * header.width, QImage.Format_ARGB32)
        
            self.images.append(img)
        
        elif version == 2:                                                                                              #Untested❗️
            sectionOffset, sectionOffset2 = Struct(">II").unpack(data[16:24])
            header = Tex0Header()
            header.unpack(data[0x1C:0x38])

            decoder = getDecoder(header.format)
            decoder = decoder(data[sectionOffset:], header.width, header.height)
            newdata = decoder.run()
            img = QImage(newdata, header.width, header.height, 4 * header.width, QImage.Format_ARGB32)
            
            header2 = Tex0Header()
            header2.unpack(data[0x38:0x54])
            
            decoder = decoder(data[sectionOffset2:], header2.width, header2.height)
            newdata = decoder.run()
            img2 = QImage(newdata, header.width, header.height, 4 * header.width, QImage.Format_ARGB32)
            
            self.images.extend([img, img2])
        
        else:
            raise ValueError('Unrecognized version')
        
        print("\nname: {}\nlength: {}\nversion: {}\noffsetToBrres: {}\nsectionOffset: {}\n".format(name, length, version, offsetToBress, sectionOffset))
        
        
        

    def pack(self):
        pass
