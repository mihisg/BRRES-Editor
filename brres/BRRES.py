from brres.BRRESHeader import *
from brres.BRRESRootSection import *
from subSections.Chr0 import Chr0
from subSections.Clr0 import Clr0
from subSections.Mdl0 import Mdl0
from subSections.Pat0 import Pat0
from subSections.Scn0 import Scn0
from subSections.Shp0 import Shp0
from subSections.Srt0 import Srt0
from subSections.Tex0 import Tex0


class BRRES:
    TAG = b'bres'

    def __init__(self):

        self.header = BRRESHeader()
        self.root = BRRESRootSection()
        self.folders = {}
        self.mdl0 = {}
        self.tex0 = {}
        self.srt0 = {}
        self.chr0 = {}
        self.pat0 = {}
        self.clr0 = {}
        self.shp0 = {}
        self.scn0 = {}
        self.zeroes = []

    def unpack(self, data):
        self.unpackHeader(data[0:0x10])
        self.unpackRoot(data[0x10:])

        offsetToFirstSubSection = self.weirdZeroes(data)
        self.generateFoldersAndFiles()

        self.unpackSubSections(data, offsetToFirstSubSection + 0x10)

    def unpackHeader(self, data):
        self.header.unpack(data)
        if self.header.tag != self.TAG:
            TypeError("This is no .brres file! Please try again. No data was changed")

    def unpackRoot(self, data):
        self.root.unpack(data)

    def weirdZeroes(self, data):
        offsetToFirstSubSection = 0x0
        zero = Struct(">s").unpack(data[0x10 + self.root.size + offsetToFirstSubSection: 0x10 + self.root.size + 0x1 + offsetToFirstSubSection])
        while zero == (b'\x00',):
            self.zeroes.append(zero)
            offsetToFirstSubSection += 1
            test = Struct(">s")
            zero = test.unpack(data[0x10 + self.root.size + offsetToFirstSubSection: 0x10 + self.root.size + 0x1 + offsetToFirstSubSection])
        return offsetToFirstSubSection

    def generateFoldersAndFiles(self):
        for entry in range(0, self.root.first_group.n_entries):
            files = []
            for i in self.root.subGroups[entry].brres_entries:
                files.append(i.name)
            self.folders[self.root.first_group.brres_entries[entry].name] = files

    def unpackSubSections(self, data, offsetToSubSection):
        counters = [0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(1, self.header.n_sections):
            nameUnpacker = Struct("> 4s ")
            lengthUnpacker = Struct("> I")
            name = nameUnpacker.unpack(
                data[self.root.size + offsetToSubSection:self.root.size + 0x4 + offsetToSubSection])
            length = lengthUnpacker.unpack(
                data[self.root.size + offsetToSubSection + 0x4:self.root.size + 0x8 + offsetToSubSection])
            if name == (b'MDL0',):
                subfile = Mdl0(self.folders["3DModels(NW4R)"][counters[0]], self.folders["3DModels(NW4R)"])
                subfile.unpack(data[self.root.size + offsetToSubSection:])
                self.mdl0[subfile.name] = subfile
                counters[0] += 1
            elif name == (b'CHR0',):
                subfile = Chr0(self.folders["AnmChr(NW4R)"][counters[1]], self.folders["AnmChr(NW4R)"])
                subfile.unpack(data[self.root.size + offsetToSubSection:])
                self.chr0[subfile.name] = subfile
                counters[1] += 1
            elif name == (b'CLR0',):
                subfile = Clr0(self.folders["AnmClr(NW4R)"][counters[2]], self.folders["AnmClr(NW4R)"])
                subfile.unpack(data[self.root.size + offsetToSubSection:])
                self.clr0[subfile.name] = subfile
                counters[2] += 1
            elif name == (b'PAT0',):
                subfile = Pat0(self.folders["AnmTexPat(NW4R)"][counters[2]], self.folders["AnmTexPat(NW4R)"])
                subfile.unpack(data[self.root.size + offsetToSubSection:])
                self.pat0[subfile.name] = subfile
                counters[3] += 1
            elif name == (b'SCN0',):
                subfile = Scn0(self.folders["AnmScn(NW4R)"][counters[2]], self.folders["AnmScn(NW4R)"])
                subfile.unpack(data[self.root.size + offsetToSubSection:])
                self.scn0[subfile.name] = subfile
                counters[4] += 1
            elif name == (b'SHP0',):
                subfile = Shp0(self.folders["AnmShp(NW4R)"][counters[2]], self.folders["AnmShp(NW4R)"])
                subfile.unpack(data[self.root.size + offsetToSubSection:])
                self.shp0[subfile.name] = subfile
                counters[5] += 1
            elif name == (b'SRT0',):
                subfile = Srt0(self.folders["AnmTexSrt(NW4R)"][counters[2]], self.folders["AnmTexSrt(NW4R)"])
                subfile.unpack(data[self.root.size + offsetToSubSection:])
                self.srt0[subfile.name] = subfile
                counters[6] += 1
            elif name == (b'TEX0',):
                subfile = Tex0(self.folders["Textures(NW4R)"][counters[7]], self.folders["Textures(NW4R)"])
                subfile.unpack(data[self.root.size + offsetToSubSection:])
                self.tex0[subfile.name] = subfile
                counters[7] += 1
            else:
                TypeError(f"[ERROR]: This format is an unknown subfile and not supported: {name}")
                return

            offsetToSubSection += length[0]

    # TODO
    def pack(self):
        data = []
        data.append(self.header.pack())
        data.append(self.root.pack())

        for i in range(0, self.header.n_sections):
            pass  # pack all sections

        return data
