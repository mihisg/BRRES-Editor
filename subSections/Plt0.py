from subSections.SubSection import SubSection
from subSections.TPLLib import *
from struct import Struct



class Plt0Header:
    def __init__(self):
        self.format = 0
        self.colors = 0
        
    def unpack(self, data):
        self.format, self.colors = Struct(">HH").unpack(data) #followed by lot's of unknown values of hopefully fixed size ...
        
    def pack(self, *args):
        pass



class Plt0(SubSection):
    """
    PLT0-subfile of a brres, represents palettes for Tex0 files
    """
    
    TAG = 'PLT0'
    EXTENSION = 'plt0'
    
    def __init__(self, item, parent):
        super(Plt0, self).__init__(item, parent)
        self.palette = []
    
    def unpack(self, data):
        print(len(data))
        super().unpackSubSectionHeader(data)
        subHeader = Plt0Header()
        subHeader.unpack(data[0x1A:0x1E])
        if subHeader.format == 0:
            self.unpackIA8(data, subHeader.colors)
        elif subHeader.format == 1:
            self.unpackRGB565(data, subHeader.colors)
        elif subHeader.format == 2:
            self.unpackRGB5A3(data, subHeader.colors)
        else: raise TypeError("This palette type isn't known to exist!")
    
    
    def unpackIA8(self, data, colors):
        tex = data[0x40:0x40+colors*2]
        for i in range(0, colors*2, 2):
            alpha = tex[i]
            newpixel = tex[i+1]
            self.palette.append([newpixel, newpixel, newpixel, alpha])
        #print(self.palette)

    
    def unpackRGB565(self, data, colors):
        tex = data[0x40:0x40+colors*2]
        for i in range(0, colors*2, 2):
            blue5 = tex[i + 1] & 0x1F
            blue = blue5 << 3 | blue5 >> 2

            greenB = (tex[i + 1] >> 5)
            greenT = (tex[i] & 0x7)
            green = greenT << 5 | greenB << 2 | greenT >> 1

            red5 = tex[i] >> 3
            red = red5 << 3 | red5 >> 2

            alpha = 0xFF
            self.palette.append([blue, green, red, alpha])
        #print(self.palette)
    
    
    def unpackRGB5A3(self, data, colors):
        tex = data[0x40:0x40+colors*2]
        for i in range(0, colors*2, 2):
            newpixel = (tex[i] << 8) | tex[i+1]
            newpixel = int(newpixel)

            if newpixel & 0x8000: # RGB555
                blue5 = (newpixel >> 10) & 0x1F
                green5 = (newpixel >> 5) & 0x1F
                red5 = newpixel & 0x1F
                blue = blue5 << 3 | blue5 >> 2
                green = green5 << 3 | green5 >> 2
                red = red5 << 3 | red5 >> 2
                alpha = 0xFF

            else: # RGB5A3
                alpha3 = newpixel >> 12
                blue4 = (newpixel >> 8) & 0xF
                green4 = (newpixel >> 4) & 0xF
                red4 = newpixel & 0xF
                alpha = (alpha3 << 5) | (alpha3 << 2) | (alpha3 >> 1)
                blue = blue4 * 17
                green = green4 * 17
                red = red4 * 17

            self.palette.append([red, green, blue, alpha])
        #print(self.palette)

    
    def pack(self):
        pass