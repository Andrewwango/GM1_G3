from constants import *
from events import Events

def detectEventType(event):
    change = event.net_change()
    short_time = event.time_taken() <= SHORT_TIME_SECS
    if change > STEPCHANGE_THRESH and short_time:
        return Events.STEPUP
    elif change < -STEPCHANGE_THRESH and short_time:
        return Events.STEPDOWN
    elif short_time:
        return Events.GLITCH
    elif not short_time:
        return Events.EATING