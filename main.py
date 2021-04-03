from brres.BRRES import *
from brres.BRRESTreeView import BRRESTreeView
from PyQt5.QtWidgets import QApplication, QMainWindow


if __name__ == '__main__':
    import sys

    with open("bgB_7801.brres", 'rb') as f:
        brres = BRRES()
        brres.unpack(f.read())
        brres.saveAllImagesAsPng()
    
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setCentralWidget(BRRESTreeView(brres.model))
    window.show()
    sys.exit(app.exec_())
