"""
Variable Neighbourhood Hillclimbing (VNH) Algorithm

This algorithm attempts to solve a CNF SAT problem using a local search strategy
with **variable neighbourhoods**:

1. Starts from a random initial solution (0/1 assignments for each CNF variable).
2. Explores the neighborhood of the current solution by flipping `k` bits simultaneously,
   where k starts at 1 and can increase up to a maximum (here k=3).
3. If an improving neighbor is found, moves immediately to it and resets k to 1.
4. If no improvement is found, increases k to explore a wider neighborhood.
5. Stops when a global optimum is found (all clauses satisfied) or all neighborhoods
   have been explored without improvement (local optimum).

Key Points:
- Fitness is the number of satisfied clauses in the CNF formula.
- Evaluations count the number of fitness computations performed.
- Uses combinatorial generation of neighbors at Hamming distance k.
- Combines a greedy hillclimbing approach with a variable neighborhood strategy
  to escape small local optima.
"""

import itertools

from utils import random_combination, evaluate_fitness

# implements variable next ascent hillclimbing using 1 bit hamming distance neighbourhood
# next ascent visits neighbourhood randomly and moves to the first neighbour that improves fitness
# enlargers neighbourhood up to k = 3 bits
def variable_neighbourhood_hillclimbing(clauses, num_clauses, num_vars, max_evaluations):

    initial_solution = random_combination(num_vars) ## start with a random solution
    fitness = evaluate_fitness(clauses, initial_solution) ## discover current solution fitness

    current_solution = initial_solution

    evaluations = 1

    k = 1

    while k <= 3 and evaluations < max_evaluations and fitness < num_clauses:
        if fitness == num_clauses: ## if the solution is a global optimum, break and return the solution
            break

        better_found = False
        indexes = list(range(num_vars)) ## gives the list of indexes

        for bits_to_flip in itertools.combinations(indexes, k): # generate neighbours at hamming distance k
            neighbour = current_solution.copy() ## to avoid modifying current solution
            for index in bits_to_flip: ## index is the value in the bits_to_flip
                neighbour[index] = 1 - neighbour[index] ## flip the bit

            nb_fitness = evaluate_fitness(clauses, neighbour)
            evaluations += 1

            if nb_fitness > fitness:
                fitness = nb_fitness
                better_found = True
                current_solution = neighbour
                k = 1
                break

        if not better_found:
            k += 1

    return current_solution, fitness, evaluations