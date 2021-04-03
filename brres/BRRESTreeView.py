from PyQt5.QtCore import QAbstractItemModel, QFile, QIODevice, QItemSelectionModel, QModelIndex, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTreeView, QAbstractItemView, QVBoxLayout
from PyQt5.QtGui import QStandardItemModel


class BRRESTreeView(QWidget):
    def __init__(self, model, parent=None):
        super(BRRESTreeView, self).__init__(parent)

        headers = ("Title", "Description")

        #file = QFile('default.txt')
        #file.open(QIODevice.ReadOnly)
        #model = BrresModel(headers, file.readAll())
        #file.close()

        self.vboxlayout = QVBoxLayout(self)
        self.vboxlayout.setContentsMargins(0, 0, 0, 0)
        self.vboxlayout.setSpacing(0)

        self.view = QTreeView()
        self.view.setAlternatingRowColors(True)
        self.view.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.view.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.view.setAnimated(True)
        self.view.setAllColumnsShowFocus(True)
        self.view.setObjectName("view")

        self.view.setModel(model)
        for column in range(model.columnCount()):
            self.view.resizeColumnToContents(column)

        self.vboxlayout.addWidget(self.view)
        self.setLayout(self.vboxlayout)

        #self.exitAction.triggered.connect(QApplication.instance().quit)

        #self.view.selectionModel().selectionChanged.connect(self.updateActions)

        #self.actionsMenu.aboutToShow.connect(self.updateActions)
        #self.insertRowAction.triggered.connect(self.insertRow)
        #self.insertColumnAction.triggered.connect(self.insertColumn)
        #self.removeRowAction.triggered.connect(self.removeRow)
        #self.removeColumnAction.triggered.connect(self.removeColumn)
        #self.insertChildAction.triggered.connect(self.insertChild)

        #self.updateActions()

    def insertChild(self):
        index = self.view.selectionModel().currentIndex()
        model = self.view.model()

        if model.columnCount(index) == 0:
            if not model.insertColumn(0, index):
                return

        if not model.insertRow(0, index):
            return

        for column in range(model.columnCount(index)):
            child = model.index(0, column, index)
            model.setData(child, "[No data]", Qt.EditRole)
            if model.headerData(column, Qt.Horizontal) is None:
                model.setHeaderData(column, Qt.Horizontal, "[No header]",
                        Qt.EditRole)

        self.view.selectionModel().setCurrentIndex(model.index(0, 0, index),
                QItemSelectionModel.ClearAndSelect)
        self.updateActions()

    def insertColumn(self):
        model = self.view.model()
        column = self.view.selectionModel().currentIndex().column()

        changed = model.insertColumn(column + 1)
        if changed:
            model.setHeaderData(column + 1, Qt.Horizontal, "[No header]",
                    Qt.EditRole)

        self.updateActions()

        return changed

    def insertRow(self):
        index = self.view.selectionModel().currentIndex()
        model = self.view.model()

        if not model.insertRow(index.row()+1, index.parent()):
            return

        self.updateActions()

        for column in range(model.columnCount(index.parent())):
            child = model.index(index.row()+1, column, index.parent())
            model.setData(child, "[No data]", Qt.EditRole)

    def removeColumn(self):
        model = self.view.model()
        column = self.view.selectionModel().currentIndex().column()

        changed = model.removeColumn(column)
        if changed:
            self.updateActions()

        return changed

    def removeRow(self):
        index = self.view.selectionModel().currentIndex()
        model = self.view.model()

        if (model.removeRow(index.row(), index.parent())):
            self.updateActions()

    def updateActions(self):
        hasSelection = not self.view.selectionModel().selection().isEmpty()
        self.removeRowAction.setEnabled(hasSelection)
        self.removeColumnAction.setEnabled(hasSelection)

        hasCurrent = self.view.selectionModel().currentIndex().isValid()
        self.insertRowAction.setEnabled(hasCurrent)
        self.insertColumnAction.setEnabled(hasCurrent)

        if hasCurrent:
            self.view.closePersistentEditor(self.view.selectionModel().currentIndex())

            row = self.view.selectionModel().currentIndex().row()
            column = self.view.selectionModel().currentIndex().column()
            if self.view.selectionModel().currentIndex().parent().isValid():
                self.statusBar().showMessage("Position: (%d,%d)" % (row, column))
            else:
                self.statusBar().showMessage("Position: (%d,%d) in top level" % (row, column))


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setCentralWidget(BRRESTreeView())
    window.show()
    sys.exit(app.exec_())
