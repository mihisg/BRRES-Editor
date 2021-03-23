from brres.BRRESIndexGroup import *


class BRRESRootSection:
    """
    Class for the root section of a brres archive
    """

    def __init__(self):
        self.tag = 0
        self.size = 0

        self.first_group = BRRESIndexGroup()

        self.subGroups = []

    def unpack(self, data):
        rootUnpacker = Struct("> 4s I")
        self.tag, self.size = rootUnpacker.unpack(data[0x0:0x8])

        print("Root unpacked!")
        print(f"magic: {self.tag}")
        print(f"length: {self.size}")

        self.first_group.unpack(data[0x8:])

        for i in range(0, self.first_group.n_entries):
            newGroup = BRRESIndexGroup()
            newGroup.unpack(data[self.first_group.brres_entries[i].data_offset + 0x8:])
            self.subGroups.append(newGroup)

    def pack(self):
        rootPacker = Struct("> 4s I")
        data = []
        data.append(rootPacker.pack(self.tag, self.size))
        data.append(self.first_group.pack())

        for i in self.subGroups:
            data.append(i.pack())

        return data

    def calculateSize(self):
        length = 0x8
        length += self.first_group.calculateSize()
        for i in self.subGroups:
            length += i.calculateSize()
        return length
