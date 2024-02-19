from motor import MOTOR
from sensor import SENSOR
import pybullet as p
import pyrosim.pyrosim as pyrosim
from pyrosim.neuralNetwork import NEURAL_NETWORK
import constants as c
import os


class ROBOT:
    def __init__(self, sim_id):
        self.sim_id = sim_id
        self.robotId = p.loadURDF("body.urdf")
        self.nn = NEURAL_NETWORK(f"brain_{self.sim_id}.nndf")
        # apparently we should delete the brain file after it is read
        os.system(f"rm brain_{self.sim_id}.nndf")
        self.sensors = {}
        self.motors = {}
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

    def think(self):
        self.nn.Update()  # this is a function we added to pyrosim

    def act(self):
        for neuron_name in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuron_name):
                joint_name = self.nn.Get_Motor_Neurons_Joint(neuron_name)
                desired_angle = c.MOTOR_JOINT_RANGE * self.nn.Get_Value_Of(neuron_name)
                # annoyingly, these keys are encoded as bytes (b'' string). This is one way to tackle this issue...
                self.motors[joint_name.encode('UTF-8')].set_value(desired_angle, self.robotId)

    def get_fitness(self):
        state_of_link_zero = p.getLinkState(self.robotId, 0)
        position_of_link_zero = state_of_link_zero[0]
        x_coordinate_of_link_zero = position_of_link_zero[0]

        # write to temp file, then move. This way we are sure that we have finished writing to the file before
        # trying to read from it later
        f = open(f"tmp_{self.sim_id}.txt", "w")
        f.write(str(x_coordinate_of_link_zero))
        f.close()
        os.system(f"mv tmp_{self.sim_id}.txt fitness_{self.sim_id}.txt")
