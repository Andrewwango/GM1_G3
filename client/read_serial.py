import serial
from constants import *

class SerialReader:
    def __init__(self):
        self.reader = serial.Serial(SERIAL_PORT, SERIAL_BAUD)

    def readline(self):
        return int(str(self.reader.readline())[2:][:-5])