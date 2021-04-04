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
                        
                    for j in range(0, 4):
                        try:
                            val = i
                            i += 1
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 0 + j*16] = palette[val&3][0]
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 1 + j*16] = palette[val&3][1]
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 2 + j*16] = palette[val&3][2]
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 3 + j*16] = palette[val&3][3]

                            val >>= 2
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 4 + j*16] = palette[val&3][0]
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 5 + j*16] = palette[val&3][1]
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 6 + j*16] = palette[val&3][2]
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 7 + j*16] = palette[val&3][3]

                            val >>= 2
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 8 + j*16] = palette[val&3][0]
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 9 + j*16] = palette[val&3][1]
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 10 + j*16] = palette[val&3][2]
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 11 + j*16] = palette[val&3][3]

                            val >>= 2
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 12 + j*16] = palette[val&3][0]
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 13 + j*16] = palette[val&3][1]
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 14 + j*16] = palette[val&3][2]
                            argbBuf[(((ypixel * w) + xpixel) * 4) + 15 + j*16] = palette[val&3][3]
                        except: print("well")
                    
        self.result = bytes(argbBuffer)
        return self.result
                    
                    
                    
                    
                    