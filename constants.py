
from math import pi


"""
Constants used in simulation
"""
NUM_SUMS = 1000

# files for control analysis
BACK_LEG_FILE = "data/back_leg_sensor_values.npy"
FRONT_LEG_FILE = "data/front_leg_sensor_values.npy"
FRONT_LEG_ANGLE_FILE = "data/front_leg_motor_angles.npy"
BACK_LEG_ANGLE_FILE = "data/back_leg_motor_angles.npy"

# some control constants
F_AMPLITUDE = pi/4
F_FREQUENCY = 10
F_PHASE_OFFSET = 0
B_AMPLITUDE = pi/4
B_FREQUENCY = F_FREQUENCY/2
B_PHASE_OFFSET = pi/1.5
LINE_SPACE_START = 0
LINE_SPACE_END = 2 * pi

GRAVITY = -9.8
MAX_FORCE = 50

SIM_SLEEP = 0.05
