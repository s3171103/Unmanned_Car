# Import OpenCV2 for image processing
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import serial
import RPi.GPIO as GPIO
import time
# Import numpy for matrices calculations
import numpy as np
import sys
'''
from UI import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import os
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
'''
ser=serial.Serial("/dev/ttyACM0",115200)

# Create Local Binary Patterns Histograms for face recognization
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Load the trained mode
recognizer.read('trainer/trainer.yml')

# Load prebuilt model for Frontal Face
cascadePath = "haarcascade_frontalface_default.xml"

# Create classifier from prebuilt model
faceCascade = cv2.CascadeClassifier(cascadePath);

# Set the font style
font = cv2.FONT_HERSHEY_SIMPLEX

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32

rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(0.1)


# Loop
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # Read the video frame
    im = frame.array

    # Convert the captured frame into grayscale
    gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

    # Get all face from the video frame
    faces = faceCascade.detectMultiScale(gray, 1.2,5)

    # For each face in faces
    for(x,y,w,h) in faces:

        # Create rectangle around the face
        cv2.rectangle(im, (x-20,y-20), (x+w+20,y+h+20), (0,255,0), 4)

        # Recognize the face belongs to which ID
        Id = recognizer.predict(gray[y:y+h,x:x+w])
        print('hihi')
        print(type(Id))
        # Check the ID if exist 
        if(Id[0] == 1):
            Id = "Kid"
        #If not exist, then it is Unknown
        elif(Id[0] == 2):
            Id = "Sam"
        elif(Id[0] == 3):
            Id = "Nina"
        elif(Id[0] == 4):
            Id = "Carolyn"
        else:
            #print(Id)
            Id = "Unknown"

        # Put text describe who is in the picture
        cv2.rectangle(im, (x-22,y-90), (x+w+22, y-22), (0,255,0), -1)
        cv2.putText(im, str(Id), (x,y-40), font, 2, (255,255,255), 3)

    # Display the video frame with the bounded rectangle
    cv2.imshow('im',im)
        # If 'q' is pressed, close program
    if cv2.waitKey(10) & 0xFF == ord('q'):
            break
        
        #elif 0xFF == ord('d'):
        #    ser.write(b'v-')    
        #elif 0xFF == ord('u'):
        #    ser.write(b'v+')      

    rawCapture.truncate(0)

# Stop the camera
# Close all windows
cv2.destroyAllWindows()
