from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import pickle
import string
from nltk.corpus import stopwords
from googletrans import Translator
from google.cloud import translate_v2 as translate
translate_client = translate.Client()

''' Fonts '''
TEXT_FONT = {"Type": "Times", "Size": "20"}
BUTTON_FONT = {"Type": "Times", "Size": "10"}
CONTENT_FONT = {"Type": "Times", "Size": "15"}
RES_FONT = {"Type": "Times", "Size": "18"}
TOOL_TIP = {"Type": "Times", "Size": "10"}

''' Fonts' settings '''
fontContent =QFont(CONTENT_FONT["Type"], int(CONTENT_FONT["Size"]), QFont.Normal)
fontResult = QFont(RES_FONT["Type"], int(RES_FONT["Size"]),QFont.Bold)
fontText = QFont(TEXT_FONT["Type"], int(TEXT_FONT["Size"]), QFont.Bold)
fontButton = QFont(BUTTON_FONT["Type"], int(BUTTON_FONT["Size"]), QFont.Bold)
QToolTip.setFont(QFont(TOOL_TIP["Type"], int(TOOL_TIP["Size"]))) # It user with the hover event
def clickable(widget):
    
        class Filter(QObject):
        
            clicked = pyqtSignal()
         
            def eventFilter(self, obj, event):
           
                if obj == widget:
                    if event.type() == QEvent.MouseButtonRelease:
                       if obj.rect().contains(event.pos()):
                           self.clicked.emit()
                           # The developer can opt for .emit(obj) to get the object within the slot.
                           return True
             
                return False
       
        filter = Filter(widget)
        widget.installEventFilter(filter)
        return filter.clicked

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

class ExampleWindow(QMainWindow):
    def load_models(self):
        self.knn_model = pickle.load( open( "resources\\models\\finalized_model-knn.sav", "rb" ) )
        self.rn_model = pickle.load( open( "resources\\models\\finalized_model-rn.sav", "rb" ) )
        self.bayes_model = pickle.load( open( "resources\\models\\finalized_model.sav", "rb" ) )
        self.models = { 'K Nearest Neighbors':self.knn_model, 'Neural Network': self.rn_model, 'Naive Bayes': self.bayes_model}
    
    def __init__(self, windowsize):
        super().__init__()
        self.windowsize = windowsize
        self.initFrame()
        self.load_models()
        self.initWidgets()
    
    def initFrame(self):
        self.setFixedSize(self.windowsize)
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.FramelessWindowHint)
        # set background image
        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        pixmap1 = QPixmap('resources\\background _f.jpg')
        pixmap1 = pixmap1.scaledToWidth(self.windowsize.width())
        self.background = QLabel()
        self.background.setPixmap(pixmap1)
        layout_box = QHBoxLayout(self.widget)
        layout_box.setContentsMargins(0, 0, 0, 0)
        layout_box.addWidget(self.background)

        #add grey bar on top
        pixmap3 = QPixmap('resources\\pngwave.png')
        pixmap3.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.bar = QLabel(self.widget)
        self.bar.setScaledContents(True)
        self.bar.setPixmap(pixmap3)
        self.bar.move(0,-30)
        self.bar.setMinimumSize(1500,90)

        #add close button
        pixmap2 = QPixmap('resources\\close.png')
        pixmap2.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.closeBtn = QLabel(self.widget)
        self.closeBtn.setScaledContents(True)
        self.closeBtn.setPixmap(pixmap2)
        self.closeBtn.setMaximumSize(25,25)
        p = self.geometry().topRight() -  self.closeBtn.geometry().topRight() +  QPoint(-6, 4)
        self.closeBtn.move(p)
        self.closeBtn.setCursor(QCursor(Qt.PointingHandCursor))
        clickable(self.closeBtn).connect(self.close)

        #add minimize button
        pixmapMinus = QPixmap('resources\\minus.png')
        pixmapMinus.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.minimize = QLabel(self.widget)
        self.minimize.setScaledContents(True)
        self.minimize.setPixmap(pixmapMinus)
        self.minimize.setMaximumSize(25,30)
        p = self.geometry().topRight() -  self.minimize.geometry().topRight() + QPoint(-40, 9)
        self.minimize.move(p)
        clickable(self.minimize).connect(self.showMinimized)
        self.minimize.setCursor(QCursor(Qt.PointingHandCursor))

        #add titlebar
        self.titlebar = QLabel(self.widget)
        self.titlebar.setScaledContents(True)
        self.titlebar.setText("Fake News Detector")
        self.titlebar.setWordWrap(True)
        self.titlebar.setAlignment(Qt.AlignCenter)
        self.titlebar.setStyleSheet("color: #d9d9d9")
        self.titlebar.setMinimumSize(180,28)
        p = self.geometry().topLeft() + QPoint(40, 2)
        self.titlebar.move(p)
        self.titlebar.setFont(QFont(CONTENT_FONT["Type"], int(CONTENT_FONT["Size"]), QFont.Bold))

        #add icon on title bar
        pixmap4 = QPixmap('resources\\fake-news.png')
        self.ico = QLabel(self.widget)
        self.ico.setScaledContents(True)
        self.ico.setPixmap(pixmap4)
        self.ico.move(6, 4)
        self.ico.setMaximumSize(25,25)

        #add title of window
        pixmap4 = QPixmap('resources\\title.png')
        self.title = QLabel(self.widget)
        self.title.setScaledContents(True)
        self.title.setPixmap(pixmap4)
        self.title.setMinimumSize(500,50)
        p = self.geometry().topRight()/2 - self.title.geometry().topRight()/2 + QPoint(0, 80)
        self.title.move(p)

        #add horizontal line
        # pixmapline = QPixmap('resources\\line.png')
        # self.line = QLabel(self.widget)
        # self.line.setScaledContents(True)
        # self.line.setPixmap(pixmapline)
        # self.line.setMinimumSize(1000,100)
        # self.line.move(300,100)

    def initWidgets(self):
        #add textbox
        self.news = QPlainTextEdit(self.widget)
        self.news.setPlaceholderText("Enter some news that you want to check if it\'s fake or not")
        self.news.setFont(fontContent)
        self.news.resize(900, 400)
        self.news.setObjectName("news")
        # self.news.setStyleSheet("")
        p = self.geometry().center() - QPoint(300,175)
        self.news.textChanged.connect(self.news_textChanged)
        self.news.move(p)

        #fake news tag
        self.imgPath = "resources\\fake_response.png"
        pixmap = QPixmap(self.imgPath)
        transform = QTransform().rotate(0)
        pixmap = pixmap.transformed(transform, Qt.SmoothTransformation)
        self.fake = QLabel(self.widget)
        self.fake.setScaledContents(True)
        self.fake.setPixmap(pixmap)
        self.fake.setMinimumSize(600, 141)
        p = self.news.geometry().topLeft() + QPoint(160, 120)
        self.fake.move(p)
        self.fake.setHidden(True)

        #reliable news tag
        # self.imgPath = "resources\\true_response.png"
        # pixmap = QPixmap(self.imgPath)
        # transform = QTransform().rotate(45)
        # pixmap = pixmap.transformed(transform, Qt.SmoothTransformation)
        # self.reliable = QLabel(self.widget)
        # self.reliable.setScaledContents(True)
        # self.reliable.setPixmap(pixmap)
        # self.reliable.setMinimumSize(400,400)
        # p = self.news.geometry().topRight() - QPoint(220,90)
        # self.reliable.move(p)
        # self.reliable.setHidden(True)

        self.imgPath = "resources\\true_response.png"
        pixmap = QPixmap(self.imgPath)
        transform = QTransform().rotate(0)
        pixmap = pixmap.transformed(transform, Qt.SmoothTransformation)
        self.reliable = QLabel(self.widget)
        self.reliable.setScaledContents(True)
        self.reliable.setPixmap(pixmap)
        self.reliable.setMinimumSize(600, 141)
        p = self.news.geometry().topLeft() + QPoint(160, 120)
        self.reliable.move(p)
        self.reliable.setHidden(True)

        #check button
        style_btn = "background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 white, stop: 1 grey);\
                                padding: 10px;\
                                border-radius: 10px;"
        checkNewsBtn = QPushButton(self.widget)
        checkNewsBtn.setText("CHECK NEWS")
        checkNewsBtn.setAutoDefault(False)
        checkNewsBtn.setFont(fontButton)
        checkNewsBtn.resize(125,35)
        checkNewsBtn.setStyleSheet(style_btn)
        checkNewsBtn.setToolTip('Verify if news is fake or not')
        checkNewsBtn.setIcon(QIcon("resources\\library.png"))
        checkNewsBtn.clicked.connect(self.checkNews)
        p = self.news.geometry().bottomLeft() + QPoint(0, 40)
        checkNewsBtn.move(p)

        #view details button
        self.viewDetalisBtn = QPushButton(self.widget)
        self.viewDetalisBtn.setText("VIEW DETAILS")    
        self.viewDetalisBtn.setDisabled(True)
        self.viewDetalisBtn.resize(125,35)
        self.viewDetalisBtn.setAutoDefault(False)
        self.viewDetalisBtn.setStyleSheet(style_btn)
        self.viewDetalisBtn.setFont(fontButton)
        self.viewDetalisBtn.setToolTip('View probability of true label')
        self.viewDetalisBtn.setIcon(QIcon("resources\\eye.png"))
        self.viewDetalisBtn.clicked.connect(self.viewDetails)
        p = checkNewsBtn.geometry().topRight() + QPoint(20, 0)
        self.viewDetalisBtn.move(p)

        #fake details label
        self.fakeDetails = QLabel()
        self.fakeDetails.setWordWrap(True)
        self.fakeDetails.move(20,10)
        self.fakeDetails = QLabel(self.widget)
        self.fakeDetails.setWordWrap(True)
        self.fakeDetails.move(20,10)
        self.fakeDetails.setFont(QFont("Times", 20, QFont.Bold))
        self.fakeDetails.setMinimumSize(150, 100)
        p = self.news.geometry().bottomRight()  + QPoint(-300, 20)
        self.fakeDetails.move(p)

        #reliable details label
        self.reliableDetails = QLabel()
        self.reliableDetails.setWordWrap(True)
        self.reliableDetails.move(20,20)
        self.reliableDetails = QLabel(self.widget)
        self.reliableDetails.setWordWrap(True)
        self.reliableDetails.move(20,10)
        self.reliableDetails.setFont(QFont("Times", 20, QFont.Bold))
        self.reliableDetails.setMinimumSize(150, 100)
        p = self.news.geometry().bottomRight()  + QPoint(-150, 20)
        self.reliableDetails.move(p)

        optionsLabel = QLabel(self.widget)
        optionsLabel.setWordWrap(True)
        optionsLabel.setText("Options:")
        optionsLabel.setFont(QFont("Times", 20, QFont.Bold))
        optionsLabel.setStyleSheet("color: white")
        p = self.news.geometry().topLeft()/2  + QPoint(-40, 80)
        optionsLabel.move(p)

        chooseModel =  QLabel(self.widget)
        chooseModel.setWordWrap(True)
        chooseModel.setText("Choose Model:")
        chooseModel.setMinimumSize(300, 30)
        chooseModel.setStyleSheet("color: white")
        chooseModel.setFont(fontContent)
        p = optionsLabel.geometry().bottomLeft() + QPoint(-40, 40)
        chooseModel.move(p)
        
        self.comobo_model = QComboBox(self.widget)
        self.comobo_model.addItems(["Neural Network", "K Nearest Neighbors", "Naive Bayes"])
        self.comobo_model.setItemIcon(0, QIcon("resources\\rn.png"))
        self.comobo_model.setItemIcon(1, QIcon("resources\\knn.png"))
        self.comobo_model.setItemIcon(2, QIcon("resources\\bayes.png"))
        self.comobo_model.setFont(fontButton)
        self.comobo_model.setObjectName("combo_model")
        self.comobo_model.setMinimumSize(180, 20)
        p = chooseModel.geometry().bottomLeft() + QPoint(0, 20)
        self.comobo_model.move(p)

        chooseLang =  QLabel(self.widget)
        chooseLang.setWordWrap(True)
        chooseLang.setText("Choose Language:")
        chooseLang.setMinimumSize(300, 30)
        chooseLang.setStyleSheet("color: white")
        chooseLang.setFont(fontContent)
        p = self.comobo_model.geometry().bottomLeft() + QPoint(0, 40)
        chooseLang.move(p)

        
        self.comobo_lang = QComboBox(self.widget)
        self.comobo_lang.addItems([" ENGLISH", " ROMANIAN"])
        self.comobo_lang.setObjectName("combo_model")
        self.comobo_lang.setMinimumSize(180, 20)
        self.comobo_lang.setItemIcon(0, QIcon("resources\\uk.png"))
        self.comobo_lang.setItemIcon(1, QIcon("resources\\romania.png"))
        self.comobo_lang.setFont(fontButton)
        p = chooseLang.geometry().bottomLeft() + QPoint(0, 20)
        self.comobo_lang.move(p)



    def checkNews(self):
        if self.comobo_lang.currentText() ==" ENGLISH":
            self.fakeDetails.setText("")
            self.reliableDetails.setText("")
            self.viewDetalisBtn.setText("View Details")
            self.viewDetalisBtn.setDisabled(False)
            content = self.news.toPlainText()
            result = self.models[self.comobo_model.currentText()].predict([content])
            self.reliable.setHidden(True)
            self.fake.setHidden(True)
            if result[0] == 1:
                self.reliable.setHidden(False)
            else:
                self.fake.setHidden(False)
            result = self.models[self.comobo_model.currentText()].predict_proba([content])
        else:
            self.fakeDetails.setText("")
            self.reliableDetails.setText("")
            self.viewDetalisBtn.setText("View Details")
            self.viewDetalisBtn.setDisabled(False)
            text_eng = self.news.toPlainText()
            # content = translator.translate(text_eng, src='ro').text
            content = translate_client.translate(text_eng, target_language='eng', source_language='ro')['translatedText']
            result = self.models[self.comobo_model.currentText()].predict([content])
            self.reliable.setHidden(True)
            self.fake.setHidden(True)
            if result[0] == 1:
                self.reliable.setHidden(False)
            else:
                self.fake.setHidden(False)
            result = self.models[self.comobo_model.currentText()].predict_proba([content])
        
        self.fake_prob = round(float(result[0][0])*100, 2)
        self.true_prob = round(float(result[0][1])*100, 2)

    def viewDetails(self):
        if self.viewDetalisBtn.text() == 'View Details':
            self.fakeDetails.setText("Fake: \n" + str(self.fake_prob)+" %")
            self.fakeDetails.setStyleSheet("color: #F44336") 
            self.reliableDetails.setText("Reliable: \n" + str(self.true_prob) + " %")
            self.reliableDetails.setStyleSheet("color: #19aa19") 
            self.viewDetalisBtn.setText("Hide Details")
        else:
            self.fakeDetails.setText("")
            self.reliableDetails.setText("")
            self.viewDetalisBtn.setText("View Details")

    def news_textChanged(self):
        self.fakeDetails.setText("")
        self.reliableDetails.setText("")
        self.viewDetalisBtn.setText("View Details")
        self.reliable.setHidden(True)
        self.fake.setHidden(True)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    qss_file = open('style_file.qss').read()
    app.setStyleSheet(qss_file)
    screensize = app.desktop().availableGeometry().size()
    ex = ExampleWindow(screensize)
    ex.show()

sys.exit(app.exec_())