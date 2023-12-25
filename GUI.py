import sys, os, shutil, pathlib
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QFileDialog, QWidget, QVBoxLayout, QDialog, QLabel, QPushButton
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
        self.setFixedSize(865, 685)

        self.showPDFs()
        self.showPDFText()

        #Setup window
        self.stackedWidget.setCurrentWidget(self.home)
        
        #Events

        #Home buttons
        self.listPDF.itemClicked.connect(self.showPDFText)
        self.buttonAddPDF.clicked.connect(self.addPDF)
        self.buttonRemovePDF.clicked.connect(self.removePDF)
        self.buttonMock.clicked.connect(self.mockTest)
        self.buttonCard.clicked.connect(self.qCards)
        self.buttonSummarize.clicked.connect(self.summarize)
        self.buttonGoSettings.clicked.connect(self.goSettings)

        #Settings buttons
        self.buttonSaveSettings.clicked.connect(self.goHome)

        #Summary buttons
        self.buttonHome.clicked.connect(self.goHome)

        #Qcard buttons
        self.buttonHome_2.clicked.connect(self.goHome)

        #Mock test buttons
        self.buttonHome_3.clicked.connect(self.goHome)

    #Add a pdf to the list
    def addPDF(self):
        #Select file
        fname = QFileDialog.getOpenFileName(self, 'Open file', "${HOME}$", "PDF Files (*.pdf)")
        #Copy file to pdfs folder
        if (fname[0] != ''):
            currDir = os.getcwd()
            shutil.copy(fname[0], currDir + "/pdfs")
            self.showPDFs()
        else:
            print("File not selected!")

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
            self.showPDFText()
        else:
            print("No files!")

    #Shows the text of a PDF
    def showPDFText(self):
        if not(self.listPDF.currentItem() is None):
            pdfText = extractPDF("pdfs/"+self.listPDF.currentItem().text())
        else:
            pdfText = ""
        self.showText.setText(pdfText)
                
    #Function that updates display for the pdf list
    def showPDFs(self):
        self.listPDF.clear()
        path = pathlib.Path('./pdfs')
        for i, entry in enumerate(path.iterdir()):
            if entry.is_file():
                self.listPDF.insertItem(i, entry.name)
        self.listPDF.setCurrentRow(0)
    
    def mockTest(self):
        if len(self.showText.toPlainText()) != 0:
            self.stackedWidget.setCurrentWidget(self.mocktest)
        else:
            self.popup("No PDF selected!", "Error!")
        #if not(self.showText.toPlainText() is None):
        #    text = self.showText.toPlainText()
        #    self.popup(createMockTest(text), "MockTest")
        #else:
        #    print("No PDF selected")

    def qCards(self):
        if len(self.showText.toPlainText()) != 0:
            numCards = self.numCards.value()
            response = "Topic: What percentage of daily activities is based on the habit system? Answer: 40 percent of daily activities are based on the habit system. Topic: What are habitual actions? Answer: Habitual actions are tasks performed without conscious thought, such as driving a car or riding a bike instinctively. Topic: Why is it important to build good habits and remove bad habits? Answer: Building good habits and removing bad habits is crucial as habits can have a profound impact on one's life."
            self.stackedWidget.setCurrentWidget(self.qcards)
            
        else:
            self.popup("No PDF selected!", "Error!")
        #if not(self.showText.toPlainText() is None):
        #    text = self.showText.toPlainText()
        #    numCards = self.numCards.value()
        #    self.popup(createQCards(text, numCards), "Qcards")
        #else:
        #    print("No PDF selected")

    def summarize(self):
        if len(self.showText.toPlainText()) != 0:
            text = self.showText.toPlainText()
            type = self.summarizeType.currentText()
            self.summaryTextBrowser.setText(summarizePDF(text, type))
            self.stackedWidget.setCurrentWidget(self.summary)
        else:
            self.popup("No PDF selected!", "Error!")
        #if not(self.showText.toPlainText() is None):
        #    text = self.showText.toPlainText()
        #    type = self.summarizeType.currentText()
        #    self.popup(summarizePDF(text, type), "PDFSummary")
        #else:
        #    print("No PDF selected")

    #Change to home window
    def goSettings(self):
        self.stackedWidget.setCurrentWidget(self.settings)

    #Change to home window
    def goHome(self):
        self.stackedWidget.setCurrentWidget(self.home)
    
    #Default popup window
    def popup(self, text, title):
        msg = QDialog()
        msg.setWindowTitle(title)

        layout = QVBoxLayout()
        label = QLabel(text, msg)
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        button = QPushButton("Close")
        button.clicked.connect(msg.accept)

        layout.addWidget(label)
        layout.addWidget(button)

        msg.setLayout(layout)
        msg.setFixedSize(200, 100)

        msg.exec()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())