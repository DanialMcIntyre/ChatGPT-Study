import sys, os, shutil, pathlib
from PyQt6 import QtWidgets, uic, QtCore, QtGui
from PyQt6.QtWidgets import QFileDialog, QWidget, QVBoxLayout, QDialog, QLabel, QPushButton
from PyQt6.QtGui import QAction, QIcon
from test import extractPDF, createMockTest, createQCards, summarizePDF
from PyQt6.QtCore import Qt
from functools import partial

qtcreator_file  = "window.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):

    cardQuestions = []
    cardAnswers = []
    cardStatus = []

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
        self.buttonHome_2.clicked.connect(self.goHomeCard)

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
            self.drawQCards()
            self.cardQuestions = []
            self.cardAnswers = []
            self.cardStatus = []

            #Create new pages for each card
            numCards = self.numCards.value()
            for i in range(0, numCards):
                self.drawCard(i)
            self.cards.setCurrentIndex(0)

            response = "Topic: What percentage of daily activities is based on the habit system? Answer: 40 percent of daily activities are based on the habit system. Topic: What are habitual actions? Answer: Habitual actions are tasks performed without conscious thought, such as driving a car or riding a bike instinctively. Topic: Why is it important to build good habits and remove bad habits? Answer: Building good habits and removing bad habits is crucial as habits can have a profound impact on one's life."
            for i in range(0, numCards):
                #Get the question
                startIndex = response.find("Topic: ")
                endIndex = response.find("Answer: ")
                question = response[startIndex + 7:endIndex]
                #Get the answer
                response = response[endIndex:]
                nextStartIndex = response.find("Topic: ")
                answer = response[8:nextStartIndex]
                response = response[nextStartIndex:]

                self.cardQuestions[i].setText(question)
                self.cardAnswers[i].setText(answer)
                self.cardStatus.append(1)
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

    #Change to home window from QCard window
    def goHomeCard(self):
        #Remove all existing pages
        pages = self.cards.count()
        for i in range(pages):
            widget = self.cards.widget(0)
            self.cards.removeWidget(widget)
        self.stackedWidget.setCurrentWidget(self.home)

    #Go to next card
    def nextCard(self):
        self.cards.setCurrentIndex(self.cards.currentIndex() + 1)
    
    #Go to next card
    def backCard(self):
        self.cards.setCurrentIndex(self.cards.currentIndex() - 1)

    def flipCard(self, index):
        if self.cardStatus[index] == 1:
            self.cardStatus[index] = 0
            self.cardQuestions[index].setHidden(True)
            self.cardAnswers[index].setHidden(False)
        else:
            self.cardStatus[index] = 1
            self.cardQuestions[index].setHidden(False)
            self.cardAnswers[index].setHidden(True)


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

    def drawQCards(self):
        self.cards = QtWidgets.QStackedWidget(parent=self.frame_10)
        self.cards.setGeometry(QtCore.QRect(10, 10, 441, 361))
        self.cards.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.cards.setAutoFillBackground(False)
        self.cards.setObjectName("cards")

    def drawCard(self, index):
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_" + str(index))

        self.label_6 = QtWidgets.QLabel(parent=self.page_2)
        self.label_6.setGeometry(QtCore.QRect(210, 40, 41, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setObjectName("cardLabel_" + str(index))
        self.label_6.setText("Card " + str(index + 1))

        self.textBrowser = QtWidgets.QTextBrowser(parent=self.page_2)
        self.textBrowser.setGeometry(QtCore.QRect(20, 80, 401, 192))
        self.textBrowser.setObjectName("cardInfoQuestion_" + str(index))
        self.cardQuestions.append(self.textBrowser)
        self.textBrowser = QtWidgets.QTextBrowser(parent=self.page_2)
        self.textBrowser.setGeometry(QtCore.QRect(20, 80, 401, 192))
        self.textBrowser.setObjectName("cardInfoAnswer_" + str(index))
        self.textBrowser.setHidden(True)
        self.cardAnswers.append(self.textBrowser)
        self.buttonNextCard = QtWidgets.QPushButton(parent=self.page_2)
        self.buttonNextCard.setGeometry(QtCore.QRect(260, 320, 75, 30))
        self.buttonNextCard.setObjectName("buttonNextCard_" + str(index))
        self.buttonNextCard.setText("Next")
        self.buttonBackCard = QtWidgets.QPushButton(parent=self.page_2)
        self.buttonBackCard.setGeometry(QtCore.QRect(120, 320, 75, 30))
        self.buttonBackCard.setObjectName("buttonBackCard_" + str(index))
        self.buttonBackCard.setText("Back")
        self.buttonFlipCard = QtWidgets.QPushButton(parent=self.page_2)
        self.buttonFlipCard.setGeometry(QtCore.QRect(190, 280, 75, 30))
        self.buttonFlipCard.setObjectName("buttonFlipCard" + str(index))
        self.buttonFlipCard.setText("Flip")
        self.cards.addWidget(self.page_2)

        self.buttonNextCard.clicked.connect(self.nextCard)
        self.buttonBackCard.clicked.connect(self.backCard)
        self.buttonFlipCard.clicked.connect(partial(self.flipCard, index))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())