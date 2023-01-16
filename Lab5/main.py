import matplotlib.pyplot as plt
import numpy as np
from random import random, sample


class Individual:
    def __init__(self, path, matrix):
        self.path = path
        self.matrix = matrix
        self.fitness = self.calculate_fitness()

    def calculate_fitness(self):
        fitness = 0
        index = 0
        for i in range(len(self.path) - 1):
            fitness += self.matrix[index][self.path[i + 1]]
            index = self.path[i]
        return fitness

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __gt__(self, other):
        return self.fitness > other.fitness

    def __getitem__(self, offset):
        return self.path[offset]

    def __len__(self):
        return len(self.path)

    def __getslice__(self, low, high):
        return Individual(self.path[low:high], self.matrix)


class Graph:
    def __init__(self, size):
        self.matrix = self.generate_matrix(size)
        self.print_matrix(self.matrix)

    @staticmethod
    def generate_matrix(size):
        matrix = []
        for _ in range(size):
            matrix.append([0 for _ in range(size)])

        for i in range(size):
            for j in range(size):
                if i >= j:
                    if i == j:
                        matrix[i][j] = float('inf')
                    else:
                        matrix[i][j] = round(random() * 149 + 5)
                        matrix[j][i] = matrix[i][j]
        return matrix

    @staticmethod
    def print_matrix(graph):
        print('Graph adjacency matrix:')
        print('\n'.join([''.join(['{:6}'.format(item) for item in row])
                         for row in graph]))
        print()

    @staticmethod
    def fill_with_infs(matrix, size):
        for i in range(size):
            matrix.append([])

        for i in matrix:
            for j in range(size):
                i.append(float('inf'))


class GeneticAlgorithm:
    def __init__(self, size):
        self.graph_size = size
        self.graph = Graph(size)

    def launch_genetic_selection(self, iterations, population_size, crossovers_number, mutations_number, mutation_probability):
        population = self.generate_population(population_size)
        best_results = [population[0].fitness]
        for i in range(iterations):
            self.generate_crossover(crossovers_number, population)
            self.mutations(mutations_number, mutation_probability, population)
            population.sort()
            population = population[:population_size]
            best_results.append(population[0].fitness)
            if i % 10 == 0:
                print(f'Current best route length: {population[0].fitness}')
        return population, best_results

    def generate_crossover(self, crossovers_number, population):
        for j in range(crossovers_number):
            childs = self.crossover(population)
            population.append(Individual(self.local_improvement(childs[0]), self.graph.matrix))
            population.append(Individual(self.local_improvement(childs[1]), self.graph.matrix))

    def mutations(self, mutations_number, mutation_probability, population):
        for j in range(mutations_number):
            childs = self.crossover(population)
            mutants = [self.try_mutation(mutation_probability, childs[0]),
                       self.try_mutation(mutation_probability, childs[1])]
            if mutants[0] is not None:
                population.append(Individual(self.local_improvement(mutants[0]), self.graph.matrix))
            elif childs[0] is not None:
                population.append(Individual(self.local_improvement(childs[0]), self.graph.matrix))
            if mutants[1] is not None:
                population.append(Individual(self.local_improvement(mutants[1]), self.graph.matrix))
            elif childs[1] is not None:
                population.append(Individual(self.local_improvement(childs[1]), self.graph.matrix))

    def generate_population(self, population_size):
        population = []
        for i in range(population_size - 1):
            population.append(Individual(self.create_random_path(), self.graph.matrix))
        return population

    def crossover(self, population):
        parents = sample(population, 2)
        breaking_point = round(random() * (len(parents[0]) - 1) + 1)
        first_child = parents[0][:breaking_point]
        self.add_chromosome_part(first_child, parents, breaking_point, 1)
        second_child = parents[1][:breaking_point]
        self.add_chromosome_part(second_child, parents, breaking_point, 0)
        return first_child, second_child

    def try_mutation(self, probability, child):
        if random() < probability:
            return self.start_mutation(child)

    def create_random_path(self):
        random_path = [0]
        while len(random_path) <= self.graph_size:
            if len(random_path) == self.graph_size:
                random_path.append(0)
            else:
                temp = round(random() * (self.graph_size - 1))
                if temp not in random_path:
                    random_path.append(temp)
        return random_path

    def add_chromosome_part(self, child, parents, breaking_point, parent_number):
        i = breaking_point
        while i < len(parents[parent_number]):
            if parents[parent_number][i] not in child:
                child.append(parents[parent_number][i])
            i += 1

        if len(child) < len(parents[parent_number]) - 1:
            self.fill_till_end(child, parents, parent_number)
        child.append(0)

    def check_child(self, child):
        matrix = self.graph.matrix
        index = 0
        for i in range(len(child) - 1):
            if matrix[index][child[i + 1]] == float('inf'):
                return False
        return True

    def start_mutation(self, child):
        indexes = sample([*range(1, len(child))], 2)
        child[indexes[0]], child[indexes[1]] = child[indexes[1]], child[indexes[0]]
        if self.check_child(child):
            return child

    @staticmethod
    def fill_till_end(child, parents, parent_number):
        if parent_number == 0:
            another_parent_number = 1
        else:
            another_parent_number = 0
        i = 0
        while i < len(parents[another_parent_number]):
            if parents[another_parent_number][i] not in child:
                child.append(parents[another_parent_number][i])
            i += 1

    @staticmethod
    def local_improvement(improved):
        i = round(random() * (len(improved) - 2) + 1)
        j = round(random() * (len(improved) - 2) + 1)
        improved[i], improved[j] = improved[j], improved[i]
        return improved


gr = GeneticAlgorithm(300)
results = gr.launch_genetic_selection(1000, 8, 8, 8, 0.2)
ypoints = np.array(results[1])
plt.plot(ypoints)
plt.show()
print(f'The best route length: {results[0][0].fitness}')
print(f'The best route: {results[0][0].path}')




