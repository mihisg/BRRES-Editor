from struct import Struct


class BRRESHeader:
    """
    Class for the header of a brres archive
    """

    def __init__(self):
        self.tag = 0
        self.byte_order_mark = 0
        self.padding = 0
        self.length = 0
        self.root_offset = 0
        self.n_sections = 0

    def unpack(self, data):
        headerUnpack = Struct(">4s H H I H H")
        self.tag, self.byte_order_mark, self.padding, self.length, self.root_offset, self.n_sections = headerUnpack.unpack(
            data)

        print("Header created!")
        print(f"magic: {self.tag}")
        print(f"bom: 0x{self.byte_order_mark:X}")
        print(f"padding: {self.padding}")
        print(f"length: {self.length}")
        print(f"root offset: 0x{self.root_offset:X}")
        print(f"num sections: {self.n_sections}")

    def pack(self):
        headerPack = Struct(">4s H H I H H")
        return headerPack.pack(self.tag, self.byte_order_mark, self.padding, self.root_offset, self.n_sections)
