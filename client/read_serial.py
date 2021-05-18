import serial
import time
from enum import Enum

class Events(Enum):
    STEPUP = 1
    STEPDOWN = 2
    EATING = 3
    GLITCH = 4

class Buffer:
    def __init__(self, N):
        self.buffer = []
        self.N = N
        self.typicalDev = 0
    def __getitem__(self, key):
        return self.buffer[key]
    def latest(self): return self.buffer[-1]
    def add(self, x):
        self.buffer.append(x)
        if self.N > 0 and len(self.buffer) > self.N:
            self.buffer.pop(0)
    def average(self):
        return sum(self.buffer)/len(self.buffer)
    def maDev(self, avg=None):
        avg = avg if avg is not None else self.average()
        return sum([abs(b - avg) for b in self.buffer]) / len(self.buffer)
    def score(self, x, useTypical=False):
        avg = self.average(); dev = self.maDev(avg) if not useTypical else self.typicalDev
        return abs(x - avg)/dev
    def updateTypicalDev(self):
        self.typicalDev = self.maDev()
    def isEmpty(self):
        return len(self.buffer) == 0
    def isFull(self):
        return len(self.buffer) == self.N

class Event:
    def __init__(self, prev, reading):
        self.start_time = time.time()
        self.end_time = 0
        self.buffer = Buffer(-1)
        self.buffer.add(prev)
        self.buffer.add(reading)
        self.eventType = None
    def add(self, reading):
        self.buffer.add(reading)
    def end(self):
        self.end_time = time.time()
        self.eventType = self.detectEventType()
        print("Event: ", self.eventType, ", time taken: ", int(self.time_taken()), ", weight diff: ", self.net_change())
    def time_taken(self):
        return self.end_time - self.start_time
    def net_change(self):
        return self.buffer[-1] - self.buffer[0]

    def detectEventType(self):
        change = self.net_change()
        short_time = self.time_taken() <= 5
        if change > 10000 and short_time:
            return Events.STEPUP
        elif change < -10000 and short_time:
            return Events.STEPDOWN
        elif short_time:
            return Events.GLITCH
        elif not short_time:
            return Events.EATING
        

class Meal:
    def __init__(self):
        self.started = False
        self.timeLastAte = 0
    def updateWithEvent(self, event):
        if event.eventType == Events.EATING and self.started: 
            self.timeLastAte = time.time()
        elif event.eventType == Events.STEPUP and not self.started:
            self.started = True
    
    def checkIfIdle(self):
        return (time.time() - self.timeLastAte > 10) and self.started
    def endMeal(self):
        print("Ended")
        self.reset()
    def reset(self):
        self.started = False

ser = serial.Serial('COM3', 57600)
buffer = Buffer(3)
events = []
eventInProgress = False
ongoingMeal = Meal()

print("\n\n\n\n\n\n\n\n\n\n")

while True:
    reading = int(str(ser.readline())[2:][:-5])
    if not buffer.isFull(): 
        buffer.add(reading)
        continue
    outlier = buffer.score(reading, useTypical=eventInProgress) > 100
    if not eventInProgress:
        buffer.updateTypicalDev()
    if not eventInProgress and outlier:
        eventInProgress = True
        #print("EVENT STARTED with reading,avg, ", reading, buffer.average())
        events.append(Event(buffer.latest(), reading))
    elif eventInProgress:
        if outlier:
            events[-1].add(reading)
        else:
            eventInProgress = False
            #print("EVENT ENDED with reading,avg, ", reading, buffer.average())
            events[-1].end()
            ongoingMeal.updateWithEvent(events[-1])
            

    buffer.add(reading)
    #print(buffer.buffer, buffer.average())

    if ongoingMeal.checkIfIdle(): ongoingMeal.endMeal()