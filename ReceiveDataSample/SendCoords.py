
from digi.xbee.devices import XBeeDevice

# serial port: local module
PORT = "/dev/ttyS0"
# baud rate: local module
BAUD_RATE = 9600

REMOTE_NODE_ID = "REMOTE"


def main():
    print(" +------------------------+")
    print(" | XBee Send Data From Pi |")
    print(" +------------------------+\n")

    device = XBeeDevice(PORT, BAUD_RATE)

    try:
        device.open()
        i = 0

        CoordFile = open("coords.txt")

        for line in CoordFile:
            i = i + 1
            DATA_TO_SEND = line
            device.send_data_broadcast(DATA_TO_SEND)
            print("Success on line: ", i, "Containing: ", DATA_TO_SEND)

        CoordFile.close()

    finally:
        if device is not None and device.is_open():
            device.close()


if __name__ == '__main__':
    main()
