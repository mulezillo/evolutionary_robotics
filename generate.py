import pyrosim.pyrosim as pyrosim
import random


def simple_cube(name: str, x: float = 0, y: float = 0, z: float = 0.5, l: float = 1, w: float = 1, h: float = 1):
    pyrosim.Send_Cube(name=f"{name}", pos=[x, y, z], size=[l, w, h])


def create_world():
    pyrosim.Start_SDF("world.sdf")
    simple_cube(name="Box", y=5)
    pyrosim.End()


# Leaving this here for reference
def create_robot():
    pyrosim.Start_URDF("body.urdf")
    simple_cube("Link0")
    # create a joint between the two cubes, otherwise you can't store them both in the same URDF file
    # first link uses absolute coordinates. all subsequent links use relative coordinates.
    pyrosim.Send_Joint(name="Link0_Link1", parent="Link0", child="Link1", type="revolute", position=[0.0,0,1])
    # since this cube is now a member of the link0 body (linked), it's position is _relative_ to lin0
    simple_cube(name="Link1", x=0.0, y=0, z=0.5)
    pyrosim.Send_Joint(name="Link1_Link2", parent="Link1", child="Link2", type="revolute", position=[0.0,0,1])
    simple_cube(name="Link2", x=0.0, y=0, z=0.5)
    pyrosim.Send_Joint(name="Link2_Link3", parent="Link2", child="Link3", type="revolute", position=[0.0,0.5,0.5])
    simple_cube(name="Link3", x=0.0, y=0.5, z=0.0)
    pyrosim.Send_Joint(name="Link3_Link4", parent="Link3", child="Link4", type="revolute", position=[0.0,1,0.0])
    simple_cube(name="Link4", x=0.0, y=0.5, z=0.0)
    pyrosim.Send_Joint(name="Link4_Link5", parent="Link4", child="Link5", type="revolute", position=[0.0,0.5,-0.5])
    simple_cube(name="Link5", x=0.0, y=0.0, z=-0.5)
    pyrosim.Send_Joint(name="Link5_Link6", parent="Link5", child="Link6", type="revolute", position=[0.0,0.0,-1])
    simple_cube(name="Link6", x=0.0, y=0.0, z=-0.5)
    pyrosim.End()


def generate_tribot():

    pyrosim.Start_URDF("body.urdf")
    simple_cube(name="Torso", x=1.5, z=1.5)

    # first link uses absolute coordinate, all subsequent links use relative
    pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute", position=[1, 0, 1])
    simple_cube(name="BackLeg", x=-0.5, y=0, z=-0.5)

    # this is another first link in this case
    pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute", position=[2, 0 ,1])
    simple_cube(name="FrontLeg", x=0.5, y=0, z=-0.5)
    pyrosim.End()


def generate_brain():
    pyrosim.Start_NeuralNetwork("brain.nndf")

    pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
    pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLeg")
    pyrosim.Send_Sensor_Neuron(name=2, linkName="FrontLeg")

    pyrosim.Send_Motor_Neuron(name=3, jointName="Torso_BackLeg")
    pyrosim.Send_Motor_Neuron(name=4, jointName="Torso_FrontLeg")

    for sensor in range(3):
        # we are iterating over sensors by sensor integer name. ugly, as always
        for motor in range(3, 5):
            pyrosim.Send_Synapse(sourceNeuronName=sensor, targetNeuronName=motor, weight=random.uniform(-1,1))

    pyrosim.End()


if __name__ == "__main__":
    create_world()
    generate_tribot()
    generate_brain()
