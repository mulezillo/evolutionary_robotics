import random
import time
import numpy as np
import pyrosim.pyrosim as pyrosim
import os
import constants as c


class SOLUTION:
    def __init__(self, unique_id):
        # multiply by 2 and subtract 1 maps [0, 1] to [-1, 1]
        self.weights = 2 * np.random.rand(c.NUM_SENSOR_NEURONS, c.NUM_MOTOR_NEURONS) - 1  # 3 rows 2 columns
        self.fitness = 0
        self.id = unique_id

    def set_id(self, new_id):
        self.id = new_id

    def start_simulation(self, display_type: str):
        self.create_world()
        self.create_body()
        self.create_brain()

        # this is confusing and I hate it. This should never be done like this. makes it so hard to debug/understand.
        # and there is really no reason to do this... other than bad architecture of the code base.
        # don't ever do this...
        # extra args lets you kick this off, then start another. also supress warning.
        os.system(f"python3 simulate.py {display_type} {self.id} 2&>1 &")

    def wait_for_sim_to_end(self):
        fitness_filename = f"fitness_{self.id}.txt"
        # wait until file is there
        while not os.path.exists(fitness_filename):
            time.sleep(0.01)

        fitness_file = open(fitness_filename, "r")
        self.fitness = float(fitness_file.read())
        print(f"\n{self.id} fitness: {self.fitness}")
        fitness_file.close()

        # delete file after reading
        os.system(f"rm {fitness_filename}")
        print(f"fitness file {self.id} deleted")

    @DeprecationWarning  # not using this anymore
    def evaluate(self, display_type: str):
        self.create_world()
        self.create_body()
        self.create_brain()

        # this is confusing and I hate it. This should never be done like this. makes it so hard to debug/understand.
        # and there is really no reason to do this... other than bad architecture of the code base.
        # don't ever do this...
        os.system(f"python3 simulate.py {display_type} {self.id} &")  # let's you kick this off, then start another

        fitness_filename = f"fitness_{self.id}.txt"
        # wait until file is there
        while not os.path.exists(fitness_filename):
            time.sleep(0.01)

        fitness_file = open(fitness_filename, "r")
        self.fitness = float(fitness_file.read())
        fitness_file.close()

    def create_world(self):
        pyrosim.Start_SDF("world.sdf")
        self.create_box(name="Box", y=5)
        pyrosim.End()

    def create_body(self):
        pyrosim.Start_URDF("body.urdf")
        self.create_box(name="Torso", z=1)  # x = 1.5, z = 1.5

        # first link uses absolute coordinate, all subsequent links use relative
        pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute", position=[0, -0.5, 1], jointAxis="1 0 0")
        self.create_box(name="BackLeg", y=-0.5, z=0, l=0.2, w=1, h=0.2)
        pyrosim.Send_Joint(name="BackLeg_LowerBackLeg", parent="BackLeg", child="LowerBackLeg", type="revolute", position=[0, -1, 0], jointAxis="1 0 0")
        self.create_box(name="LowerBackLeg", z=-0.5, l=0.2, w=0.2, h=1)

        # this is another first link in this caseBackLegBackLeg
        pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute", position=[0, 0.5, 1], jointAxis="1 0 0") #2, 0, 1
        self.create_box(name="FrontLeg", y=0.5, z=0, l=0.2, w=1, h=0.2)
        pyrosim.Send_Joint(name="FrontLeg_LowerFrontLeg", parent="FrontLeg", child="LowerFrontLeg", type="revolute", position=[0, 1, 0], jointAxis="1 0 0") #2, 0, 1
        self.create_box(name="LowerFrontLeg", z=-0.5, l=0.2, w=0.2, h=1)

        # first link
        pyrosim.Send_Joint(name="Torso_LeftLeg", parent="Torso", child="LeftLeg", type="revolute", position=[-0.5, 0, 1], jointAxis="0 1 0") #2, 0, 1
        self.create_box(name="LeftLeg", x=-0.5, z=0, l=1, w=0.2, h=0.2)
        pyrosim.Send_Joint(name="LeftLeg_LowerLeftLeg", parent="LeftLeg", child="LowerLeftLeg", type="revolute", position=[-1, 0, 0], jointAxis="0 1 0") #2, 0, 1
        self.create_box(name="LowerLeftLeg", z=-0.5, l=0.2, w=0.2, h=1)

        # also first link
        pyrosim.Send_Joint(name="Torso_RightLeg", parent="Torso", child="RightLeg", type="revolute", position=[0.5, 0, 1], jointAxis="0 1 0") #2, 0, 1
        self.create_box(name="RightLeg", x=0.5, z=0, l=1, w=0.2, h=0.2)
        pyrosim.Send_Joint(name="RightLeg_LowerRightLeg", parent="RightLeg", child="LowerRightLeg", type="revolute", position=[1, 0, 0], jointAxis="0 1 0") #2, 0, 1
        self.create_box(name="LowerRightLeg", z=-0.5, l=0.2, w=0.2, h=1)

        pyrosim.End()

    def create_brain(self):
        pyrosim.Start_NeuralNetwork(f"brain_{self.id}.nndf")

        # pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
        # pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLeg")
        # pyrosim.Send_Sensor_Neuron(name=2, linkName="FrontLeg")
        # pyrosim.Send_Sensor_Neuron(name=3, linkName="LeftLeg")
        # pyrosim.Send_Sensor_Neuron(name=4, linkName="RightLeg")

        # only the 4 lower legs touch the ground, so let's just put sensors on them (not the middle legs commented
        # out above)
        pyrosim.Send_Sensor_Neuron(name=0, linkName="LowerBackLeg")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="LowerFrontLeg")
        pyrosim.Send_Sensor_Neuron(name=2, linkName="LowerLeftLeg")
        pyrosim.Send_Sensor_Neuron(name=3, linkName="LowerRightLeg")

        pyrosim.Send_Motor_Neuron(name=4, jointName="Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name=5, jointName="Torso_FrontLeg")
        pyrosim.Send_Motor_Neuron(name=6, jointName="Torso_LeftLeg")
        pyrosim.Send_Motor_Neuron(name=7, jointName="Torso_RightLeg")
        pyrosim.Send_Motor_Neuron(name=8, jointName="BackLeg_LowerBackLeg")
        pyrosim.Send_Motor_Neuron(name=9, jointName="FrontLeg_LowerFrontLeg")
        pyrosim.Send_Motor_Neuron(name=10, jointName="LeftLeg_LowerLeftLeg")
        pyrosim.Send_Motor_Neuron(name=11, jointName="RightLeg_LowerRightLeg")

        for row in range(c.NUM_SENSOR_NEURONS):
            # we are iterating over sensors by sensor integer name. ugly, as always
            for column in range(c.NUM_MOTOR_NEURONS):
                pyrosim.Send_Synapse(
                    # kind of ugly name matching here... column + 5
                    sourceNeuronName=row, targetNeuronName=column + c.NUM_SENSOR_NEURONS, weight=self.weights[row][column])
        pyrosim.End()

    def mutate(self):
        ran_row = random.randint(0, c.NUM_SENSOR_NEURONS - 1)
        ran_col = random.randint(0, c.NUM_MOTOR_NEURONS - 1)
        self.weights[ran_row][ran_col] = 2 * random.random() - 1

    @staticmethod
    def create_box(name: str, x: float = 0, y: float = 0, z: float = 0.5, l: float = 1, w: float = 1, h: float = 1):
        pyrosim.Send_Cube(name=f"{name}", pos=[x, y, z], size=[l, w, h])
    
