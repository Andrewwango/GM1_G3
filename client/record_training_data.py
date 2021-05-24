from constants import *
import numpy as np
import time, csv
from read_serial import SerialReader
from classes import Buffer, Event
from events import Events
from matplotlib import pyplot as plt

ser = SerialReader()
record_buffer = Buffer(INFINITE_LENGTH)
buffer = Buffer(AR_LENGTH)
result_book = []
events = []
eventInProgress = False

def saveline(c, buf):
    result_book.append([c] + buf.buffer)

print("Ready")
while True:
    try:
        reading = ser.readline()
        record_buffer.add(reading)
        if not buffer.isFull(): 
            buffer.add(reading)
            continue
        
        outlier = buffer.score(reading, useTypical=eventInProgress) > OUTLIER_Z_SCORE
        if not eventInProgress:
            buffer.updateTypicalDev()
        if not eventInProgress and outlier:
            eventInProgress = True
            events.append(Event(record_buffer.buffer[-5:], reading))
        elif eventInProgress:
            if outlier:
                events[-1].add(reading)
            else:
                eventInProgress = False
                for _ in range(3):
                    events[-1].buffer.add(ser.readline())
                events[-1].end()
                saveline(0 if events[-1].eventType == Events.STEPUP else 1, events[-1].buffer)
                record_buffer.reset()

        buffer.add(reading)



    except KeyboardInterrupt:
        break

with open("training_data.csv", mode="w", newline='') as f:
    csvwriter = csv.writer(f, delimiter=',')
    for row in result_book:
        csvwriter.writerow(row)