import constants as c
import pyrosim.pyrosim as pyrosim
import pybullet as p


class MOTOR:
    def __init__(self, joint_name, amplitude: float = 0, frequency: float = 0, offset: float = 0):
        self.joint_name = joint_name
        self.amplitude = amplitude
        self.frequency = frequency
        self.offset = offset

    def set_value(self, angle, robot_id):
        pyrosim.Set_Motor_For_Joint(
            bodyIndex=robot_id,
            jointName=self.joint_name,  # not sure what this b is for. throws keyerror without
            controlMode=p.POSITION_CONTROL,  # position control. could also be velocity.
            targetPosition=angle,  # desired angle
            maxForce=c.MAX_FORCE)  # Nm - max force applied to achieve setpoint
