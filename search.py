from parallel_hillclimber import PARALLEL_HILLCLIMBER


if __name__ == "__main__":

    phc = PARALLEL_HILLCLIMBER()
    phc.evolve()
    phc.show_best()
