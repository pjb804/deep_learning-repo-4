import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt 
import time
import cv2, imutils

main = uic.loadUiType("./main.ui")[0]
manual= uic.loadUiType("./manual.ui")[0]
log = uic.loadUiType("./log.ui")[0]

class  Main (QMainWindow, main):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pixmap = QPixmap()

        #camera setting
        self.camera = Camera(self)
        self.camera.daemon = True
        self.camera.update.connect(self.updateCamera)
        
        # move the page
        self.btn_manual.clicked.connect(self.openManualMode) 
        self.btn_history.clicked.connect(self.openLog)

        warningLabel = [self.safetyHat, self.securityChain, self.safetyGlass, self.weldingHelmet, 
                        self.fireFreezer, self.sparkProof, self.fire, self.flammable, 
                        self.fallingDanger, self.load]
        
        for label in warningLabel:
            text = label.text()
            self.isViolated(label, text)
            self.isSolved(label, text)

        ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def openManualMode(self):
        self.manual_window = Manual()
        self.manual_window.show()

    def openLog(self):
        self.log_window = Log()
        self.log_window.show()
    
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def openCamera(self):
        self.camera.running = True
        self.camera.start()
        self.video= cv2.VideoCapture(-1)

        
    def updateCamera(self):
        ret, img = self.video.read()
        if ret:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            h,w,c = img.shape
            qimage = QImage(img.data, w, h, w*c, QImage.Format_RGB888)

            self.pixmap = self.pixmap.fromImage(qimage)
            self.pixmap = self.pixmap.scaled(self.camera.width(), self.camera.height())

            self.camera.setPixmap(self.pixmap)

    ''' change the text box of color when it violated '''
    def changeColor(self, box, text):
        box.setStyleSheet("background-color: #CA3433;") #change the color of background
        box.setText(text + " 위반")

        
    ''' return back the text box status when it solved '''
    def solved(self, box, text):
        box.setStyleSheet("background-color: transparent;")
        box.setText(text)
        

    '''
    1. check if violated
    2. Yes -> change
    3. No -> nothing change
    '''
    def isViolated(self, box, text):
        # in database, if some event happened -> get the Name of ID -> find the match word -> changeColor
         
        self.changeColor(box, text)
        

    def isSolved(self, box, text):
        
        self.solved(box, text)


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    
class Manual(QMainWindow, manual):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class Log (QMainWindow, log):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class Camera(QThread):
    update = pyqtSignal()

    def __init__(self, sec=0, parent=None):
        super().__init__()
        self.main = parent
        self.running = True
    
    def run(self):
        count = 0
        while self.running == True:
            self.update.emit()
            time.sleep(1)
    
    def stop(self):
        self.running = False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindows = Main()
    myWindows.show()

    sys.exit(app.exec_())

