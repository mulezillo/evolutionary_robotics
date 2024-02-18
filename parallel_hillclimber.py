from solution import SOLUTION
import constants as c
import copy
import os


class PARALLEL_HILLCLIMBER:
    def __init__(self):

        # deleting all files here seems scary... but okay
        os.system("rm brain*.nndf")
        os.system("rm fitness*.txt")
        self.next_id = 0
        self.parents = {}
        self.children = {}
        for i in range(c.POPULATION_SIZE):
            self.parents[i] = SOLUTION(self.next_id)
            self.next_id += 1

    def evolve(self):
        self.evaluate(self.parents.values())

        for generation in range(c.NUM_GENERATIONS):
            print(f"Simulating generation: {generation}...")
            self.evolve_one_generation()
        pass

    def evolve_one_generation(self):
        self.spawn()
        self.mutate()
        self.evaluate(self.children.values())
        self.print()
        self.select()

    def spawn(self):
        for key, parent in self.parents.items():
            child = copy.deepcopy(parent)
            child.set_id(self.next_id)
            self.next_id += 1
            self.children[key] = child

    def mutate(self):
        for child in self.children.values():
            child.mutate()

    @staticmethod
    def evaluate(solutions):

        for sol in solutions:
            sol.start_simulation("DIRECT")

        for sol in solutions:
            sol.wait_for_sim_to_end()

    def select(self):
        for child_id, child in self.children.items():
            # going "left" this time
            if child.fitness < self.parents[child_id].fitness:
                self.parents[child_id] = child

    def print(self):
        print(f"\nFITNESS of PARENTS: {[p.fitness for p in self.parents.values()]}")
        print(f"\nFITNESS of CHILDREN: {[p.fitness for p in self.children.values()]}")

    def show_best(self):
        best_fitness = 1000000  # some arbitrary large number
        best_parent = None
        for parent in self.parents.values():
            if parent.fitness < best_fitness:
                best_parent = parent
        best_parent.start_simulation("DISPLAY")
