import pybullet as p
import time


if __name__ == "__main__":
    physicsClient = p.connect(p.GUI)
    for i in range(1000):
        p.stepSimulation()
        time.sleep(0.06)
        print(i)
    p.disconnect()
