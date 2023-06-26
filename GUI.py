import sys, os, shutil, pathlib
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QFileDialog, QWidget, QMessageBox, QVBoxLayout, QScrollArea
from PyQt6.QtGui import QAction, QIcon
from test import extractPDF, createMockTest, createQCards, summarizePDF
from PyQt6.QtCore import Qt


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
        self.buttonMock.clicked.connect(self.mockTest)
        self.buttonCard.clicked.connect(self.qCards)
        self.buttonSummarize.clicked.connect(self.summarize)

    #Add a pdf to the list
    def addPDF(self):
        #Select file
        fname = QFileDialog.getOpenFileName(self, 'Open file', "${HOME}$", "PDF Files (*.pdf)")
        #Copy file to pdfs folder
        currDir = os.getcwd()
        shutil.copy(fname[0], currDir + "/pdfs")
        self.showPDFs()

    #Removes selected pdf from the list
    def removePDF(self):

        #Check if folder has files
        numFiles = 0;
        path = pathlib.Path('./pdfs')
        for entry in path.iterdir():
            numFiles+=1
        
        #Checks if folder has files and there is a selected item
        if numFiles > 0 and not(self.listPDF.currentItem() is None):

            #Gets selected item
            currentText = self.listPDF.currentItem().text()

            #Searches for item in folder
            path = pathlib.Path('./pdfs')
            currDir = os.getcwd() + "/pdfs"
            for entry in path.iterdir():
                if entry.name == currentText:
                    os.remove(currDir + "/" + currentText)
            self.showPDFs()
        else:
            print("No files!")
                
    #Function that updates display for the pdf list
    def showPDFs(self):
        self.listPDF.clear()
        path = pathlib.Path('./pdfs')
        for i, entry in enumerate(path.iterdir()):
            if entry.is_file():
                self.listPDF.insertItem(i, entry.name)
    
    def mockTest(self):
        text = self.listPDF.currentItem().text()
        text = extractPDF("pdfs/"+text)
        self.popup(createMockTest(text), "MockTest")
        # self.popup("text", "text")
    def qCards(self):
        text = self.listPDF.currentItem().text()
        text = extractPDF("pdfs/"+text)
        self.popup(createQCards(text, 5), "Qcards")

    def summarize(self):
        text = self.listPDF.currentItem().text()
        text = extractPDF("pdfs/"+text)
        self.popup(summarizePDF(text), "PDFSummary")
    
    def popup(self, text, title):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(text)
        scroll_area = QScrollArea()

        # widget = QWidget()
        # widget.setLayout(QVBoxLayout())
        # widget.layout().addWidget(msg)
        scroll_area.setWidget(msg)
        scroll_area.show()
        msg.exec()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())