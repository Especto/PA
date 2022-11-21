import random
import numpy as np
import matplotlib.pyplot as plt


class Item:
    num_items = 0

    def __init__(self, cost, weight):
        self.cost = cost
        self.weight = weight


def init(popsize, n):
    population = []
    for i in range(popsize):
        pop = '0' * i
        pop += '1'
        pop += '0' * (n - i)
        population.append(pop)
    return population


def decode(chromosome, lenght, ITEMS, cap):
    s = []
    g = 0
    f = 0
    for i in range(lenght):
        if chromosome[i] == '1':
            if g+ITEMS[i].weight <= cap:
                g += ITEMS[i].weight
                f += ITEMS[i].cost
                s.append(i)
            else:
                break
    return f, s


def fitness(population, lenght, ITEMS, cap):
    value = []
    ss = []
    for i in range(len(population)):
        f, s = decode(population[i], lenght, ITEMS, cap)
        value.append(f)
        ss.append(s)
    return value, ss


def roulettewheel(population, value, p_size):
    fitness_sum = []
    value_sum = sum(value)
    fitness = [i/value_sum for i in value]
    for i in range(len(population)):
        if i == 0:
            fitness_sum.append(fitness[i])
        else:
            fitness_sum.append(fitness_sum[i-1]+fitness[i])
    population_new = []
    for j in range(p_size):
        r = np.random.uniform(0, 1)
        for i in range(len(fitness_sum)):
            if i == 0:
                if 0 <= r <= fitness_sum[i]:
                    population_new.append(population[i])
            else:
                if fitness_sum[i-1] <= r <= fitness_sum[i]:
                    population_new.append(population[i])
    return population_new


def crossover(population, pc):
    a = int(len(population)/2)
    parents_one = population[:a]
    parents_two = population[a:]
    np.random.shuffle(parents_one)
    np.random.shuffle(parents_two)
    offspring = []
    for i in range(a):
        r = np.random.uniform(0, 1)
        if r <= pc:
            point1 = int(len(parents_one[i])/3)
            point2 = 2 * point1
            off_one = parents_one[i][:point1]+parents_two[i][point1:point2]+parents_one[i][point2:]
            off_two = parents_two[i][:point1]+parents_one[i][point1:point2]+parents_two[i][point2:]
        else:
            off_one = parents_one[i]
            off_two = parents_two[i]
        offspring.append(off_one)
        offspring.append(off_two)
    return offspring


def mutation(offspring, pm):
    for i in range(len(offspring)):
        r = np.random.uniform(0, 1)
        if r <= pm:
            point = np.random.randint(0, len(offspring[i]))
            if not point:
                if offspring[i][point] == '1':
                    offspring[i] = '0'+offspring[i][1:]
                else:
                    offspring[i] = '1'+offspring[i][1:]
            else:
                if offspring[i][point] == '1':
                    offspring[i] = offspring[i][:(point-1)]+'0'+offspring[i][point:]
                else:
                    offspring[i] = offspring[i][:(point-1)]+'1'+offspring[i][point:]
    return offspring


def local_improve(offspring, ITEMS, CAPACITY, ITEM_BENEFITS):
    for gen in range(len(offspring)):
        weight = 0
        for chromosome in range(len(offspring[gen])):
            if offspring[gen][chromosome] == '1':
                weight += ITEMS[chromosome].weight

        if weight <= CAPACITY:
            for item in range(len(ITEM_BENEFITS)):
                if offspring[gen][ITEM_BENEFITS[item][1]] == '0':
                    if weight + ITEMS[ITEM_BENEFITS[item][1]].weight <= CAPACITY:
                        weight += ITEMS[ITEM_BENEFITS[item][1]].weight
                        if not ITEM_BENEFITS[item][1]:
                            offspring[gen] = '1' + offspring[gen][1:]
                        else:
                            offspring[gen] = offspring[gen][:(ITEM_BENEFITS[item][1] - 1)] + '1' + offspring[gen][ITEM_BENEFITS[item][1]:]
                    break
    return offspring


def fitness_items(ITEMS):
    items = []
    for i in range(len(ITEMS)):
        items.append((ITEMS[i].cost/ITEMS[i].weight, i))
    items.sort(reverse=True)
    return items


def main():
    GENERATIONS = 1000
    P_CROSSOVER = 1
    P_MUTATION = 0.1
    P_SIZE = 100
    LENGTH_CHROMOSOME = 100
    ITEMS = []
    for item in range(LENGTH_CHROMOSOME):
        ITEMS.append(Item(random.randint(2, 20), random.randint(1, 10)))
    ITEM_BENEFIT = fitness_items(ITEMS)
    CAPACITY = 200
    IMPROVE = True

    population = init(P_SIZE, LENGTH_CHROMOSOME)

    t = []
    best_ind = []

    for i in range(GENERATIONS):
        if i % 20 == 0 and i > 0:
            print(max(value1))
        offspring = crossover(population, P_CROSSOVER)
        offspring = mutation(offspring, P_MUTATION)
        if IMPROVE:
            offspring = local_improve(offspring, ITEMS, CAPACITY, ITEM_BENEFIT)
        mixpopulation = population+offspring

        value, s = fitness(mixpopulation, LENGTH_CHROMOSOME, ITEMS, CAPACITY)
        population = roulettewheel(mixpopulation, value, P_SIZE)

        value1, s1 = fitness(population, LENGTH_CHROMOSOME, ITEMS, CAPACITY)

        h = value1.index(max(value1))
        t.append(max(value1))
        best_ind.append(population[h])

    hh = t.index(max(t))
    f2, s2 = decode(best_ind[hh], LENGTH_CHROMOSOME, ITEMS, CAPACITY)
    cost, weight = 0, 0
    for i in s2:
        cost += ITEMS[i].cost
        weight += ITEMS[i].weight
    print(f"The best combination:\n{s2}\nCost: {cost}, Weight: {weight}")
    print(f"First appearance in {hh} generation")

    plt.plot(t, color='red')
    plt.xlabel('Generations')
    plt.ylabel('Fitness')
    plt.title('Dependence of quality on generation')
    plt.show()


main()
