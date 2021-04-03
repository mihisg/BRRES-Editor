from subSections.SubSection import SubSection
from struct import Struct



class Pat0HeaderV4:
    def __init__(self):
        self.unk0 = 0
        self.unk1 = 0
        self.framecount = 0
        self.n = 0
        self.n_str = 0
        self.unk2 = 0
        self.unk3 = 0
        self.looping = False


    def unpack(self, data):
        self.unk0, self.unk1, self.framecount, self.n, self.n_str, self.unk2, self.unk3, looping = Struct(">HHHHHHHH").unpack(data)
        self.looping = True if looping == 0x01 else False


    def pack(self, *args):
        pass



class Pat0V4Section0BaseHeader:
    def __init__(self):
        self.head_size = 0
        self.unk0 = 0
        self.n = 0
        self.unk1 = 0xFFFF
        self.unk2 = 0
        self.n_unk = 0                              #mostly same as n in MKW
        self.unk3 = 0
        self.unk4 = 0
        self.unk5 = 0
        self.unk6 = 0
        self.unk7 = 0
        self.baseData = []


    def unpack(self, data):
        self.head_size, self.unk0, self.n, self.unk1, self.unk2, self.n_unk, self.unk3, self.unk4, self.unk5, self.unk6, self.unk7 = Struct(">IHHHHHHHHHH").unpack(data[0x00:0x18])
        for i in range(0, self.n):
            baseData = Pat0V4Section0BaseData()
            baseData.unpack(data[0x18 + i*0x10:0x28 + i*0x10])
            self.baseData.append(baseData)


    def pack(self, *args):
        pass


class Pat0V4Section0BaseData:
    def __init__(self):
        self.unk0 = 0x19                            #values between 0x19 and 0x96 in MKW
        self.unk1 = 0
        self.unk2 = 0                               #Values between 0 and 2 in MKW. Value is only >0, if N_BASE >1.
        self.unk3 = 1                               #1 or 2 in MKW. Value is never the same as the value before (offset 0x04) and only 2, if N_BASE >1.
        self.nameOffset = 0                         #Offset (relative to beginning of this Base Header) into the string pool.
        self.referenceHeaderOffset = 0              #Offset (relative to beginning of this Base Header) to the related Reference Header.


    def unpack(self, data):
        self.unk0, self.unk1, self.unk2, self.unk3, self.nameOffset, self.referenceHeaderOffset  = Struct(">HHHHII").unpack(data)


    def pack(self, *args):
        pass


class Pat0(SubSection):
    TAG = 'PAT0'
    EXTENSION = 'pat0'

    def __init__(self, item, parent):
        super(Pat0, self).__init__(item, parent)
        
    def unpack(self, data):
        super().unpackSubSectionHeader(data)
        
        subHeader = Pat0HeaderV4()
        subHeader.unpack(data[0x14+self.header.n*4:0x24+self.header.n*4])
        
        section0BaseHeader = Pat0V4Section0BaseHeader()
        section0BaseHeader.unpack(data[0x24+self.header.n*4:])
        print(section0BaseHeader.n)


    def pack(self):
        pass