import serial
from time import sleep

ser = serial.Serial("/dev/ttyS0", 9600)
while True:
    recieved_data = ser.read(size=23)
    print(recieved_data)
    #ser.write(recieved_data)
