import serial
from time import sleep

ser = serial.Serial("/dev/ttyS0", 9600)
while True:
    x = "Hello this is gonna be sent"
    print(x)
    ser.write(x)
