from constants import *
import numpy as np
import time
from read_serial import SerialReader
from classes import Buffer
from matplotlib import pyplot as plt

ser = SerialReader()
buffer = Buffer(INFINITE_LENGTH)
print("Ready")
while True:
    try:
        reading = ser.readline()
        buffer.add(reading)

    except KeyboardInterrupt:
        print('Interrupted')
        np.savetxt('experiments{0}.csv'.format(int(time.time())), buffer.buffer, delimiter=',')
        plt.plot(buffer.buffer)
        plt.show()
        break