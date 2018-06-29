import sys
import cv2
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import os
from camera import *

ser=serial.Serial("/dev/ttyACM0",115200)

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        
        self.image=None
        self.startButton.clicked.connect(self.start_webcam)
        self.stopButton.clicked.connect(self.stop_webcam)

        self.horizontalSlider.valueChanged.connect(self.setH)
        self.verticalSlider.valueChanged.connect(self.setV)

    def setH(self):
        h=self.horizontalSlider.value()
        strh='H' + str(h) + '\n'
        print(strh)
        ser.write(strh.encode())
        time.sleep(0.06)
    def setV(self):
        v=self.verticalSlider.value()
        strv='v' + str(v) + '\n'
        ser.write(strv.encode())
        #ser.write(b'v+')
        time.sleep(0.06)
        if a==0:
            camera.stop_preview()
            a=1


    def start_webcam(self):
        self.capture=cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)

        self.timer=QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(5)
    def update_frame(self):
        ret,self.image=self.capture.read()
        self.image=cv2.flip(self.image,1)
        self.displayImage(self.image,1)

    def stop_webcam(self):
        self.timer.stop()
    def displayImage(self,img,window=1):
        qformat=QImage.Format_Indexed8
        if len(img.shape)==3:
            if img.shape[2]==4:
                qformat=QImage.Foramt_RGBA8888
            else:
                qformat=QImage.Format_RGB888

        outImage=QImage(img,img.shape[1],img.shape[0],img.strides[0],qformat)

        outImage=outImage.rgbSwapped()

        if window == 1:
            self.imgLabel.setPixmap(QPixmap.fromImage(outImage))
            self.imgLabel.setScaledContents(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
