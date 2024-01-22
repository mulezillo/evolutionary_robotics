import pyrosim.pyrosim as pyrosim


def stack_cubes(num_cubes: int, x: float, y: float, z: float, l: float, w: float, h: float):
    z += h / 2  # coordinates are the middle of the object... apparently
    for i in range(num_cubes):
        pyrosim.Send_Cube(name=f"Box{i}", pos=[x, y, z], size=[l, w, h])
        l *= 0.9
        w *= 0.9
        h *= 0.9
        # since coordinates are center based, we have to account for half the height of the base box and half the
        # height of the of top box when calculating the next z. hideous, I know.
        z += (h/2 + (h/0.9 * 2))


def build_crazy_world():
    x = 0
    y = 0
    z = 0
    l = 1
    w = 1
    h = 1
    for x in range(5):
        for y in range(5):
            stack_cubes(10, x, y, z, l, w, h)
            y += 1
        x += 1


if __name__ == "__main__":
    pyrosim.Start_SDF("boxes.sdf")
    build_crazy_world()
    pyrosim.End()
