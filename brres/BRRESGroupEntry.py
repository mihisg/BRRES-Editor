from struct import Struct


class BRRESGroupEntry:
    """
    Class for an entry of the brres
    """

    def __init__(self):
        self.id = 0
        self.unknown = 0
        self.left_index = 0
        self.right_index = 00
        self.name_offset = 0
        self.data_offset = 0

        self.name = ""

    def unpack(self, data, start, end):
        indexGroupEntryUnpacker = Struct(">HHHHII")
        mainData = data[start:end]

        self.id, self.unknown, self.left_index, self.right_index, self.name_offset, self.data_offset = indexGroupEntryUnpacker.unpack(
            mainData)

        nameLength = data[self.name_offset - 1]
        self.name = data[self.name_offset:self.name_offset + nameLength].decode("utf-8")

        print(
            f"BRRESGroupEntry -- id={self.id}, zero={self.unknown}, leftIndex={self.left_index}, rightIndex={self.right_index}, nameOffset=0x{self.name_offset:04X}, name={self.name}, dataOffset=0x{self.data_offset:04X}")

    def pack(self):
        pass
