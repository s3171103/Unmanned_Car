import sys
import cv2
form PyQt5.QtWidgets import QAppolication, QDialog
from PyQt5.uic import loadUi

class Life2Coding(QDialog):
    def __init__(self):
        super(Life2Coding,self).__init__()
        loadUi('life2coding.ui',self)
        self.image=None
        self.startButton.clicked.connected(self.start_webcam)
        self.stopButton.clicked.connect(self.stop_webcam)


    def start_webcam(self):
        self.capture=cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)

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
                qformat=QImage.Format_RGB8888

        outImage=QImage(img,img.shape[1],img.shape[0],img.strides[0],qformat)

        outImage=outImage.rgbSwapped()

        if window == 1:
            self.imgLabel.setPixmap(QPixmap.fromImage(outImage))
            self.imgLabel.setScaledContesnts(True)


if __name__=='__main__':
    app=QApplication(sys.argv)
    window=Life2Coding()
    window.setWindowTitle('Camera Test')
    window.show()