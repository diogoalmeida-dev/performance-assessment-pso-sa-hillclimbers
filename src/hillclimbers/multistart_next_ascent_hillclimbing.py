"""
Multistart Next Ascent Hillclimbing Algorithm (1-bit Hamming Distance)

This algorithm attempts to solve a CNF SAT problem using a stochastic local search.
It combines two strategies:
1. Next-Ascent Hillclimbing: explores the 1-bit Hamming distance neighbourhood of a solution,
   moving to the first neighbor that improves fitness (number of satisfied clauses).
2. Multistart: repeats the hillclimbing process from multiple random initial solutions
   until either a global optimum is found or a maximum number of evaluations is reached.

Key Points:
- Each solution is represented as a list of 0/1 assignments for the CNF variables.
- Fitness is the number of clauses satisfied by the solution.
- Evaluations count the number of fitness computations performed.
- Stops early if the global optimum (all clauses satisfied) is found.
"""

import random

from utils import random_combination, evaluate_fitness, generate_neighbours

def multistart_next_ascent_hillclimbing(clauses, num_clauses, num_vars, max_evaluations):
    best_solution = None   # store the best found
    best_fitness = -1      # initialize to something smaller than possible
    evaluations = 0

    while evaluations < max_evaluations:
        current_solution = random_combination(num_vars)
        fitness = evaluate_fitness(clauses, current_solution)
        evaluations += 1

        while True:
            if evaluations >= max_evaluations:
                break

            if fitness == num_clauses:  # global optimum found
                best_solution = (current_solution, fitness, evaluations)
                return best_solution, evaluations

            indexes = list(range(num_vars))  # indices of each bit
            random.shuffle(indexes)  # shuffle indices once
            better_found = False

            for i in indexes:
                if evaluations >= max_evaluations:
                    break

                current_solution[i] = 1 - current_solution[i]  # flip bit directly
                nb_fitness = evaluate_fitness(clauses, current_solution)
                evaluations += 1

                if nb_fitness > fitness:
                    fitness = nb_fitness
                    better_found = True
                    break
                else:
                    current_solution[i] = 1 - current_solution[i]  # undo flip

            if not better_found:
                break  # local optimum

        if fitness > best_fitness:   # update global best if current local optimum is better
            best_solution = (current_solution, fitness, evaluations)
            best_fitness = fitness

    return best_solution, evaluations