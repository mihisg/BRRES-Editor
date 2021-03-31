from subSections.SubSection import SubSection
from subSections.TPLLib import *
from struct import Struct


class Unk0(SubSection):
    """
    Unknown subfile of a brres
    """
    
    TAG = 'UNK0'        #used for all unknown subfiles
    EXTENSION = 'unk0'  #used for all unknown subfiles
    
    def __init__(self, name, parent):
        super(Unk0, self).__init__(name, parent)
    
    def unpack(self, data):
        pass
    
    def pack(self):
        pass