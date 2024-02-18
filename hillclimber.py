from solution import SOLUTION
import constants as c
import copy


class HILLCLIMBER:
    def __init__(self):
        self.parent = SOLUTION()
        self.child = None

    def evolve(self):
        self.parent.evaluate("DISPLAY")

        for generation in range(c.NUM_GENERATIONS):
            print(f"Simulating generation: {generation}...")
            self.evolve_one_generation()

    def evolve_one_generation(self):
        self.spawn()
        self.mutate()
        self.child.evaluate("DIRECT")
        self.print()
        self.select()

    def spawn(self):
        self.child = copy.deepcopy(self.parent)

    def mutate(self):
        self.child.mutate()

    def select(self):
        if self.child.fitness > self.parent.fitness:
            self.parent = self.child

    def print(self):
        print(f"\nPARENT FITNESS: {self.parent.fitness}")
        print(f"CHILD FITNESS: {self.child.fitness}\n")

    def show_best(self):
        self.parent.evaluate("DISPLAY")