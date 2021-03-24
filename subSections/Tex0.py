from subSections.SubSection import SubSection
from struct import Struct
try:
    from PyQt5.QtGui import QImage
except ImportError:
    from PySide2.QtGui import QImage

class Tex0(SubSection):
    """
    TEX0-subfile of a brres, represents images and textures
    """

    TAG = 'TEX0'
    EXTENSION = 'tex0'
    FORMATS = {0: 'I4', 1: 'I8', 2: 'IA4', 3: 'IA8',
               4: 'RGB565', 5: 'RGB5A3', 6: 'RGBA32',
               8: 'C4', 9: 'C8', 10: 'C14X2', 14: 'CMPR'}

    def __init__(self, name, parent):
        super(Tex0, self).__init__(name, parent)
        self.animations = []
        self.framecount = 1
        self.loop = True
        self.scaling_rule = 0

    def unpack(self, data):
        super()._unpack(data, {1: 1, 2: 2, 3: 1})

    def pack(self):
        pass





RGB4A3LUT = []
RGB4A3LUT_NoAlpha = []
def PrepareRGB4A3LUTs():
    global RGB4A3LUT, RGB4A3LUT_NoAlpha

    RGB4A3LUT = [None] * 0x10000
    RGB4A3LUT_NoAlpha = [None] * 0x10000
    for LUT, hasA in [(RGB4A3LUT, True), (RGB4A3LUT_NoAlpha, False)]:

        # RGB4A3
        for d in range(0x8000):
            if hasA:
                alpha = d >> 12
                alpha = alpha << 5 | alpha << 2 | alpha >> 1
            else:
                alpha = 0xFF
            red = ((d >> 8) & 0xF) * 17
            green = ((d >> 4) & 0xF) * 17
            blue = (d & 0xF) * 17
            LUT[d] = blue | (green << 8) | (red << 16) | (alpha << 24)

        # RGB555
        for d in range(0x8000):
            red = d >> 10
            red = red << 3 | red >> 2
            green = (d >> 5) & 0x1F
            green = green << 3 | green >> 2
            blue = d & 0x1F
            blue = blue << 3 | blue >> 2
            LUT[d + 0x8000] = blue | (green << 8) | (red << 16) | 0xFF000000

PrepareRGB4A3LUTs()

def RGB4A3Decode(tex, useAlpha=True):
    tx = 0; ty = 0
    iter = tex.__iter__()
    dest = [0] * 262144

    LUT = RGB4A3LUT if useAlpha else RGB4A3LUT_NoAlpha

    # Loop over all texels (of which there are 16384)
    for i in range(16384):
        temp1 = (i // 256) % 8
        if temp1 == 0 or temp1 == 7:
            # Skip every row of texels that is a multiple of 8 or (a
            # multiple of 8) - 1
            # Unrolled loop for performance.
            next(iter); next(iter); next(iter); next(iter)
            next(iter); next(iter); next(iter); next(iter)
            next(iter); next(iter); next(iter); next(iter)
            next(iter); next(iter); next(iter); next(iter)
            next(iter); next(iter); next(iter); next(iter)
            next(iter); next(iter); next(iter); next(iter)
            next(iter); next(iter); next(iter); next(iter)
            next(iter); next(iter); next(iter); next(iter)
        else:
            temp2 = i % 8
            if temp2 == 0 or temp2 == 7:
                # Skip every column of texels that is a multiple of 8
                # or (a multiple of 8) - 1
                # Unrolled loop for performance.
                next(iter); next(iter); next(iter); next(iter)
                next(iter); next(iter); next(iter); next(iter)
                next(iter); next(iter); next(iter); next(iter)
                next(iter); next(iter); next(iter); next(iter)
                next(iter); next(iter); next(iter); next(iter)
                next(iter); next(iter); next(iter); next(iter)
                next(iter); next(iter); next(iter); next(iter)
                next(iter); next(iter); next(iter); next(iter)
            else:
                # Actually render this texel
                for y in range(ty, ty+4):
                    for x in range(tx, tx+4):
                        dest[x + y * 1024] = LUT[next(iter) << 8 | next(iter)]

        # Move on to the next texel
        tx += 4
        if tx >= 1024: tx = 0; ty += 4

    # Convert the list of ARGB color values into a bytes object, and
    # then convert that into a QImage
    return QImage(struct.pack('<262144I', *dest), 1024, 256, QImage.Format_ARGB32)


def RGB4A3Encode(tex):
    shorts = []
    colorCache = {}
    for ytile in range(0, 256, 4):
        for xtile in range(0, 1024, 4):
            for ypixel in range(ytile, ytile + 4):
                for xpixel in range(xtile, xtile + 4):

                    if xpixel >= 1024 or ypixel >= 256:
                        continue

                    pixel = tex.pixel(xpixel, ypixel)

                    if pixel in colorCache:
                        rgba = colorCache[pixel]

                    else:

                        a = pixel >> 24
                        r = (pixel >> 16) & 0xFF
                        g = (pixel >> 8) & 0xFF
                        b = pixel & 0xFF

                        # See encodingTests.py for verification that these
                        # channel conversion formulas are 100% correct

                        # It'd be nice if we could do
                        # if a < 19:
                        #     rgba = 0
                        # for speed, but that defeats the purpose of the
                        # "Toggle Alpha" setting.

                        if a < 238: # RGB4A3
                            alpha = ((a + 18) << 1) // 73
                            red = (r + 8) // 17
                            green = (g + 8) // 17
                            blue = (b + 8) // 17

                            # 0aaarrrrggggbbbb
                            rgba = blue | (green << 4) | (red << 8) | (alpha << 12)

                        else: # RGB555
                            red = ((r + 4) << 2) // 33
                            green = ((g + 4) << 2) // 33
                            blue = ((b + 4) << 2) // 33

                            # 1rrrrrgggggbbbbb
                            rgba = blue | (green << 5) | (red << 10) | (0x8000)

                        colorCache[pixel] = rgba

                    shorts.append(rgba)

                    if xtile % 32 == 0 or xtile % 32 == 28:
                        shorts.append(rgba)
                        shorts.append(rgba)
                        shorts.append(rgba)
                        break
                if ytile % 32 == 0 or ytile % 32 == 28:
                    shorts.extend(shorts[-4:])
                    shorts.extend(shorts[-8:])
                    break

    return struct.pack('>262144H', *shorts)
