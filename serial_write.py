import serial
import RPi.GPIO as GPIO
import time

ser=serial.Serial("/dev/ttyACM1",9600)  #change ACM number as found from ls /dev/tty/ACM*


msg = b"apple"
while True:


    ser.write(b'132\n1')


    time.sleep(5)