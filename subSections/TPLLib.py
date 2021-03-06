# TPLLib - A Python library for decoding and encoding Nintendo image formats
# Version 0.2
# Copyright (C) 2009-2014 Tempus, RoadrunnerWMC, 2021 Nin0

# This file was part of TPLLib.

# TPLLib is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# TPLLib is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with TPLLib.  If not, see <http://www.gnu.org/licenses/>.



################################################################
################################################################


class Decoder():
    """
    Object that decodes a texture
    """
    def __init__(self, tex, width, height, palette):
        """
        Initializes the decoder
        """
        self.tex = tex
        self.size = [width, height]
        self.palette = palette
        self.result = None


    def run(self):
        """
        Runs the algorithm
        """
        raise NotImplementedError('You cannot run an abstract decoder')


class Encoder():
    """
    Object that encodes a texture
    """
    def __init__(self, argb, width, height):
        """
        Initializes the encoder
        """
        self.argb = argb
        self.size = [width, height]
        self.result = None

    def run(self):
        """
        Runs the algorithm
        """
        raise NotImplementedError('You cannot run an abstract encoder')


class I4Decoder(Decoder):
    """
    Decodes an I4 texture
    """
    # Format:
    # IIII
    bytesPerPixel = .5

    def run(self):
        """
        Runs the algorithm
        """
        tex, w, h = self.tex, self.size[0], self.size[1]

        argbBuf = bytearray((w+4) * (h+4) * 4)
        i = 0
        for ytile in range(0, h, 8):
            for xtile in range(0, w, 8):
                for ypixel in range(ytile, ytile + 8):
                    for xpixel in range(xtile, xtile + 8, 2):
                        try:
                            newpixel = (tex[i] >> 4) * 0x11 # upper nybble

                            argbBuf[(((ypixel * w) + xpixel) * 4) + 0] = newpixel
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 1] = newpixel
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 2] = newpixel
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 3] = 0xFF

                            newpixel = (tex[i] & 0xF) * 0x11 # lower nybble

                            argbBuf[(((ypixel * w) + xpixel) * 4) + 4] = newpixel
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 5] = newpixel
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 6] = newpixel
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 7] = 0xFF
                        except IndexError: continue
                        i += 1

        self.result = bytes(argbBuf)
        return self.result


class I4Encoder(Encoder):
    """
    Encodes an I4 texture
    """
    # Format:
    # IIII
    bytesPerPixel = .5

    def run(self):
        """
        Runs the algorithm
        """
        argb, w, h = self.argb, self.size[0], self.size[1]

        texBuf = bytearray(int(w * h / 2))
        i = 0
        for ytile in range(0, h, 8):
            for xtile in range(0, w, 8):
                for ypixel in range(ytile, ytile + 8):
                    for xpixel in range(xtile, xtile + 8, 2):

                        if xpixel >= w or ypixel >= h:
                            continue

                        newpixelB = argb[(((ypixel * w) + xpixel) * 4) + 0]
                        newpixelG = argb[(((ypixel * w) + xpixel) * 4) + 1]
                        newpixelR = argb[(((ypixel * w) + xpixel) * 4) + 2]
                        newpixelA = argb[(((ypixel * w) + xpixel) * 4) + 3]
                        newpixel = (newpixelR + newpixelG + newpixelB) / 3
                        newpixel = int(newpixel * (newpixelA / 255))

                        texBuf[i] = ((newpixel + 8) // 17) << 4 # upper nybble

                        newpixelB = argb[(((ypixel * w) + xpixel) * 4) + 4]
                        newpixelG = argb[(((ypixel * w) + xpixel) * 4) + 5]
                        newpixelR = argb[(((ypixel * w) + xpixel) * 4) + 6]
                        newpixelA = argb[(((ypixel * w) + xpixel) * 4) + 7]
                        newpixel = (newpixelR + newpixelG + newpixelB) / 3
                        newpixel = int(newpixel * (newpixelA / 255))

                        texBuf[i] |= (newpixel + 8) // 17 # lower nybble

                        i += 1

        self.result = bytes(texBuf)
        return self.result


class I8Decoder(Decoder):
    """
    Decodes an I8 texture
    """
    # Format:
    # IIIIIIII
    bytesPerPixel = 1

    def run(self):
        """
        Runs the algorithm
        """
        tex, w, h = self.tex, self.size[0], self.size[1]

        argbBuf = bytearray((w+4) * (h+4) * 4)
        i = 0
        for ytile in range(0, h, 4):
            for xtile in range(0, w, 8):
                for ypixel in range(ytile, ytile + 4):
                    for xpixel in range(xtile, xtile + 8):
                        try:
                            newpixel = tex[i]

                            argbBuf[(((ypixel * w) + xpixel) * 4) + 0] = newpixel
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 1] = newpixel
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 2] = newpixel
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 3] = 0xFF
                        except IndexError: continue
                        i += 1

        self.result = bytes(argbBuf)
        return self.result


class I8Encoder(Encoder):
    """
    Encodes an I8 texture
    """
    # Format:
    # IIIIIIII
    bytesPerPixel = 1

    def run(self):
        """
        Runs the algorithm
        """
        argb, w, h = self.argb, self.size[0], self.size[1]

        texBuf = bytearray(w * h)
        i = 0
        for ytile in range(0, h, 4):
            for xtile in range(0, w, 8):
                for ypixel in range(ytile, ytile + 4):
                    for xpixel in range(xtile, xtile + 8):

                        if xpixel >= w or ypixel >= h:
                            continue

                        newpixelB = argb[(((ypixel * w) + xpixel) * 4) + 0]
                        newpixelG = argb[(((ypixel * w) + xpixel) * 4) + 1]
                        newpixelR = argb[(((ypixel * w) + xpixel) * 4) + 2]
                        newpixelA = argb[(((ypixel * w) + xpixel) * 4) + 3]
                        newpixel = (newpixelR + newpixelG + newpixelB) / 3
                        texBuf[i] = int(newpixel * (newpixelA / 255))

                        i += 1

        self.result = bytes(texBuf)
        return self.result


class IA4Decoder(Decoder):
    """
    Decodes an IA4 texture
    """
    # Format:
    # AAAAIIII
    bytesPerPixel = 1

    def run(self):
        """
        Runs the algorithm
        """
        tex, w, h = self.tex, self.size[0], self.size[1]

        argbBuf = bytearray((w+4) * (h+4) * 4)
        i = 0
        for ytile in range(0, h, 4):
            for xtile in range(0, w, 8):
                for ypixel in range(ytile, ytile + 4):
                    for xpixel in range(xtile, xtile + 8):
                        try:
                            alpha = (tex[i] >> 4) * 0x11
                            newpixel = (tex[i] & 0xF) * 0x11

                            argbBuf[((ypixel * w) + xpixel) * 4] = newpixel
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 1] = newpixel
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 2] = newpixel
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 3] = alpha
                        except IndexError: continue
                        i += 1

        self.result = bytes(argbBuf)
        return self.result


class IA4Encoder(Encoder):
    """
    Encodes an IA4 texture
    """
    # Format:
    # AAAAIIII
    bytesPerPixel = 1

    def run(self):
        """
        Runs the algorithm
        """
        argb, w, h = self.argb, self.size[0], self.size[1]

        texBuf = bytearray(w * h)
        i = 0
        for ytile in range(0, h, 4):
            for xtile in range(0, w, 8):
                for ypixel in range(ytile, ytile + 4):
                    for xpixel in range(xtile, xtile + 8):

                        if xpixel >= w or ypixel >= h:
                            continue

                        newpixelB = argb[(((ypixel * w) + xpixel) * 4) + 0]
                        newpixelG = argb[(((ypixel * w) + xpixel) * 4) + 1]
                        newpixelR = argb[(((ypixel * w) + xpixel) * 4) + 2]
                        newpixelA = argb[(((ypixel * w) + xpixel) * 4) + 3]
                        newpixel = (newpixelR + newpixelG + newpixelB) / 3
                        texBuf[i] = (int((newpixelA + 8) // 17) << 4) | int((newpixel + 8) // 17)

                        i += 1

        self.result = bytes(texBuf)
        return self.result


class IA8Decoder(Decoder):
    """
    Decodes an IA8 texture
    """
    # Format:
    # IIIIIIII AAAAAAAA
    bytesPerPixel = 2

    def run(self):
        """
        Runs the algorithm
        """
        tex, w, h = self.tex, self.size[0], self.size[1]

        argbBuf = bytearray((w+4) * (h+4) * 4)
        i = 0
        for ytile in range(0, h, 4):
            for xtile in range(0, w, 4):
                for ypixel in range(ytile, ytile + 4):
                    for xpixel in range(xtile, xtile + 4):
                        try:
                            alpha = tex[i]
                        
                            newpixel = tex[i+1]
                        
                            argbBuf[((ypixel * w) + xpixel) * 4] = newpixel
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 1] = newpixel
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 2] = newpixel
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 3] = alpha
                        except IndexError: continue
                        i += 2

        self.result = bytes(argbBuf)
        return self.result


class IA8Encoder(Encoder):
    """
    Encodes an IA8 texture
    """
    # Format:
    # IIIIIIII AAAAAAAA
    bytesPerPixel = 2

    def run(self):
        """
        Runs the algorithm
        """
        argb, w, h = self.argb, self.size[0], self.size[1]

        texBuf = bytearray(w * h * 2)
        i = 0
        for ytile in range(0, h, 4):
            for xtile in range(0, w, 4):
                for ypixel in range(ytile, ytile + 4):
                    for xpixel in range(xtile, xtile + 4):

                        if xpixel >= w or ypixel >= h:
                            continue

                        newpixelB = argb[(((ypixel * w) + xpixel) * 4) + 0]
                        newpixelG = argb[(((ypixel * w) + xpixel) * 4) + 1]
                        newpixelR = argb[(((ypixel * w) + xpixel) * 4) + 2]
                        newpixelA = argb[(((ypixel * w) + xpixel) * 4) + 3]
                        newpixel = int((newpixelR + newpixelG + newpixelB) / 3)
                        texBuf[i] = newpixel
                        i += 1
                        texBuf[i] = newpixelA
                        i += 1

        self.result = bytes(texBuf)
        return self.result


class RGB565Decoder(Decoder):
    """
    Decodes an RGB565 texture
    """
    # Format:
    # RRRRRGGG GGGBBBBB
    bytesPerPixel = 2

    def run(self):
        """
        Runs the algorithm
        """
        tex, w, h = self.tex, self.size[0], self.size[1]

        argbBuf = bytearray((w+4) * (h+4) * 4)
        i = 0
        for ytile in range(0, h, 4):
            for xtile in range(0, w, 4):
                for ypixel in range(ytile, ytile + 4):
                    for xpixel in range(xtile, xtile + 4):
                        try:
                            blue5 = tex[i + 1] & 0x1F
                            blue = blue5 << 3 | blue5 >> 2

                            greenB = (tex[i + 1] >> 5)
                            greenT = (tex[i] & 0x7)
                            green = greenT << 5 | greenB << 2 | greenT >> 1

                            red5 = tex[i] >> 3
                            red = red5 << 3 | red5 >> 2

                            alpha = 0xFF

                            argbBuf[(((ypixel * w) + xpixel) * 4) + 0] = blue
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 1] = green
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 2] = red
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 3] = alpha
                        except IndexError: continue
                        i += 2

        self.result = bytes(argbBuf)
        return self.result



class RGB565Encoder(Encoder):
    """
    Encodes an RGB565 texture
    """
    # Format:
    # RRRRRGGG GGGBBBBB
    bytesPerPixel = 2

    def run(self):
        """
        Runs the algorithm
        """
        argb, w, h = self.argb, self.size[0], self.size[1]

        texBuf = bytearray(w * h * 2)
        i = 0
        for ytile in range(0, h, 4):
            for xtile in range(0, w, 4):
                for ypixel in range(ytile, ytile + 4):
                    for xpixel in range(xtile, xtile + 4):
                        newpixelB = argb[(((ypixel * w) + xpixel) * 4) + 0]
                        newpixelG = argb[(((ypixel * w) + xpixel) * 4) + 1]
                        newpixelR = argb[(((ypixel * w) + xpixel) * 4) + 2]
                        newpixelA = argb[(((ypixel * w) + xpixel) * 4) + 3]
                        newpixelR = int(newpixelR * (newpixelA / 255))
                        newpixelG = int(newpixelG * (newpixelA / 255))
                        newpixelB = int(newpixelB * (newpixelA / 255))
                        red5 = ((newpixelR + 4) << 2) // 33
                        green6 = ((newpixelG + 2) << 4) // 65
                        blue5 = ((newpixelB + 4) << 2) // 33
                        newpixel = red5 << 11 | green6 << 5 | blue5
                        texBuf[i] = newpixel >> 8
                        texBuf[i + 1] = newpixel & 0xFF
                        i += 2

        self.result = bytes(texBuf)
        return self.result


class RGB5A3Decoder(Decoder):
    """
    Decodes an RGB5A3 texture
    """
    # Formats:
    # 1BBBBBGG GGGRRRRR
    # 0AAABBBB GGGGRRRR
    bytesPerPixel = 2

    def run(self):
        """
        Runs the algorithm
        """
        tex, w, h = self.tex, self.size[0], self.size[1]

        argbBuf = bytearray((w+4) * (h+4) * 4)
        i = 0
        for ytile in range(0, h, 4):
            for xtile in range(0, w, 4):
                for ypixel in range(ytile, ytile + 4):
                    for xpixel in range(xtile, xtile + 4):
                        try:

                            newpixel = (tex[i] << 8) | tex[i+1]
                            newpixel = int(newpixel)


                            if newpixel & 0x8000: # RGB555
                                blue5 = (newpixel >> 10) & 0x1F
                                green5 = (newpixel >> 5) & 0x1F
                                red5 = newpixel & 0x1F
                                blue = blue5 << 3 | blue5 >> 2
                                green = green5 << 3 | green5 >> 2
                                red = red5 << 3 | red5 >> 2
                                alpha = 0xFF

                            else: # RGB5A3
                                alpha3 = newpixel >> 12
                                blue4 = (newpixel >> 8) & 0xF
                                green4 = (newpixel >> 4) & 0xF
                                red4 = newpixel & 0xF
                                alpha = (alpha3 << 5) | (alpha3 << 2) | (alpha3 >> 1)
                                blue = blue4 * 17
                                green = green4 * 17
                                red = red4 * 17

                            argbBuf[(((ypixel * w) + xpixel) * 4) + 0] = red
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 1] = green
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 2] = blue
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 3] = alpha
                        except IndexError: continue
                        i += 2

        self.result = bytes(argbBuf)
        return self.result


class RGB5A3Encoder(Encoder):
    """
    Encodes an RGB5A3 texture
    """
    # Formats:
    # 1BBBBBGG GGGRRRRR
    # 0RRRRGGG GBBBBAAA
    bytesPerPixel = 2

    def run(self):
        """
        Runs the algorithm
        """
        argb, w, h = self.argb, self.size[0], self.size[1]

        texBuf = bytearray(w * h * 2)
        i = 0
        for ytile in range(0, h, 4):
            for xtile in range(0, w, 4):
                for ypixel in range(ytile, ytile + 4):
                    for xpixel in range(xtile, xtile + 4):
                        newpixelB = argb[(((ypixel * w) + xpixel) * 4) + 0]
                        newpixelG = argb[(((ypixel * w) + xpixel) * 4) + 1]
                        newpixelR = argb[(((ypixel * w) + xpixel) * 4) + 2]
                        newpixelA = argb[(((ypixel * w) + xpixel) * 4) + 3]
                        if newpixelA < 238: # RGB5A3
                            alpha3 = ((newpixelA + 18) << 1) // 73
                            red4 = (newpixelR + 8) // 17
                            green4 = (newpixelG + 8) // 17
                            blue4 = (newpixelB + 8) // 17
                            newpixel = (alpha3 << 12) | (red4 << 8) | (green4 << 4) | blue4
                        else: # RGB555
                            red5 = ((newpixelR + 4) << 2) // 33
                            green5 = ((newpixelG + 4) << 2) // 33
                            blue5 = ((newpixelB + 4) << 2) // 33
                            newpixel = 0x8000 | (red5 << 10) | (green5 << 5) | blue5
                        texBuf[i] = newpixel >> 8
                        texBuf[i + 1] = newpixel & 0xFF
                        i += 2

        self.result = bytes(texBuf)
        return self.result


class RGBA8Decoder(Decoder):
    """
    Decodes an RGBA8 texture
    """
    # Format:
    # RRRRRRRR GGGGGGGG BBBBBBBB AAAAAAAA
    bytesPerPixel = 4

    def run(self):
        """
        Runs the algorithm
        """
        tex, w, h = self.tex, self.size[0], self.size[1]

        argbBuf = bytearray(w * h * 4)
        i = 0
        for ytile in range(0, h, 4):
            for xtile in range(0, w, 4):
                A = []
                R = []
                G = []
                B = []
                try:
                    for AR in range(16):
                        A.append(tex[i])
                        R.append(tex[i+1])
                        i += 2
                    for GB in range(16):
                        G.append(tex[i])
                        B.append(tex[i+1])
                        i += 2
                except IndexError: continue

                j = 0
                try:
                    for ypixel in range(ytile, ytile+4):
                        for xpixel in range(xtile, xtile+4):
                            red, green, blue, alpha = R[j], G[j], B[j], A[j]
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 0] = blue
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 1] = green
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 2] = red
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 3] = alpha
                            j += 1
                except IndexError: continue

        self.result = bytes(argbBuf)
        return self.result



class RGBA8Encoder(Encoder):
    """
    Encodes an RGBA8 texture
    """
    # Format:
    # RRRRRRRR GGGGGGGG BBBBBBBB AAAAAAAA
    bytesPerPixel = 4

    def run(self):
        """
        Runs the algorithm
        """
        argb, w, h = self.argb, self.size[0], self.size[1]

        texBuf = bytearray(w * h * 4)
        i = 0
        for ytile in range(0, h, 4):
            for xtile in range(0, w, 4):
                for ypixel in range(ytile, ytile + 4):
                    for xpixel in range(xtile, xtile + 4):
                        newpixelR = argb[(((ypixel * w) + xpixel) * 4) + 2]
                        newpixelA = argb[(((ypixel * w) + xpixel) * 4) + 3]
                        texBuf[i] = newpixelA
                        i += 1
                        texBuf[i] = newpixelR
                        i += 1
                for ypixel in range(ytile, ytile + 4):
                    for xpixel in range(xtile, xtile + 4):
                        newpixelB = argb[(((ypixel * w) + xpixel) * 4) + 0]
                        newpixelG = argb[(((ypixel * w) + xpixel) * 4) + 1]
                        texBuf[i] = newpixelG
                        i += 1
                        texBuf[i] = newpixelB
                        i += 1

        self.result = bytes(texBuf)
        return self.result


class CI4Decoder(Decoder):
    """
    Decodes a CI4 texture
    """
    def run(self):
        """
        Runs the algorithm
        """
        if not self.palette: raise TypeError("Palette for decoding seems to be missing!")
        tex, w, h = self.tex, self.size[0], self.size[1]

        argbBuf = bytearray((w+4) * (h+4) * 4)
        i = 0
        for ytile in range(0, h, 8):
            for xtile in range(0, w, 8):
                for ypixel in range(ytile, ytile + 8):
                    for xpixel in range(xtile, xtile + 8, 2):
                        try:
                            index = (tex[i] >> 4) # upper nybble

                            argbBuf[(((ypixel * w) + xpixel) * 4) + 0] = self.palette[index][0]
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 1] = self.palette[index][1]
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 2] = self.palette[index][2]
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 3] = self.palette[index][3]

                            index = (tex[i] & 0xF) # lower nybble

                            argbBuf[(((ypixel * w) + xpixel) * 4) + 4] = self.palette[index][0]
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 5] = self.palette[index][1]
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 6] = self.palette[index][2]
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 7] = self.palette[index][3]
                        except IndexError: continue
                        i += 1

        self.result = bytes(argbBuf)
        return self.result


class CI8Decoder(Decoder):
    """
    Decodes a CI8 texture
    """
    def run(self):
        """
        Runs the algorithm
        """
        if not self.palette: raise TypeError("Palette for decoding seems to be missing!")
        tex, w, h = self.tex, self.size[0], self.size[1]

        argbBuf = bytearray((w+4) * (h+4) * 4)
        i = 0
        for ytile in range(0, h, 4):
            for xtile in range(0, w, 8):
                for ypixel in range(ytile, ytile + 4):
                    for xpixel in range(xtile, xtile + 8):
                        try:
                            index = tex[i]

                            argbBuf[(((ypixel * w) + xpixel) * 4) + 0] = self.palette[index][0]
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 1] = self.palette[index][1]
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 2] = self.palette[index][2]
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 3] = self.palette[index][3]
                        except IndexError: continue
                        i += 1

        self.result = bytes(argbBuf)
        return self.result








class CMPRDecoder(Decoder):
    """
    Decodes an RGBA8 texture
    """
    
    bytesPerPixel = 0.5 #, or 4 bits
    blockWidth   = 8
    blockHeight  = 8
    
    def run(self):
        """
        Runs the algorithm
        """
        tex, w, h = self.tex, self.size[0], self.size[1]
        argbBuf = bytearray(w * h * 4)
        i = 0
        for ytile in range(0, h, 8):
            for xtile in range(0, w, 8):
                palette = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
                for subb in range(0, 4):
                
                    val1 = tex[i] | (tex[i + 1] << 8)
                
                    blue5 = tex[i + 1] & 0x1F
                    blue = blue5 << 3 | blue5 >> 2

                    greenB = (tex[i + 1] >> 5)
                    greenT = (tex[i] & 0x7)
                    green = greenT << 5 | greenB << 2 | greenT >> 1

                    red5 = tex[i] >> 3
                    red = red5 << 3 | red5 >> 2

                    alpha = 0xFF
                    
                    palette[0] = [blue, green, red, alpha]
                    
                    i += 2



                    val2 = tex[i] | (tex[i + 1] << 8)
                
                    blue5 = tex[i + 1] & 0x1F
                    blue = blue5 << 3 | blue5 >> 2

                    greenB = (tex[i + 1] >> 5)
                    greenT = (tex[i] & 0x7)
                    green = greenT << 5 | greenB << 2 | greenT >> 1

                    red5 = tex[i] >> 3
                    red = red5 << 3 | red5 >> 2

                    alpha = 0xFF
                    
                    palette[1] = [blue, green, red, alpha]
                    
                    i += 2
                    
                    

                    if val1 > val2:
                        blue =  (2 * palette[0][0] + palette[1][0]) / 3
                        green = (2 * palette[0][1] + palette[1][1]) / 3
                        red =   (2 * palette[0][2] + palette[1][2]) / 3
                        alpha = 0xff
                        palette[2] = [blue, green, red, alpha]
                        
                        blue =  (2 * palette[1][0] + palette[0][0]) / 3
                        green = (2 * palette[1][1] + palette[0][1]) / 3
                        red =   (2 * palette[1][2] + palette[0][2]) / 3
                        alpha = 0xff
                        palette[3] = [blue, green, red, alpha]
                        
                    else:
                        blue =  (palette[0][0] + palette[1][0]) / 2
                        green = (palette[0][1] + palette[1][1]) / 2
                        red =   (palette[0][2] + palette[1][2]) / 2
                        alpha = 0xff
                        palette[2] = [blue, green, red, alpha]
                        
                        blue  = 0
                        green = 0
                        red   = 0
                        alpha = 0
                        palette[3] = [blue, green, red, alpha]
                        
                    
                    print(palette)
                    
                    for j in range(0, 4):
                        try:
                            val = i
                            i += 1
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 0 + j*4] = palette[val&3][0]
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 1 + j*4] = palette[val&3][1]
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 2 + j*4] = palette[val&3][2]
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 3 + j*4] = palette[val&3][3]

                            val >>= 2
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 4 + j*4] = palette[val&3][0]
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 5 + j*4] = palette[val&3][1]
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 6 + j*4] = palette[val&3][2]
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 7 + j*4] = palette[val&3][3]

                            val >>= 2
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 8 + j*4] = palette[val&3][0]
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 9 + j*4] = palette[val&3][1]
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 10 + j*4] = palette[val&3][2]
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 11 + j*4] = palette[val&3][3]

                            val >>= 2
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 12 + j*4] = palette[val&3][0]
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 13 + j*4] = palette[val&3][1]
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 14 + j*4] = palette[val&3][2]
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 15 + j*4] = palette[val&3][3]
                        except: continue #print("well")
                    
        self.result = bytes(argbBuf)
        return self.result






# Enums
I4 = 0
I8 = 1
IA4 = 2
IA8 = 3
RGB565 = 4
RGB5A3 = 5
RGBA8 = 6
CI4 = 8
CI8 = 9
CI14x2 = 10
CMPR = 14



def getDecoder(type):
    """
    Returns the appropriate decoding algorithm based on the type specified
    """
    if not isinstance(type, int):
        raise TypeError('Type is not an int')

    if type == I4:
        return I4Decoder
    elif type == I8:
        return I8Decoder
    elif type == IA4:
        return IA4Decoder
    elif type == IA8:
        return IA8Decoder
    elif type == RGB565:
        return RGB565Decoder
    elif type == RGB5A3:
        return RGB5A3Decoder
    elif type == RGBA8:
        return RGBA8Decoder
    elif type == CI4:
        return CI4Decoder #raise ValueError('CI4 is not supported')
    elif type == CI8:
        return CI8Decoder #raise ValueError('CI8 is not supported')
    elif type == CI14x2:
        raise ValueError('CI14x2 is not supported')
    elif type == CMPR:
        return CMPRDecoder #raise ValueError('CMPR is not supported')
    else:
        raise ValueError('Unrecognized type')


def getEncoder(type):
    """
    Returns the appropriate encoding algorithm based on the type specified
    """
    if not isinstance(type, int):
        raise TypeError('Type is not an int')

    if type == I4:
        return I4Encoder
    elif type == I8:
        return I8Encoder
    elif type == IA4:
        return IA4Encoder
    elif type == IA8:
        return IA8Encoder
    elif type == RGB565:
        return RGB565Encoder
    elif type == RGB5A3:
        return RGB5A3Encoder
    elif type == RGBA8:
        return RGBA8Encoder
    elif type == CI4:
        raise ValueError('CI4 is not supported')
    elif type == CI8:
        raise ValueError('CI8 is not supported')
    elif type == CI14x2:
        raise ValueError('CI14x2 is not supported')
    elif type == CMPR:
        raise ValueError('CMPR is not supported')
    else:
        raise ValueError('Unrecognized type')
