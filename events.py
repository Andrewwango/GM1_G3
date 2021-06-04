"""
Class containing event types for classification
"""
from enum import Enum

class Events(Enum):
    """
    Enumeration class containing event types:
    Step up/down, eating, glitches.
    """
    STEPUP = 0
    STEPDOWN = 1
    EATING = 2
    GLITCH = 3