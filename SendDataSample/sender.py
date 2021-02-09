import serial
import time
from xbee import Zigbee

PORT  = "ttyS0"
BAUD_RATE = 9600
ser = serial.Serial(PORT, BAUD_RATE)

while True:
    try:
        data = raw_input("Send:")
        ser.write(data)
    except KeyboardInterrupt:
        ser.close()
        break
