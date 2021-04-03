from struct import Struct


class SubSection:
    """
    Represents a brres-subsection, base class for mdl0, tex0, ...
    """

    class SubSectionHeader:
        def __init__(self):
            self.magic = 0
            self.size = 0
            self.version = 0
            self.outerOffset = 0
            self.sectionOffsets = []
            self.stringOffset = 0
            self.n = 0

    def __init__(self, item, parent):
        self.parent = parent
        self.item = item
        self.name = item.text()
        self.observers = []
        self.header = SubSection.SubSectionHeader()
        self.isModified = False
        self.readStart = 0
        self.readEnd = 0

    def unpackSubSectionHeader(self, data):
        header = SubSection.SubSectionHeader()
        header.magic, header.size, header.version, header.outerOffset = Struct(">4sIII").unpack(data[0x0:0x10])

        n = self.getNumberOfSections(header.magic, header.version)
        for i in range(0, n):
            header.sectionOffsets.append(Struct(">I").unpack(data[0x10 + i * 4:0x14 + i * 4])[0])

        if not n == 0: header.stringOffset = Struct(">I").unpack(data[0x10 + 4 * n:0x14 + 4 * n])[0]

        header.n = n

        self.header = header

        # print(self.header.magic)
        # print(self.header.size)
        # print(self.header.version)
        # print(self.header.outerOffset)
        # print(self.header.sectionOffsets)
        # print(self.header.stringOffset)

    def getNumberOfSections(self, magic, version):
        if magic == b'CHR0':
            if version == 3:
                return 1
            elif version == 5:
                return 2

        elif magic == b'CLR0':
            if version == 4: return 2

        elif magic == b'MDL0':
            if version == 8:
                return 11
            elif version == 11:
                return 14

        elif magic == b'PAT0':
            if version == 4: return 6
            print(version)
        elif magic == b'SCN0':
            if version == 4:
                return 6
            elif version == 5:
                return 7

        elif magic == b'SHP0':
            if version == 4: return 3

        elif magic == b'SRT0':
            if version == 4:
                return 1
            elif version == 5:
                return 2

        elif magic == b'TEX0':
            if version == 1:
                return 1
            elif version == 2:
                return 2
            elif version == 3:
                return 1

        elif magic == b'PLT0':
            return 1

        return 0

    def _pack(self):
        pass
