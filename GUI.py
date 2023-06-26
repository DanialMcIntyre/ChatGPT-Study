import sys, os, shutil, pathlib
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QFileDialog, QTextEdit
from PyQt6.QtGui import QAction, QIcon

qtcreator_file  = "window.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Study Assist")

        self.showPDFs()
        self.buttonAddPDF.clicked.connect(self.addPDF)

    def addPDF(self):
        #Select file
        fname = QFileDialog.getOpenFileName(self, 'Open file', "${HOME}$", "PDF Files (*.pdf)")
        #Copy file to pdfs folder
        currDir = os.getcwd()
        shutil.copy(fname[0], currDir + "/pdfs")
        self.showPDFs()

    def showPDFs(self):
        self.listPDF.clear()
        path = pathlib.Path('./pdfs')
        for i, entry in enumerate(path.iterdir()):
            if entry.is_file():
                self.listPDF.insertItem(i, entry.name)
        app.processEvents()

        


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())