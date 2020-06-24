''' Used libraries '''
import sys
import ctypes
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pickle
import string
from nltk.corpus import stopwords
from googletrans import Translator

''' Fonts '''
TEXT_FONT = {"Type": "Times", "Size": "20"}
BUTTON_FONT = {"Type": "Times", "Size": "10"}
CONTENT_FONT = {"Type": "Times", "Size": "12"}
RES_FONT = {"Type": "Times", "Size": "18"}
TOOL_TIP = {"Type": "Times", "Size": "10"}

''' Fonts' settings '''
fontContent =QtGui.QFont(CONTENT_FONT["Type"], int(CONTENT_FONT["Size"]), QtGui.QFont.Normal)
fontResult = QtGui.QFont(RES_FONT["Type"], int(RES_FONT["Size"]), QtGui.QFont.Bold)
fontText = QtGui.QFont(TEXT_FONT["Type"], int(TEXT_FONT["Size"]), QtGui.QFont.Bold)
fontButton = QtGui.QFont(BUTTON_FONT["Type"], int(BUTTON_FONT["Size"]), QtGui.QFont.Bold)
QToolTip.setFont(QFont(TOOL_TIP["Type"], int(TOOL_TIP["Size"]))) # It user with the hover event

''' Window' settings '''
HEIGHT = 600
WIDTH = 800

def text_process(mess):
    """
    Takes in a string of text, then performs the following:
    1. Remove all punctuation
    2. Remove all stopwords
    3. Returns a list of the cleaned text
    """
    # Check characters to see if they are in punctuation
    nopunc = [char for char in mess if char not in string.punctuation]

    # Join the characters again to form the string.
    nopunc = ''.join(nopunc)

    # Now just remove any stopwords
    return [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]

class App(QWidget):
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def load_models(self):
        self.knn_model = pickle.load( open( "..\\3_Sample\\finalized_model-knn.sav", "rb" ) )
        self.rn_model = pickle.load( open( "..\\3_Sample\\finalized_model-rn.sav", "rb" ) )
        self.bayes_model = pickle.load( open( "..\\3_Sample\\finalized_model.sav", "rb" ) )
        self.models = { 'K Nearest Neighbors':self.knn_model, 'Neural Network': self.rn_model, 'Naive Bayes': self.bayes_model}

    def __init__(self):
        super().__init__()
        self.load_models()

        ''' Centralize the window and fix a size for it '''
        self.setWindowTitle('Fake News Detector')
        self.setWindowIcon(QIcon('resources\\fake.png'))
        self.setFixedSize(WIDTH, HEIGHT)
        self.center()
        ''' Create Labels: status, port, buttons for opening the client and closing the server '''

        self.imgPath = "resources\\fake_response.png"
        pixmap = QPixmap(self.imgPath)
        pixmap.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # transform = QTransform().rotate(15)
        # pixmap = pixmap.transformed(transform, Qt.SmoothTransformation)
        self.label = QLabel()
        self.label.setScaledContents(True)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setPixmap(pixmap)
        self.label.setMaximumSize(220, 147)
        self.label.move(100,100)

        titleLabel = QLabel()
        titleLabel.setWordWrap(True)
        titleLabel.setText("Fake news detector")
        titleLabel.setFont(fontText)
        titleLabel.setAlignment(Qt.AlignCenter)


        optionsLabel = QLabel()
        optionsLabel.setWordWrap(True)
        optionsLabel.setText("Options:")
        optionsLabel.setFont(QFont("Times", 15, QFont.Bold))

        chooseModel =  QLabel()
        chooseModel.setWordWrap(True)
        chooseModel.setText("Choose Model:")
        chooseModel.setFont(fontContent)

        chooseLang =  QLabel()
        chooseLang.setWordWrap(True)
        chooseLang.setText("Choose Language:")
        chooseLang.setFont(fontContent)


        self.news = QPlainTextEdit()
        self.news.setPlaceholderText("Enter a news that you want to check if it\'s fake or not")
        self.news.setFont(fontContent)

        self.result = QLabel()
        self.result.setWordWrap(True)

        self.comobo_model = QComboBox()
        self.comobo_model.addItems(["Neural Network", "K Nearest Neighbors", "Naive Bayes"])

        self.comobo_lang = QComboBox()
        self.comobo_lang.addItems(["English", "Romanian"])

        self.fakeDetails = QLabel()
        self.fakeDetails.setWordWrap(True)
        self.fakeDetails.move(20,10)

        self.reliableDetails = QLabel()
        self.reliableDetails.setWordWrap(True)
        self.reliableDetails.move(20,20)

        spaceLabel = QLabel()
        spaceLabel.setWordWrap(True)
        spaceLabel.setText("\n")
        spaceLabel.setAlignment(Qt.AlignCenter)

        checkNewsBtn= QPushButton("Check News")
        checkNewsBtn.setAutoDefault(False)
        checkNewsBtn.setFont(fontButton)
        checkNewsBtn.setToolTip('Verify if news is fake or not')
        checkNewsBtn.setIcon(QtGui.QIcon("resources\\library.png"))

        self.viewDetalisBtn= QPushButton("View Details")
        self.viewDetalisBtn.setDisabled(True)
        self.viewDetalisBtn.setAutoDefault(False)
        self.viewDetalisBtn.setFont(fontButton)
        self.viewDetalisBtn.setToolTip('View probability of true label')
        self.viewDetalisBtn.setIcon(QtGui.QIcon("resources\\eye.png"))
    
        ''' Define actions for the buttons '''
        checkNewsBtn.clicked.connect(self.checkNews)
        self.viewDetalisBtn.clicked.connect(self.viewDetails)

        ''' Define layout for the buttons '''
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(checkNewsBtn)
        buttonLayout.addStretch(5)
        buttonLayout.addWidget(self.viewDetalisBtn)
        buttonLayout.addStretch(60)
        buttonLayout.addWidget(self.result) 
        ''' Define layout for the buttons '''
        optionsLayout = QVBoxLayout()
        optionsLayout.addWidget(optionsLabel)
        optionsLayout.addWidget(chooseModel)
        optionsLayout.addWidget(self.comobo_model)
        optionsLayout.addWidget(chooseLang)
        optionsLayout.addWidget(self.comobo_lang)
        optionsLayout.addWidget(spaceLabel)
        optionsLayout.addWidget(spaceLabel)
        optionsLayout.addWidget(spaceLabel)

        ''' Define layout for the details'''
        detailsLayout = QHBoxLayout()
        detailsLayout.addStretch(60)
        detailsLayout.addWidget(self.fakeDetails)
        detailsLayout.addStretch(5)
        detailsLayout.addWidget(self.reliableDetails)
        ''' Define layout for the buttons '''
        comboLayout = QHBoxLayout()
        comboLayout.addStretch(20)
        comboLayout.addWidget(self.comobo_model)
        comboLayout.addStretch(20)

        inputLayout = QHBoxLayout()
        inputLayout.addLayout(optionsLayout)
        inputLayout.addWidget(QLabel(""))
        inputLayout.addWidget(self.news)

        ''' Define the main layout with the texts and main button '''
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(50, 50, 50, 50)
        mainLayout.addWidget(titleLabel)
        mainLayout.addWidget(spaceLabel)
        mainLayout.addLayout(inputLayout)
        mainLayout.addWidget(spaceLabel)
        mainLayout.addLayout(buttonLayout) 
        mainLayout.addLayout(detailsLayout)
        mainLayout.addWidget(spaceLabel)
        mainLayout.addLayout(comboLayout)
        mainLayout.addChildWidget(self.label)
        self.label.move(100,100)
        self.setLayout(mainLayout)
        self.setWindowFlags(self.windowFlags() # Just the minimize button is available
            | QtCore.Qt.WindowMinimizeButtonHint
            | QtCore.Qt.WindowSystemMenuHint)

    def checkNews(self):
        translator = Translator()
        if self.comobo_lang.currentText() =="English":
            self.fakeDetails.setText("")
            self.reliableDetails.setText("")
            self.viewDetalisBtn.setText("View Details")
            self.viewDetalisBtn.setDisabled(False)
            content = self.news.toPlainText()
            result = self.models[self.comobo_model.currentText()].predict([content])
            if result[0] == 1:
                self.result.setText("RELIABLE NEWS")
                self.result.setStyleSheet("color: green") 
                self.result.setFont(fontResult)
                self.result.setAlignment(Qt.AlignCenter)
            else:
                self.result.setText("FAKE NEWS")
                self.result.setStyleSheet("color: red") 
                self.result.setFont(fontResult)
                self.result.setAlignment(Qt.AlignCenter)
            result = self.models[self.comobo_model.currentText()].predict_proba([content])
            self.fake_prob = round(float(result[0][0])*100, 2)
            self.true_prob = round(float(result[0][1])*100, 2)
        else:
            self.fakeDetails.setText("")
            self.reliableDetails.setText("")
            self.viewDetalisBtn.setText("View Details")
            self.viewDetalisBtn.setDisabled(False)
            text_eng = self.news.toPlainText()
            try:
                content = translator.translate(text_eng).text
            except:
                pass
            result = self.models[self.comobo_model.currentText()].predict([content])
            if result[0] == 1:
                self.result.setText("RELIABLE NEWS")
                self.result.setStyleSheet("color: green") 
                self.result.setFont(fontResult)
                self.result.setAlignment(Qt.AlignCenter)
            else:
                self.result.setText("FAKE NEWS")
                self.result.setStyleSheet("color: red") 
                self.result.setFont(fontResult)
                self.result.setAlignment(Qt.AlignCenter)
            result = self.models[self.comobo_model.currentText()].predict_proba([content])
            self.fake_prob = round(float(result[0][0])*100, 2)
            self.true_prob = round(float(result[0][1])*100, 2)

    def viewDetails(self):
        if self.viewDetalisBtn.text() == 'View Details':
            self.fakeDetails.setText("False: \n" + str(self.fake_prob)+" %")
            self.fakeDetails.setStyleSheet("color: red") 
            self.reliableDetails.setText("True: \n" + str(self.true_prob) + " %")
            self.reliableDetails.setStyleSheet("color: green") 
            self.viewDetalisBtn.setText("Hide Details")
        else:
            self.fakeDetails.setText("")
            self.reliableDetails.setText("")
            self.viewDetalisBtn.setText("View Details")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = App() # Start the app
    ex.show() # Show the app's window
    sys.exit(app.exec_()) # Close the window if the user clicks <close> or by the dialog's close event