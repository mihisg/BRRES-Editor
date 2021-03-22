from brres.BRRESGroupEntry import *
from struct import Struct


class BRRESIndexGroup:
    """
    Class for an index group. They contain the folders of the brres or the actual sections
    """

    def __init__(self):
        self.size = 0
        self.n_entries = 0

        self.brres_entries = []

    def calculateSize(self):
        return 8 + (len(self.brres_entries) + 1) * 16

    def unpack(self, data):
        groupHeader = data[0x0:0x8]
        groupHeaderUnpacker = Struct("> I I")
        self.size, self.n_entries = groupHeaderUnpacker.unpack(groupHeader)

        offset = 0x10
        print(f"BRRESGroup -- length={self.size}, entries={self.n_entries}")
        for i in range(1, self.n_entries + 1):
            dataStart = 0x08 + offset
            dataEnd = 0x08 + offset + 0x10

            newEntry = BRRESGroupEntry()
            newEntry.unpack(data, dataStart, dataEnd)
            offset += 0x10
            self.brres_entries.append(newEntry)

            print(f"New entry with name {newEntry.name}")

    def pack(self):
        groupHeaderPacker = Struct("> I I")
        data = []
        data.append()
