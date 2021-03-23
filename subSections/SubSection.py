from struct import Struct

"""class Observer:
    def onNodeUpdate(self, node):
        pass

    def onRenameUpadte(self, node):
        pass

    def onChildUpdate(self, node):
        pass
"""


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

    def rename(self, name):
        if name != self.name:
            oldName = self.name
            self.name = name
            self.markModified(False)
            # self.notifyRename(oldName)
            return True
        return False

    def markModified(self, notifyObservers=True):
        if notifyObservers:
            pass  # self.notifyObservers()
        if not self.isModified:
            self.isModified = True
            if self.parent:
                self.parent.markModified(False)

    def markUnmodified(self):
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

        """elif header.versionNum == 2:
                headerUnpacker2 = Struct("> I")
                header.sectionOffsets.append(headerUnpacker2.unpack(data[0x10:0x14]))
                header.sectionOffsets.append(headerUnpacker2.unpack(data[0x14:0x18]))
            elif header.versionNum == 3:
                headerUnpacker2 = Struct("> I")
                header.sectionOffsets.append(headerUnpacker2.unpack(data[0x10:0x14]))
            elif header.versionNum == 4:
                headerUnpacker2 = Struct("> I")
                header.sectionOffsets.append(headerUnpacker2.unpack(data[0x10:0x14]))
            elif header.versionNum == 5:
                headerUnpacker2 = Struct("> I")
                header.sectionOffsets.append(headerUnpacker2.unpack(data[0x10:0x14]))
            elif header.versionNum == 8:
                headerUnpacker2 = Struct("> I")
                header.sectionOffsets.append(headerUnpacker2.unpack(data[0x10:0x14]))
            elif header.versionNum == 11:
                headerUnpacker2 = Struct("> I")
                header.sectionOffsets.append(headerUnpacker2.unpack(data[0x10:0x14]))"""
        # else:
        # ValueError("The section number does not equal the common values 1, 2 or 3")


def _pack(self):
    pass


"""def notifyRename(self, oldName):
    if self.observers:
        for o in self.observers:
            o.onRenameUpdate(self, oldName)
    self.notifyParentObservers()"""

"""def notifyParentObservers(self):
    parent = self.parent
    if parent and parent.observers:
        for o in parent.observers:
            o.onChildUpdate()"""

"""def registerObserver(self, observer):
    if self.observers is None:
        self.observers = [observer]
    elif observer not in self.observers:
        self.observers.append(observer)"""

"""def unregister(self, observer):
    try:
        self.observers.remove(observer)
    except ValueError as e:
        print(f"Could not remove observer {observer} because it is not contained in the list: {e} ")"""

"""def notifyObservers(self):
    if self.observers:
        for o in self.observers:
            o.onNodeUpdate()
    self.notifyParentObservers()"""
