from math import ceil, isclose

import numpy as np
import copy


class Gene:
    def __init__(self):
        self.values = None
        self.cost = None


class Output:
    def __init__(self):
        self.name = "Default"
        self.pop = None
        self.best_sol = None
        self.best_cost = None
        self.avg_cost = None
        self.converged_it = 0


def run(config, cost_fun):
    cost_fun = cost_fun

    if config.seed != 0:
        print(f"=== Seed = {config.seed} ===")
        np.random.seed(config.seed)

    # Data from configuration file
    max_iter = config.max_iter
    pop_size = config.pop_size
    mating_num = config.mating_num
    child_percentage = config.child_percentage
    mutation_num = config.mutation_num
    mut_rate = config.mut_rate
    discard_num = config.discard_num
    min_bound = config.min_bound
    max_bound = config.max_bound
    alpha = config.alpha
    sigma = config.sigma

    # Best solution found
    best_sol = copy.deepcopy(Gene())
    best_sol.cost = np.inf  # Infinity, because we're looking for the lowest cost

    # Initialize population
    pop = []
    for _ in range(pop_size):
        pop.append(Gene())

    # Avg and best cost of generations
    avg_cost = np.empty(max_iter)
    best_cost = np.empty(max_iter)

    # How many times to mate
    loop_times = ceil(pop_size*child_percentage/2)

    # Convergence check
    converges = [0, np.inf, 0]

    for i in range(pop_size):
        pop[i].values = np.random.uniform(min_bound, max_bound, 33)
        pop[i].cost = cost_fun(pop[i].values)

        if pop[i].cost < best_sol.cost:
            best_sol = copy.deepcopy(pop[i])

    to_mutate = []
    for i in range(loop_times):
        if i < mutation_num:
            to_mutate.append(1)
        else:
            to_mutate.append(0)

    # Main loop
    for it in range(max_iter):
        # Sort and discard
        pop = sorted(pop, key=lambda x: x.cost)
        pop = pop[0:(pop_size - ceil(pop_size * discard_num))]
        np.random.shuffle(to_mutate)
        popc = []
        kids_count = 0
        for t in range(loop_times):
            # Selection
            p1 = turnir(cost_fun, pop[0:mating_num], 3)
            p2 = turnir(cost_fun, pop[0:mating_num], 3)

            # Crossover
            c1, c2 = crossover(p1, p2, alpha)

            # Mutation
            if kids_count < loop_times:
                if to_mutate[kids_count] == 1:
                    c1 = mutate(c1, mut_rate, sigma)
                kids_count += 1
                if kids_count < loop_times:
                    if to_mutate[kids_count] == 1:
                        c2 = mutate(c2, mut_rate, sigma)
                kids_count += 1

            # Apply Bounds (can't be out of bounds obviously)
            apply_bounds(c1, min_bound, max_bound)
            apply_bounds(c2, min_bound, max_bound)

            # Evaluate children - 1
            c1.cost = cost_fun(c1.values)
            if c1.cost < best_sol.cost:
                best_sol = copy.deepcopy(c1)

            # Evaluate children - 2
            c2.cost = cost_fun(c2.values)
            if c2.cost < best_sol.cost:
                best_sol = copy.deepcopy(c2)

            # Add children to popc
            popc.append(c1)
            popc.append(c2)

        # Merge
        pop += popc

        # Store avg and best cost
        sum0 = 0
        for p in pop:
            sum0 += p.cost
        avg_cost[it] = sum0 / len(pop)
        best_cost[it] = best_sol.cost

        # Dal konvergira?? Radim po best solution ever
        if isclose(converges[1], best_cost[it], rel_tol=0.05):
            converges[0] += 1
        else:
            converges[0] = 0
            converges[1] = best_cost[it]

        if converges[0] > 40:
            converges[2] = it
            break

        # Print info for each gen
        print(f"Generation {it}:\t Best Cost = {round(best_cost[it], 5)}\t|\tAvg Cost = {round(avg_cost[it], 5)}")

    # Print best solution
    print(f"Best solution :\n{np.round(best_sol.values, 3)}")

    # Values to return
    out = Output()
    out.pop = pop
    out.best_sol = best_sol
    out.best_cost = best_cost
    out.avg_cost = avg_cost
    out.converged_it = converges[2]
    return out


# BLX-alpha crossover
# formula... i ovo je da je default ako se ne prosledi alpha 0.5
def crossover(p1, p2, alpha=0.5):
    c1 = copy.deepcopy(p1)
    c2 = copy.deepcopy(p2)

    # So...get values...enumerate splits them? i ce biti od 0 do koliko ima,
    # dok ce x i y biti vrednosti c1 i c2 respektivno...
    for i, (x, y) in enumerate(zip(c1.values, c2.values)):
        d = abs(x - y)
        c1.values[i] = np.random.uniform(min(x, y) - alpha * d, max(x, y) + alpha * d)
        c2.values[i] = np.random.uniform(min(x, y) - alpha * d, max(x, y) + alpha * d)
    return c1, c2


# x is non-mutated solution
# mut_rate - number of genes/values in them that will be mutated
# sigma is step size of our real mutation
def mutate(x, mut_rate, sigma):
    y = copy.deepcopy(x)

    # this basically generates an array of the same size as the gene,
    # with numbers that range from 0 to 1, and in flag we are storing
    # the comparison value with mut_rate, which can be in range [0, 1],
    # and using math magic this means that in mut_rate cases we will get
    # a True value
    flag = np.random.rand(*x.values.shape) <= mut_rate
    # argwhere means where True, and returns indices
    ind = np.argwhere(flag)
    # and...here we mutate it with standard deviation sigma N(mut_rate, sigma^2)
    y.values[ind] += sigma * np.random.randn(*ind.shape)
    return y


# Self-explanatory, if x value is greater than max allowed, lower it to max and vice versa
def apply_bounds(x, min_bound, max_bound):
    x.values = np.maximum(x.values, min_bound)
    x.values = np.minimum(x.values, max_bound)


# turnirska selekcija - argumenti su funkcija troška, rešenje, populacija i veličina turnira
def turnir(fja, pop, vel):
    z = []
    while len(z) < vel:
        z.append(np.random.choice(pop))
    best = None
    best_f = None
    for e in z:
        ff = fja(e.values)
        if best is None or ff < best_f:
            best_f = ff
            best = e
    return best
