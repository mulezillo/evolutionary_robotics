import pybullet as p
import pybullet_data
import time
import pyrosim.pyrosim as pyrosim
import numpy as np


num_sims = 100
back_leg_file = "data/back_leg_sensor_values.npy"
front_leg_file = "data/front_leg_sensor_values.npy"

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
    for i in range(num_sims):
        p.stepSimulation()
        # add touch sensor
        # Note: touch sensors only work for non-root links
        backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
        frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
        time.sleep(0.06)
    p.disconnect()
    print(f"backLegSensorValues: {backLegSensorValues}")
    np.save(back_leg_file, backLegSensorValues)
    np.save(front_leg_file, frontLegSensorValues)
