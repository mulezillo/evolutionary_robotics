import random

import numpy as np
import pyrosim.pyrosim as pyrosim
import os


rows = 3
cols = 2


class SOLUTION:
    def __init__(self):
        # multiply by 2 and subtract 1 maps [0, 1] to [-1, 1]
        self.weights = 2 * np.random.rand(rows, cols) - 1  # 3 rows 2 columns
        self.fitness = 0

    def evaluate(self, display_type: str):
        self.create_world()
        self.create_body()
        self.create_brain()

        # this is confusing and I hate it. This should never be done like this. makes it so hard to debug/understand.
        # and there is really no reason to do this... other than bad architecture of the code base.
        # don't ever do this...
        os.system(f"python3 simulate.py {display_type}")

        fitness_file = open("fitness.txt", "r")
        self.fitness = float(fitness_file.read())
        fitness_file.close()

    def create_world(self):
        pyrosim.Start_SDF("world.sdf")
        self.create_cube(name="Box", y=5)
        pyrosim.End()

    def create_body(self):
        pyrosim.Start_URDF("body.urdf")
        self.create_cube(name="Torso", x=1.5, z=1.5)

        # first link uses absolute coordinate, all subsequent links use relative
        pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute", position=[1, 0, 1])
        self.create_cube(name="BackLeg", x=-0.5, y=0, z=-0.5)

        # this is another first link in this case
        pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute", position=[2, 0, 1])
        self.create_cube(name="FrontLeg", x=0.5, y=0, z=-0.5)
        pyrosim.End()

    def create_brain(self):
        pyrosim.Start_NeuralNetwork("brain.nndf")

        pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLeg")
        pyrosim.Send_Sensor_Neuron(name=2, linkName="FrontLeg")

        pyrosim.Send_Motor_Neuron(name=3, jointName="Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name=4, jointName="Torso_FrontLeg")

        for row in range(rows):
            # we are iterating over sensors by sensor integer name. ugly, as always
            for column in range(cols):
                pyrosim.Send_Synapse(
                    # kind of ugly name matching here... column + 3
                    sourceNeuronName=row, targetNeuronName=column + 3, weight=self.weights[row][column])
        pyrosim.End()

    def mutate(self):
        ran_row = random.randint(0, rows - 1)
        ran_col = random.randint(0, cols - 1)
        self.weights[ran_row][ran_col] = 2 * random.random() - 1

    @staticmethod
    def create_cube(name: str, x: float = 0, y: float = 0, z: float = 0.5, l: float = 1, w: float = 1, h: float = 1):
        pyrosim.Send_Cube(name=f"{name}", pos=[x, y, z], size=[l, w, h])