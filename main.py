from brres.BRRES import *

if __name__ == '__main__':
    with open("bgB_7801.brres", 'rb') as f:
        brres = BRRES()
        brres.unpack(f.read())