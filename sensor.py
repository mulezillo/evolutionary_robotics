import numpy as np
import constants as c
import pyrosim.pyrosim as pyrosim


class SENSOR:
    def __init__(self, link_name):
        self.link_name = link_name
        self.values = np.zeros(c.NUM_SUMS)  # this is probably not the best way to do this....

    def get_value(self, time_step: int):
        self.values[time_step] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.link_name)
        print(self.values[time_step])

    def save_values(self):
        np.save(f"{self.link_name}.npy", self.values)
