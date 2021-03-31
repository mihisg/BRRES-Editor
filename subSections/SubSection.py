from struct import Struct

class SubSection:
    """
        Represents a brres-subsection, base class for mdl0, tex0, ...
    """

    class SubSectionHeader:
        def __init__(self):
            self.tag = 0
            self.size = 0
            self.versionNum = 0
            self.outerOffset = 0
            self.sectionOffsets = []
            self.stringOffset = 0

    @property
    def TAG(self):
        raise NotImplementedError()

    @property
    def EXTENSION(self):
        raise NotImplementedError()

    def __init__(self, name, parent):
        self.parent = parent
        self.name = name
        self.observers = []
        self.header = SubSection.SubSectionHeader()
        self.isModified = False

    def _unpack(self, data, section_table):
        header = SubSection.SubSectionHeader()
        header.tag, header.size, header.versionNum, header.outerOffset = Struct("> 4s I I I").unpack(data[0x0:0x10])
        extraOffset = 0x0
        for i in range(0, section_table[header.versionNum]):
            headerUnpacker2 = Struct("> I")
            header.sectionOffsets.append(hex(headerUnpacker2.unpack(data[0x10 + extraOffset:0x14 + extraOffset])[0]))
            extraOffset += 0x4

        header.stringOffset = hex(
        Struct("> I").unpack(data[0x14 + 0x4 * (section_table[header.versionNum] - 1):0x18 + 0x4 * (section_table[header.versionNum] - 1)])[0])

        self.header = header

        print(self.header.tag)
        print(self.header.size)
        print(self.header.versionNum)
        print(self.header.outerOffset)
        print(self.header.sectionOffsets)
        print(self.header.stringOffset)

    def _pack(self):
        pass

