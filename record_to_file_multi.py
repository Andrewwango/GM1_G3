from constants import *
import numpy as np
import time
from read_serial import SerialReader
from classes import Buffer
from matplotlib import pyplot as plt

ser = SerialReader()
buffer1 = Buffer(INFINITE_LENGTH)
buffer2 = Buffer(INFINITE_LENGTH)
buffer3 = Buffer(INFINITE_LENGTH)

print("Ready")
while True:
    try:
        reading = ser.readline_multi()
        buffer1.add(reading[0])
        buffer2.add(reading[1])
        buffer3.add(reading[2])

    except KeyboardInterrupt:
        print('Interrupted')
        np.savetxt('experiments/experiments{0}-{1}.csv'.format(int(time.time()), 1), buffer1.buffer, delimiter=',')
        np.savetxt('experiments/experiments{0}-{1}.csv'.format(int(time.time()), 2), buffer2.buffer, delimiter=',')
        np.savetxt('experiments/experiments{0}-{1}.csv'.format(int(time.time()), 3), buffer3.buffer, delimiter=',')
        print("Success")
        break