import serial
from time import sleep

ser = serial.Serial("/dev/ttyS0", 9600)
while True:
    recieved_data = ser.read()
    sleep(.03)
    data_left = ser.inWaiting()
    recieved_data += ser.read(data_left)
    print(recieved_data)
    ser.write(recieved_data)
