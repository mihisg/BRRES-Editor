from subSections.SubSection import SubSection
from subSections.TPLLib import *
from struct import Struct


class Plt0(SubSection):
    """
    PLT0-subfile of a brres, represents palettes for Tex0 files
    """
    
    TAG = 'PLT0'
    EXTENSION = 'plt0'
    
    def __init__(self, name, parent):
        super(Plt0, self).__init__(name, parent)
    
    def unpack(self, data):
        pass
    
    def pack(self):
        pass