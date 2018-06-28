import sys

from UI import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import os
import serial
import time
from picamera import PiCamera
camera = PiCamera()
camera.resolution=(2592,1944)
camera.start_preview()

ser=serial.Serial("/dev/ttyACM0",115200)

a=0

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
