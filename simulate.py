import pybullet as p
import pybullet_data
import time


if __name__ == "__main__":
    physicsClient = p.connect(p.GUI)

    # add path to URDF files
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0, 0, -9.8)

    # add a "floor"
    planeId = p.loadURDF("plane.urdf")
    p.loadSDF("boxes.sdf")
    for i in range(1000):
        p.stepSimulation()
        time.sleep(0.06)
        print(i)
    p.disconnect()
