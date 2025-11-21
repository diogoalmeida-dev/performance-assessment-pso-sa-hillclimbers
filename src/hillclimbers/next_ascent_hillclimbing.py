"""
Next-Ascent Hillclimbing Algorithm (1-bit Hamming Distance)

This algorithm attempts to solve a CNF SAT problem using stochastic local search.
It implements the **Next-Ascent Hillclimbing** strategy:

1. Starts from a random initial solution (0/1 assignments for each CNF variable).
2. Explores the neighborhood at Hamming distance 1 (flipping one bit at a time).
3. Moves immediately to the first neighbor that improves the fitness
   (number of satisfied clauses).
4. Repeats until no improving neighbor is found (local optimum)
   or the global optimum (all clauses satisfied) is reached.

Key Points:
- Fitness is the number of clauses satisfied by the current assignment.
- Evaluations count the number of fitness computations performed.
- Neighbors are visited in random order to introduce stochasticity.
"""

from multistart_next_ascent_hillclimbing import *
from multistart_variable_neighbourhood_ascent import *

def next_ascent_hillclimbing(clauses, num_clauses, num_vars, max_evaluations):
    initial_solution = random_combination(num_vars) ## start with a random solution
    fitness = evaluate_fitness(clauses, initial_solution) ## discover initial solution fitness

    tmp_solution = initial_solution

    evaluations = 1

    while evaluations <= max_evaluations:
        if fitness == num_clauses: ## if the solution is a global optimum, break and return the solution
            break

        neighbours = generate_neighbours(tmp_solution) # generate the neighbourhood by flipping one bit in each solution
        random.shuffle(neighbours) # since its next ascent, randomize search space
        better_found = False # trigger to find local optimum

        for neighbour in neighbours: # for each neighbour
            nb_fitness = evaluate_fitness(clauses, neighbour) # discover its fitness (how many clauses are satisfied)
            evaluations += 1 # for each neighbour accessed, evaluation goes up

            if nb_fitness > fitness: ## if neighbour fitness is better than the current solution, switch to the neighbour
                fitness = nb_fitness
                tmp_solution = neighbour
                better_found = True
                break

        if not better_found:
            break

    return tmp_solution, fitness, evaluations