from simulation import SIMULATION
import sys


if __name__ == "__main__":
    display_flag = sys.argv[1]
    solution_id = sys.argv[2]
    simulation = SIMULATION(display_flag, solution_id)
    simulation.run()
    simulation.get_fitness()
