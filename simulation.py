from world import WORLD
from robot import ROBOT
import pyrosim.pyrosim as pyrosim
import pybullet_data
import pybullet as p
import constants as c
import time


class SIMULATION:
    def __init__(self):
        self.physicsClient = p.connect(p.GUI)

        # add path to URDF files before creating world and robot (they need the connection + path)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        self.world = WORLD()
        self.robot = ROBOT()

        p.setGravity(0, 0, c.GRAVITY)
        pyrosim.Prepare_To_Simulate(self.robot.robotId)

    def __del__(self):
        p.disconnect()

    def run(self, num_sims: int = c.NUM_SUMS):
        for t in range(num_sims):
            p.stepSimulation()
            self.robot.sense(time_step=t)
            self.robot.think()
            self.robot.act()
            time.sleep(c.SIM_SLEEP)
