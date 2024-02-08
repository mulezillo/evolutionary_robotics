import math

import pybullet as p
import pybullet_data
import time
import pyrosim.pyrosim as pyrosim
import numpy as np
from math import pi
import random as ran


num_sims = 1000
back_leg_file = "data/back_leg_sensor_values.npy"
front_leg_file = "data/front_leg_sensor_values.npy"

front_leg_angle_file = "data/front_leg_motor_angles.npy"
back_leg_angle_file = "data/back_leg_motor_angles.npy"

f_amplitude = pi/4
f_frequency = 10
f_phase_offset = 0
b_amplitude = pi/4
b_frequency = 10
b_phase_offset = pi/1.5


if __name__ == "__main__":
    physicsClient = p.connect(p.GUI)

    # add path to URDF files
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0, 0, -9.8)

    # add a "floor"
    planeId = p.loadURDF("plane.urdf")
    # add robot
    robotId = p.loadURDF("body.urdf")
    # note that we could load this robot multiple times, create multiple IDs, and add multiple identical robots
    pyrosim.Prepare_To_Simulate(robotId)
    p.loadSDF("world.sdf")
    backLegSensorValues = np.zeros(num_sims)
    frontLegSensorValues = np.zeros(num_sims)

    # motor control values:
    targetAngles = np.sin(np.linspace(0, 2*pi, num_sims)) * (pi/4)  # scalling by pi/4 for some reason
    front_leg_motor_cmds = np.array(f_amplitude * np.sin(f_frequency * np.linspace(0, 2 * pi, num_sims) + f_phase_offset))
    back_leg_motor_cmds = np.array(b_amplitude * np.sin(b_frequency * np.linspace(0, 2 * pi, num_sims) + b_phase_offset))
    # np.save(front_leg_angle_file, front_leg_motor_cmds)
    # np.save(back_leg_angle_file, back_leg_motor_cmds)
    # exit()

    for i in range(num_sims):
        p.stepSimulation()
        # add touch sensor
        # Note: touch sensors only work for non-root links
        backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
        frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")

        t_pose_backleg = front_leg_motor_cmds[i]
        t_pose_frontleg = back_leg_motor_cmds[i]
        pyrosim.Set_Motor_For_Joint(
            bodyIndex=robotId,
            jointName=b"Torso_BackLeg",  # not sure what this b is for. throws keyerror without
            controlMode=p.POSITION_CONTROL,  # position control. could also be velocity.
            targetPosition=t_pose_backleg,  # desired position
            maxForce=50)  #Nm - max force applied to achieve setpoint
        pyrosim.Set_Motor_For_Joint(
            bodyIndex=robotId,
            jointName=b"Torso_FrontLeg",  # not sure what this b is for. throws keyerror without
            controlMode=p.POSITION_CONTROL,  # position control. could also be velocity.
            targetPosition=t_pose_frontleg,  # desired position
            maxForce=50)  #Nm - max force applied to achieve setpoint

        time.sleep(0.05)
    p.disconnect()
    print(f"backLegSensorValues: {backLegSensorValues}")
    np.save(back_leg_file, backLegSensorValues)
    np.save(front_leg_file, frontLegSensorValues)
