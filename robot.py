from motor import MOTOR
from sensor import SENSOR
import pybullet as p
import pyrosim.pyrosim as pyrosim
import constants as c


class ROBOT:
    def __init__(self):
        self.sensors = {}
        self.motors = {}
        self.robotId = p.loadURDF("body.urdf")
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.prepare_to_sense()
        self.prepare_to_act()

    def prepare_to_sense(self):
        for link_name in pyrosim.linkNamesToIndices:
            self.sensors[link_name] = SENSOR(link_name)

    def prepare_to_act(self):
        # attach motor to every joint
        # some silly logic to set different controls per assignment 6
        done = False
        for joint_name in pyrosim.jointNamesToIndices:
            self.motors[joint_name] = MOTOR(
                joint_name,
                amplitude=c.F_AMPLITUDE,
                frequency=c.F_FREQUENCY if not done else c.B_FREQUENCY,
                offset=c.F_PHASE_OFFSET)
            done = True

    def sense(self, time_step: int):
        for sensor in self.sensors.values():
            sensor.get_value(time_step)

    def act(self, time_step: int):
        for motor in self.motors.values():
            motor.set_value(time_step, self.robotId)
