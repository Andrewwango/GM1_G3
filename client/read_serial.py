import serial
from constants import *

class SerialReader:
    def __init__(self):
        self.reader = serial.Serial(SERIAL_PORT, SERIAL_BAUD)

    def readline(self):
        strl = str(self.reader.readline())
        if strl == "-1":
            return -1
        return int(strl[2:][:-5])
    
    def readline_multi(self):
        strl = str(self.reader.readline())[2:][:-5]
        print(strl)
        if strl == "-1":
            return -1
        return [int(i) for i in strl.split(',')]