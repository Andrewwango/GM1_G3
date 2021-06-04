"""
Python file containing constants used in information processing model.
"""
# Constants for electronics serial communication
SERIAL_BAUD = 57600             # Baud rate of serial read (sync with Arduino)
SERIAL_PORT = "COM3"            # Comms port of serial read

# Parameters for simple (non ML) event classification
SHORT_TIME_SECS = 2             # Time threshold between steps and eating
STEPCHANGE_THRESH = 50          # Weight threshold between steps and eating

# Parameters for autoregressive model
DEFAULT_DEV_WEIGHT = 3          # Default weight variability (in grams)
OUTLIER_Z_SCORE = 10            # z-score for outlier detection
AR_LENGTH = 10                  # Default length of buffer
INFINITE_LENGTH = -1            # Parameter to pass in when infinite length desired

# Parameters for manual meal end detection (only for demonstration)
MEAL_TIMEOUT_SECS = 99999999    # Time until meal forced to end (in secs)
MEAL_LENGTH_SECS = 0.5          # Min. time for meal to be valid (in secs)

# Constants for demonstration
DEMO_MODE = True                # Whether demo mode (i.e. with manual start/end)