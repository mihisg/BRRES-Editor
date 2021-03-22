import archive
import sys
import os, os.path
try:
    from PyQt5 import QtCore, QtGui, QtWidgets
except ImportError:
    from PySide2 import QtCore, QtGui, QtWidgets
Qt = QtCore.Qt

if hasattr(QtCore, 'pyqtSlot'): # PyQt
    QtCoreSlot = QtCore.pyqtSlot
    QtCoreSignal = QtCore.pyqtSignal
else: # PySide2
    QtCoreSlot = QtCore.Slot
    QtCoreSignal = QtCore.Signal





def module_path():
    """
    This will get us the program's directory, even if we are frozen
    using PyInstaller
    """

    if hasattr(sys, 'frozen') and hasattr(sys, '_MEIPASS'):  # PyInstaller
        if sys.platform == 'darwin':  # macOS
            # sys.executable is /x/y/z/puzzle.app/Contents/MacOS/puzzle
            # We need to return /x/y/z/puzzle.app/Contents/Resources/

            macos = os.path.dirname(sys.executable)
            if os.path.basename(macos) != 'MacOS':
                return None

            return os.path.join(os.path.dirname(macos), 'Resources')

    if __name__ == '__main__':
        return os.path.dirname(os.path.abspath(sys.argv[0]))

    return None





class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setupMenus()
        #path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Choose the first folder ...')
        with open("bgA_7808.arc", 'rb') as arcData:
            data = arcData.read()
        arc = archive.U8()
        arc._load(data)
        brresData = None
        brres = archive.U8()

        for key, value in arc.files:
            if value is None:
                continue
            elif key.endswith('.brres'):
                brresData = value
        
        #print(brresData)
        if brresData is not None:
            brres._load(brresData)
        #    for key, value in brres.files:
        #        if value is None:
        #            continue
        #        print("Key: {}\n".format(key))
        
        self.updateAllWidgets()
        #self.setupWidgets()
    
    def setupMenus(self):
        fileMenu = self.menuBar().addMenu("&File")
        fileMenu.addAction("Open folders ...", self.setupMenus, QtGui.QKeySequence('Ctrl+O'))

    def updateAllWidgets(self):
        self.widget = QtWidgets.QWidget()
        #self.widget.setLayout(layout)
        self.setCentralWidget(self.widget)


#############################################################################################
####################################### Main Function #######################################


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setAttribute(Qt.AA_DisableWindowContextHelpButton)

    # go to the script path
    path = module_path()
    if path is not None:
        os.chdir(path)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    app.deleteLater()
