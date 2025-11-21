"""
Multistart Variable Neighbourhood Hillclimbing (VNH) Algorithm

This algorithm attempts to solve a CNF SAT problem using a **multistart variable neighbourhood hillclimbing** approach:

1. **Multistart:** Repeatedly starts from random initial solutions until either the global optimum
   is found or a maximum number of evaluations is reached.
2. **Variable Neighbourhood:** Explores the neighborhood of the current solution by flipping `k` bits simultaneously.
   - `k` starts at 1 and increases up to a maximum (`max_k = 3`) if no improvement is found.
   - If an improving neighbor is found, moves to it immediately and resets `k` to 1.
3. **Next-Ascent Hillclimbing:** Visits neighbors in combinatorial order and moves to the first neighbor
   that improves fitness (number of satisfied clauses).

Key Points:
- Fitness = number of satisfied clauses in the CNF formula.
- Evaluations count the total number of fitness computations performed.
- Stops early if the global optimum is found.
- Combines multistart, variable neighborhood, and greedy hillclimbing to escape local optima.
"""

import itertools

from utils import random_combination, evaluate_fitness, generate_neighbours

def multistart_variable_next_ascent_hillclimbing(clauses, num_clauses, num_vars, max_evaluations, max_k):
    evaluations = 0

    best_fitness = -1
    best_solution = None

    while evaluations < max_evaluations:
        current_solution = random_combination(num_vars) ## start with a random solution
        fitness = evaluate_fitness(clauses, current_solution) ## discover current solution fitness
        evaluations += 1

        k = 1

        while k <= max_k and evaluations < max_evaluations:
            better_found = False
            indexes = list(range(num_vars))

            for bits_to_flip in itertools.combinations(indexes, k): # generate neighbours at Hamming distance k ##
                if evaluations >= max_evaluations: # early stop
                    break

                neighbour = current_solution.copy() ## to avoid modifying current solution
                for index in bits_to_flip: ## index is the value in the bits_to_flip
                    neighbour[index] = 1 - neighbour[index] ## flip the bit

                nb_fitness = evaluate_fitness(clauses, neighbour)
                evaluations += 1

                if nb_fitness > fitness:
                    fitness = nb_fitness
                    current_solution = neighbour
                    better_found = True
                    k = 1
                    break

            if not better_found:
                k += 1

        if fitness > best_fitness:
            best_fitness = fitness
            best_solution = current_solution

        if fitness == num_clauses:
            best_solution = current_solution
            best_fitness = fitness
            return best_solution, best_fitness, evaluations

    return best_solution, best_fitness, evaluations