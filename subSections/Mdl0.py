from subSections.SubSection import SubSection
from struct import Struct


class Vec3D:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z


class Mdl0Header:
    def __init__(self):
        self.headerLength = 0x40
        self.headerOffset = 0
        self.unk0 = 0
        self.unk1 = 0
        self.vertices = 0
        self.faces = 0
        self.unk2 = 0
        self.bones = 0
        self.unk3 = 0x01000000
        self.boneTableOffset = 0
        self.min = Vec3D()
        self.max = Vec3D()
        
    def unpack(self, data):
        self.headerLength, self.headerOffset, self.unk0, self.unk1, self.vertices, self.faces, self.unk2, self.bones, self.unk3, self.boneTableOffset = Struct(">IIIIIIIIII").unpack(data[:0x28])
        self.min.x, self.min.y, self.min.z, self.max.x, self.max.y, self.max.z = Struct(">ffffff").unpack(data[0x28:0x40])
        """
        print(self.headerLength)
        print(self.headerOffset)
        print(self.unk0)
        print(self.unk1)
        print(self.vertices)
        print(self.faces)
        print(self.unk2)
        print(self.bones)
        print(self.unk3)
        print(self.boneTableOffset)
        print(self.min.x)
        print(self.min.y)
        print(self.min.z)
        print(self.max.x)
        print(self.max.y)
        print(self.max.z)
        """

    def pack(self, *args):
        pass


class Mdl0(SubSection):
    TAG = 'MDL0'
    EXTENSION = 'mdl0'

    def __init__(self, item, parent):
        super(Mdl0, self).__init__(item, parent)
        self.animations = []
        self.framecount = 1
        self.loop = True
        self.scaling_rule = 0

    def unpack(self, data):
        super().unpackSubSectionHeader(data)
        subHeader = Mdl0Header()
        subHeader.unpack(data[0x14 + self.header.n * 4:0x54 + self.header.n * 4])

    def pack(self):
        pass