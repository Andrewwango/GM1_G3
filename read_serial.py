"""
Class to read sensor data from serial port (via USB)
"""

import serial
from constants import *

class SerialReader:
    """
    SerialReader: class to read sensor data
    Methods: readline, readline_multi, isButtonPressed
    """
    def __init__(self):
        """
        Initialise serial reader from serial port and baud set in constants file
        Parameters: None
        """
        self.reader = serial.Serial(SERIAL_PORT, SERIAL_BAUD)

    def readline(self):
        """
        Reads a single line from serial and convert to int
        Parameters: None
        Returns: int : reading in grams
        """
        strl = str(self.reader.readline())
        if strl == "-1":
            return -1
        return int(strl[2:][:-5])
    
    def readline_multi(self):
        """
        Reads a single line of 3 comma separated values from serial and convert to list of ints
        Parameters: None
        Returns: list : 3 readings in grams representing individual sensors and sum
        """
        strl = str(self.reader.readline())[2:][:-5]
        print(strl)
        if strl == "-1":
            return -1
        return [int(i) for i in strl.split(',')]
    
    def isButtonPressed(self, r):
        return r == -1