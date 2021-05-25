import numpy as np
from constants import *
import eventClassification
from events import Events
import time

class Buffer:
    def __init__(self, N):
        self.buffer = []
        self.N = N
        self.typicalDev = 0
    def __getitem__(self, key):
        return self.buffer[key]
    def reset(self):
        self.buffer = []
        self.typicalDev = 0
    def latest(self): return self.buffer[-1]
    def earliest(self): return self.buffer[0]
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
        if dev < 1e5: dev = DEFAULT_DEV_WEIGHT
        return abs(x - avg)/dev
    def updateTypicalDev(self):
        self.typicalDev = self.maDev()
    def isEmpty(self):
        return len(self.buffer) == 0
    def isFull(self):
        return len(self.buffer) == self.N

class Event:
    def __init__(self, prevs, reading):
        self.start_time = time.time()
        self.end_time = 0
        self.start_weight = prevs[0]
        self.end_weight = 0
        self.buffer = Buffer(INFINITE_LENGTH)
        for prev in prevs:
            self.buffer.add(prev)
            #print(prev,self.buffer)
        self.buffer.add(reading)
        self.eventType = None
    def add(self, reading):
        self.buffer.add(reading)
    def end(self):
        self.end_time = time.time()
        self.end_weight = self.buffer[-1]
        self.eventType = self.classify()
        print("Event: ", self.eventType, ", time taken: ", round(self.time_taken(), 2), ", weight diff: ", self.net_change())
    def time_taken(self):
        return self.end_time - self.start_time
    def net_change(self):
        return self.buffer[-1] - self.buffer[0]

    def classify(self):
        return eventClassification.detectEventType(self)

        

class Meal:
    def __init__(self):
        self.ready = False
        self.started = False
        self.forceEnd = False
        self.start_time = 0
        self.start_weight = 0
        self.end_time = 0
        self.end_weight = 0
        self.step_offset = 0
        self.timeLastAte = time.time()
    def updateWithEvent(self, event):
        if event.eventType in [Events.STEPDOWN, Events.STEPUP] and self.started:
            self.step_offset += event.net_change()
        if not DEMO_MODE:
            if event.eventType == Events.EATING and self.ready:
                if not self.started:
                    self.started = True
                    self.start_time = event.start_time
                    self.start_weight = event.start_weight
                    print("Meal started")
                self.timeLastAte = time.time()
            elif event.eventType == Events.STEPUP and not self.started:
                self.ready = True
                self.timeLastAte = time.time()

    def checkIfIdle(self):
        return (time.time() - self.timeLastAte > MEAL_TIMEOUT_SECS) and self.ready
    def checkIfMealValid(self):
        print(self.started)
        return ((time.time() - self.start_time > MEAL_LENGTH_SECS) and self.started) or DEMO_MODE
    
    def forceToggle(self, prev):
        if self.started: 
            self.started = False
            self.forceEnd = True
        else:
            self.ready = True
            if self.ready and not self.started:
                self.ready = False
                self.started = True
                self.start_time = time.time()
                self.start_weight = prev
                print("Meal Started")
    
    def endMeal(self, reading):
        print("Meal ended")
        self.end_time = time.time()
        self.end_weight = reading
        success = 0 if self.checkIfMealValid() else -1
        return success
    def reset(self):
        self.forceEnd = False
        self.ready = False
        self.started = False
        self.start_time = 0; self.start_weight = 0; self.end_time = 0; self.end_weight = 0
        self.step_offset = 0

class FinishedMeal:
    def __init__(self, meal):
        self.start_time, self.end_time, self.start_weight, self.end_weight = meal.start_time, meal.end_time, meal.start_weight, meal.end_weight
        self.weight_change_raw = self.end_weight - self.start_weight
        self.weight_offset = meal.step_offset
        self.weight_change = self.weight_change_raw - self.weight_offset
    def __repr__(self):
        return "Finished meal, start/end time {0},{1}, start/end weight {2},{3}, change {4}, offset {5}, total change: {6} g".format(self.start_time, self.end_time, self.start_weight, self.end_weight, self.weight_change_raw, self.weight_offset, self.weight_change)
