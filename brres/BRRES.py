from brres.BRRESHeader import *
from brres.BRRESRootSection import *
from brres.BRRESIndexGroup import *
from brres.FolderFile import *


class BRRES:

    TAG = b'bres'

    def __init__(self):

        self.header = BRRESHeader()
        self.root = BRRESRootSection()
        self.folders = []
        self.mdl0 = []
        self.tex0 = []
        self.srt0 = []
        self.chr0 = []
        self.pat0 = []
        self.clr0 = []
        self.shp0 = []
        self.scn0 = []
        self.zeroes = []

    def unpack(self, data):
        headerData = data[0:0x10]
        self.header.unpack(headerData)

        rootData = data[0x10:]
        self.root.unpack(rootData)

        offsetToFirstSubSection = 0x0
        zero = Struct(">s").unpack(data[0x10 + self.root.size + offsetToFirstSubSection: 0x10 + self.root.size + 0x1 + offsetToFirstSubSection])
        while zero == (b'\x00',):
            self.zeroes.append(zero)
            offsetToFirstSubSection += 1
            test = Struct(">s")
            zero = test.unpack(data[0x10 + self.root.size + offsetToFirstSubSection: 0x10 + self.root.size + 0x1 + offsetToFirstSubSection])

        for i in range(1, self.header.n_sections):
            test = Struct("> 4s")
            name = test.unpack(data[0x10 + self.root.size + offsetToFirstSubSection:0x10 + self.root.size + 0x4 + offsetToFirstSubSection])
            print(name)
            print(len(self.zeroes))
            pass  # load all sections

        for entry in self.root.first_group.brres_entries:
            new = Folder(entry.name)
            self.folders.append(new)

        for i in self.folders:
            print(i.name)

    def pack(self):
        data = []
        data.append(self.header.pack())
        data.append(self.root.pack())

        for i in range(0, self.header.n_sections):
            pass # pack all sections

        return data
