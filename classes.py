"""
Classes to take weight data in, group and detect events, and present as meals,
providing layers of abstraction from raw data to meal objects.
"""
from constants import *
import event_classification
from events import Events
from api.tool import Patient
import time

class Buffer:
    """
    Buffer: class to store a moving window of past data and extract information from it.
    Methods: reset, latest, earliest, add, average, maDev, score, updateTypicalDev, isEmpty, isFull
    """
    def __init__(self, N):
        """
        Initialise buffer
        Parameters: int : N : length of moving window (i.e. length of autoregressive model)
        """
        self.buffer = []
        self.N = N
        self.typicalDev = 0
    
    def __getitem__(self, key):
        return self.buffer[key]
    
    def reset(self):
        """
        Empty and reset buffer.
        """
        self.buffer = []
        self.typicalDev = 0

    def latest(self): 
        """
        Return most recent buffer reading
        Returns: int : latest buffer reading
        """
        return self.buffer[-1]
    def earliest(self):
        """
        Return first in reading current buffer
        Returns: int : earliest buffer reading
        """
        return self.buffer[0]
    
    def add(self, x):
        """
        Add reading to end of buffer and maintain length
        Parameters: int : x : reading to add
        Returns: None
        """
        self.buffer.append(x)
        if self.N > 0 and len(self.buffer) > self.N:
            self.buffer.pop(0)
    
    def average(self):
        """
        Take average of current buffer
        Parameters: None
        Returns: int : arithmetic mean of current buffer
        """
        return sum(self.buffer)/len(self.buffer)
    
    def maDev(self, avg=None):
        """
        Calculate mean absolute deviation of current buffer about sample mean or avg if given
        Parameters: int : avg (optional) : mean value to take deviation around
        Returns: int : mean absolute deviation of buffer
        """
        avg = avg if avg is not None else self.average()
        return sum([abs(b - avg) for b in self.buffer]) / len(self.buffer)
    
    def score(self, x, useTypical=False):
        """
        Calculate z-score of new sample with respect to the current buffer, using sample
        mean absolute deviation or the typical deviation if useTypical is True
        Parameters: int : x : new incoming sample
                    bool: useTypical (optional) : whether to use stored typical deviation
        Returns: int : z-score of x with respect to current buffer
        """        
        avg = self.average(); dev = self.maDev(avg) if not useTypical else self.typicalDev
        if dev < 1e5: dev = DEFAULT_DEV_WEIGHT
        return abs(x - avg)/dev
    
    def updateTypicalDev(self):
        """
        Update typical deviation as mean absolute deviation of current buffer
        """
        self.typicalDev = self.maDev()
    
    def isEmpty(self):
        """
        Returns whether buffer is empty
        """
        return len(self.buffer) == 0
    
    def isFull(self):
        """
        Returns whether buffer is full
        """
        return len(self.buffer) == self.N

class Event:
    """
    Class to detect events from incoming readings, classify, and store event data.
    Methods: add, end, time_taken, net_change, classify
    Attributes: int : start_time, end_time : time of event start and end
                int : start_weight, end_weight : weight at event start and end
                Buffer : buffer : buffer object containing weight data during event
                Events : eventType : enum of event type after classification
    """
    def __init__(self, prevs, reading):
        """
        Initialise event storing class
        Parameters: list : prevs : any previous readings to add to event data buffer
                    int : reading : current reading to add to event buffer when event starts
        """
        self.start_time = time.time()
        self.end_time = 0
        self.start_weight = prevs[0]
        self.end_weight = 0
        self.buffer = Buffer(INFINITE_LENGTH)
        for prev in prevs: self.buffer.add(prev)
        self.buffer.add(reading)
        self.eventType = None
    
    def add(self, reading):
        """
        Add reading to event data buffer
        Parameters: int : reading : new weight reading
        Returns: None
        """
        self.buffer.add(reading)
    
    def end(self):
        """
        End event and trigger classification.
        """
        self.end_time = time.time()
        self.end_weight = self.buffer[-1]
        self.eventType = self.classify()
        print("Event: ", self.eventType, ", time taken: ", round(self.time_taken(), 2), ", weight diff: ", self.net_change())
    
    def time_taken(self):
        """
        Returns total elapsed time of event.
        """
        return self.end_time - self.start_time
    
    def net_change(self):
        """
        Returns total change of weight between end and start of event.
        """
        return self.buffer[-1] - self.buffer[0]

    def classify(self):
        """
        Returns event type from event classification based on current event.
        """
        return event_classification.detectEventType(self)

        

class Meal:
    """
    Class to store an ongoing meal during eating and manage events
    Methods: updateWithEvent, checkIfIdle, checkIfMealValid, forceToggle, endMeal, reset
    Attributes: bool : ready : whether meal is ready to go
                bool : started : whether meal has been already started
                bool : forceEnd : whether meal has been forced to end
                int : start_time, end_time : time at meal start and end
                int : start_weight, end_weight : weight readings at meal start and end
                int : step_offset : accumulator of any step events occured during meal
                                    which are not food (e.g. phones, bottle etc.)
                int : timeLastAte : time last EATING event occured (for idleness detection)
    """
    def __init__(self):
        """
        Initialise ongoing meal object.
        """
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
        """
        Update meal with new event and start meal
        Parameters : Events : event : new incoming detected event
        Returns : None
        """
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
        """
        Returns whether meal has timed out from idleness
        """
        return (time.time() - self.timeLastAte > MEAL_TIMEOUT_SECS) and self.ready
    
    def checkIfMealValid(self):
        """
        Returns whether meal is valid based on time of meal
        This can be further developed using grouping on an hourly basis
        """
        return ((time.time() - self.start_time > MEAL_LENGTH_SECS) and self.started) or DEMO_MODE
    
    def forceToggle(self, prev):
        """
        Toggle meal start/end when button is pressed in demo mode
        Parameters : int : prev : 
        """
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
        p1 = Patient("Rodger", 30, 33)
        p1.addMeal(1,0,-1* self.weight_change_raw,str(self.tot(self.end_time)))
    def tot(self,t):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))
    def __repr__(self):
        return "Finished meal, start/end time {0},{1}, start/end weight {2},{3}, change {4}, offset {5}, total change: {6} g".format(self.tot(self.start_time), self.tot(self.end_time), self.start_weight, self.end_weight, self.weight_change_raw, self.weight_offset, self.weight_change)
