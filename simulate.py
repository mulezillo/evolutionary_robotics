from simulation import SIMULATION
import sys


if __name__ == "__main__":
    display_flag = sys.argv[1]
    simulation = SIMULATION(display_flag)
    simulation.run()
    simulation.get_fitness()
