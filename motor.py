import numpy as np
import constants as c
import pyrosim.pyrosim as pyrosim
import pybullet as p


class MOTOR:
    def __init__(self, joint_name, amplitude: float = 0, frequency: float = 0, offset: float = 0):
        self.joint_name = joint_name
        self.values = None
        self.amplitude = amplitude
        self.frequency = frequency
        self.offset = offset
        self.prepare_to_act()

    def prepare_to_act(self):
        self.values = np.array(
            self.amplitude * np.sin(
                self.frequency * np.linspace(c.LINE_SPACE_START, c.LINE_SPACE_END, c.NUM_SUMS) + self.offset))

    def set_value(self, time_step, robot_id):
        pyrosim.Set_Motor_For_Joint(
            bodyIndex=robot_id,
            jointName=self.joint_name,  # not sure what this b is for. throws keyerror without
            controlMode=p.POSITION_CONTROL,  # position control. could also be velocity.
            targetPosition=self.values[time_step],  # desired position
            maxForce=c.MAX_FORCE)  # Nm - max force applied to achieve setpoint

    def save_values(self):
        np.save(f"{self.joint_name}.npy", self.values)
