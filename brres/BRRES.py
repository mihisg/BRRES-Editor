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
from subSections.Plt0 import Plt0
from subSections.Unk0 import Unk0


class BRRES:
    TAG = b'bres'

    def __init__(self):
        self.header = BRRESHeader()
        self.root = BRRESRootSection()
        self.folders = {}
        self.mdl0 = {}
        self.tex0 = {}
        self.plt0 = {}
        self.srt0 = {}
        self.chr0 = {}
        self.pat0 = {}
        self.clr0 = {}
        self.shp0 = {}
        self.scn0 = {}
        self.unk0 = {}
        self.zeroes = 0

    def unpack(self, data):
        self.header.unpack(data[0:0x10])
        if self.header.tag != self.TAG:
            TypeError("This is no .brres file! Please try again. No data was changed")
        self.root.unpack(data[0x10:])

        offsetToFirstSubSection = self.weirdZeroes(data)
        self.generateFoldersAndFiles()

        self.unpackSubSections(data, offsetToFirstSubSection + 0x10)

    def weirdZeroes(self, data):
        offsetToFirstSubSection = 0x0
        zero = Struct(">s").unpack(data[0x10 + self.root.size + offsetToFirstSubSection:0x10 + self.root.size + 0x1 + offsetToFirstSubSection])[0]
        while zero == b'\x00':
            self.zeroes += 1
            offsetToFirstSubSection += 1
            zero = Struct(">s").unpack(data[0x10 + self.root.size + offsetToFirstSubSection:0x10 + self.root.size + 0x1 + offsetToFirstSubSection])[0]
        return offsetToFirstSubSection

    def generateFoldersAndFiles(self):
        for entry in range(0, self.root.first_group.n_entries):
            files = []
            for i in self.root.subGroups[entry].brres_entries:
                files.append(i.name)
            self.folders[self.root.first_group.brres_entries[entry].name] = files

    def unpackSubSections(self, data, offsetToSubSection):
        counters = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(1, self.header.n_sections):
            name = Struct(">4s").unpack(
                data[self.root.size + offsetToSubSection:self.root.size + 0x4 + offsetToSubSection])[0]
            length = Struct(">I").unpack(
                data[self.root.size + offsetToSubSection + 0x4:self.root.size + 0x8 + offsetToSubSection])[0]
            if name == b'MDL0':
                subfile = Mdl0(self.folders["3DModels(NW4R)"][counters[0]], self.folders["3DModels(NW4R)"])
                subfile.unpack(data[self.root.size + offsetToSubSection:self.root.size + offsetToSubSection + length])  # @Mihi is this actually correct? Can't check it right now 😅😜
                self.mdl0[subfile.name] = subfile
                counters[0] += 1
            elif name == b'CHR0':
                subfile = Chr0(self.folders["AnmChr(NW4R)"][counters[1]], self.folders["AnmChr(NW4R)"])
                subfile.unpack(data[self.root.size + offsetToSubSection:self.root.size + offsetToSubSection + length])
                self.chr0[subfile.name] = subfile
                counters[1] += 1
            elif name == b'CLR0':
                subfile = Clr0(self.folders["AnmClr(NW4R)"][counters[2]], self.folders["AnmClr(NW4R)"])
                subfile.unpack(data[self.root.size + offsetToSubSection:self.root.size + offsetToSubSection + length])
                self.clr0[subfile.name] = subfile
                counters[2] += 1
            elif name == b'PAT0':
                subfile = Pat0(self.folders["AnmTexPat(NW4R)"][counters[2]], self.folders["AnmTexPat(NW4R)"])
                subfile.unpack(data[self.root.size + offsetToSubSection:self.root.size + offsetToSubSection + length])
                self.pat0[subfile.name] = subfile
                counters[3] += 1
            elif name == b'SCN0':
                subfile = Scn0(self.folders["AnmScn(NW4R)"][counters[2]], self.folders["AnmScn(NW4R)"])
                subfile.unpack(data[self.root.size + offsetToSubSection:self.root.size + offsetToSubSection + length])
                self.scn0[subfile.name] = subfile
                counters[4] += 1
            elif name == b'SHP0':
                subfile = Shp0(self.folders["AnmShp(NW4R)"][counters[2]], self.folders["AnmShp(NW4R)"])
                subfile.unpack(data[self.root.size + offsetToSubSection:self.root.size + offsetToSubSection + length])
                self.shp0[subfile.name] = subfile
                counters[5] += 1
            elif name == b'SRT0':
                subfile = Srt0(self.folders["AnmTexSrt(NW4R)"][counters[2]], self.folders["AnmTexSrt(NW4R)"])
                subfile.unpack(data[self.root.size + offsetToSubSection:self.root.size + offsetToSubSection + length])
                self.srt0[subfile.name] = subfile
                counters[6] += 1
            elif name == b'TEX0':
                subfile = Tex0(self.folders["Textures(NW4R)"][counters[7]], self.folders["Textures(NW4R)"])
                #subfile.unpack(data[self.root.size + offsetToSubSection:self.root.size + offsetToSubSection + length])
                subfile.readStart = self.root.size + offsetToSubSection
                subfile.readEnd = self.root.size + offsetToSubSection + length
                self.tex0[subfile.name] = subfile
                counters[7] += 1
            elif name == b'PLT0':
                subfile = Plt0(self.folders["Palettes(NW4R)"][counters[8]], self.folders["Palettes(NW4R)"])
                #subfile.unpack(data[self.root.size + offsetToSubSection:self.root.size + offsetToSubSection + length])
                subfile.readStart = self.root.size + offsetToSubSection
                subfile.readEnd = self.root.size + offsetToSubSection + length
                self.plt0[subfile.name] = subfile
                counters[8] += 1
            else:                   #insert other subfiles before this one - also in the counters list!
                subfile = Unk0(self.folders["Unknown(NW4R)"][counters[-1]], self.folders["Unknown(NW4R)"])
                subfile.unpack(data[self.root.size + offsetToSubSection:self.root.size + offsetToSubSection + length])
                self.unk0[subfile.name] = subfile
                counters[-1] += 1
                
                
            offsetToSubSection += length
            
        for name, subfile in self.plt0.items():                     #unpack Plt0
            subfile.unpack(data[subfile.readStart:subfile.readEnd])

        for name, subfile in self.tex0.items():                     #unpack Tex0
            if name in self.plt0:
                #print(self.plt0[name].palette)
                subfile.unpack(data[subfile.readStart:subfile.readEnd], self.plt0[name].palette)
            else:
                subfile.unpack(data[subfile.readStart:subfile.readEnd])



    # TODO
    def pack(self):
        data = []
        data.append(self.header.pack())
        data.append(self.root.pack())

        for i in range(0, self.header.n_sections):
            pass  # pack all sections

        return data


    def saveAllImagesAsPng(self):
        for key, value in self.tex0.items():
            for i in range(0, len(value.images)):
                value.images[i].save("{} {}.png".format(key, i))

