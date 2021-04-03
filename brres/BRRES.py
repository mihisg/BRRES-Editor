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
from PyQt5.QtGui import QStandardItemModel, QStandardItem


class BRRES:
    TAG = b'bres'

    def __init__(self):
        self.header = BRRESHeader()
        self.root = BRRESRootSection()
        self.model = QStandardItemModel()
        self.folders = {}
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


    def newItem(self, isFolder, name, data = 0):
        #title = os.path.basename(path)
        item = QStandardItem()
        #icon_path = FILE_ICON_PATH
        #if isFolder:
        #    icon_path = DIR_ICON_PATH
        #icon = QtGui.QIcon(icon_path)
        item.setText(name)
        #item.setIcon(icon)
        return item


    def generateFoldersAndFiles(self):
        for entry in range(0, self.root.first_group.n_entries):
            newParent = self.newItem(True, self.root.first_group.brres_entries[entry].name)
            self.model.appendRow(newParent)
            for i in self.root.subGroups[entry].brres_entries:
                newSubFile = self.newItem(False, i.name)
                newSubFile.subFile = 0
                newParent.appendRow(newSubFile)
            
            self.folders[self.root.first_group.brres_entries[entry].name] = newParent


    def unpackSubSections(self, data, offsetToSubSection):
        counters = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        
        for i in range(1, self.header.n_sections):
            name = Struct(">4s").unpack(data[self.root.size + offsetToSubSection:self.root.size + 0x4 + offsetToSubSection])[0]
            length = Struct(">I").unpack(data[self.root.size + offsetToSubSection + 0x4:self.root.size + 0x8 + offsetToSubSection])[0]
            
            if name == b'MDL0':
                subfile = Mdl0(self.folders["3DModels(NW4R)"].child(counters[0]), self.folders["3DModels(NW4R)"])             # Mdl0(name, parent)
                subfile.unpack(data[self.root.size + offsetToSubSection:self.root.size + offsetToSubSection + length])  # @Mihi is this actually correct? Can't check it right now 😅😜
                self.folders["3DModels(NW4R)"].child(counters[0]).subFile = subfile
                counters[0] += 1
                
            elif name == b'CHR0':
                subfile = Chr0(self.folders["AnmChr(NW4R)"].child(counters[1]), self.folders["AnmChr(NW4R)"])
                subfile.unpack(data[self.root.size + offsetToSubSection:self.root.size + offsetToSubSection + length])
                self.folders["AnmChr(NW4R)"].child(counters[1]).subFile = subfile
                counters[1] += 1
                
            elif name == b'CLR0':
                subfile = Clr0(self.folders["AnmClr(NW4R)"].child(counters[2]), self.folders["AnmClr(NW4R)"])
                subfile.unpack(data[self.root.size + offsetToSubSection:self.root.size + offsetToSubSection + length])
                self.folders["AnmClr(NW4R)"].child(counters[2]).subFile = subfile
                counters[2] += 1
                
            elif name == b'PAT0':
                subfile = Pat0(self.folders["AnmTexPat(NW4R)"].child(counters[3]), self.folders["AnmTexPat(NW4R)"])
                subfile.unpack(data[self.root.size + offsetToSubSection:self.root.size + offsetToSubSection + length])
                self.folders["AnmTexPat(NW4R)"].child(counters[3]).subFile = subfile
                counters[3] += 1
                
            elif name == b'SCN0':
                subfile = Scn0(self.folders["AnmScn(NW4R)"].child(counters[4]), self.folders["AnmScn(NW4R)"])
                subfile.unpack(data[self.root.size + offsetToSubSection:self.root.size + offsetToSubSection + length])
                self.folders["AnmScn(NW4R)"].child(counters[4]).subFile = subfile
                counters[4] += 1
                
            elif name == b'SHP0':
                subfile = Shp0(self.folders["AnmShp(NW4R)"].child(counters[5]), self.folders["AnmShp(NW4R)"])
                subfile.unpack(data[self.root.size + offsetToSubSection:self.root.size + offsetToSubSection + length])
                self.folders["AnmShp(NW4R)"].child(counters[5]).subFile = subfile
                counters[5] += 1
                
            elif name == b'SRT0':
                subfile = Srt0(self.folders["AnmTexSrt(NW4R)"].child(counters[6]), self.folders["AnmTexSrt(NW4R)"])
                subfile.unpack(data[self.root.size + offsetToSubSection:])  #self.root.size + offsetToSubSection + length  ->  @Nin0 this doesn't work since the string table at the end has to be accessed
                self.folders["AnmTexSrt(NW4R)"].child(counters[6]).subFile = subfile
                counters[6] += 1
                
            elif name == b'TEX0':
                subfile = Tex0(self.folders["Textures(NW4R)"].child(counters[7]), self.folders["Textures(NW4R)"])
                #subfile.unpack(data[self.root.size + offsetToSubSection:self.root.size + offsetToSubSection + length])
                subfile.readStart = self.root.size + offsetToSubSection
                subfile.readEnd = self.root.size + offsetToSubSection + length
                self.folders["Textures(NW4R)"].child(counters[7]).subFile = subfile
                counters[7] += 1
                
            elif name == b'PLT0':
                subfile = Plt0(self.folders["Palettes(NW4R)"].child(counters[8]), self.folders["Palettes(NW4R)"])
                subfile.unpack(data[self.root.size + offsetToSubSection:self.root.size + offsetToSubSection + length])
                self.folders["Palettes(NW4R)"].child(counters[8]).subFile = subfile
                counters[8] += 1
                
            else:                   #insert other subfiles before this one - also in the counters list!                         --> this won't work - there is no Unknown(NW4R) folder created in generateFoldersAndFiles ...
                subfile = Unk0(self.folders["Unknown(NW4R)"].child(counters[-1]), self.folders["Unknown(NW4R)"])
                subfile.unpack(data[self.root.size + offsetToSubSection:self.root.size + offsetToSubSection + length])
                self.folders["Unknown(NW4R)"].child(counters[-1]).subFile = subfile
                counters[-1] += 1
                
                
            offsetToSubSection += length
            
        
        #Unpack Tex0 subFiles:
        textures = self.folders["Textures(NW4R)"]
        for i in range(0, textures.rowCount()):             #unpack Tex0
            texture = textures.child(i).subFile
            name = textures.child(i).text()
            texture.unpack(data[texture.readStart:texture.readEnd], self.getPalette(name))


    def getPalette(self, name):
        if "Palettes(NW4R)" in self.folders:
            palettes = self.folders["Palettes(NW4R)"]
            for i in range(0, palettes.rowCount()):
                if palettes.child(i).text() == name:
                    return palettes.child(i).subFile.palette
        
        return []
        

    # TODO
    def pack(self):
        data = []
        data.append(self.header.pack())
        data.append(self.root.pack())

        for i in range(0, self.header.n_sections):
            pass  # pack all sections

        return data


    def saveAllImagesAsPng(self):
        textures = self.folders["Textures(NW4R)"]
        for i in range(0, textures.rowCount()):             #unpack Tex0
            texture = textures.child(i).subFile
            name = textures.child(i).text()
            for j in range(0, len(texture.images)):
                texture.images[j].save("{} {}.png".format(name, j))























