# Function to find the fitness being the fitness the number of clauses satisfied by the combination
def evaluate_particle_fitness(clauses, combination):
    fitness = 0

    for clause in clauses:

        clause_fitness = 0
        for value in clause:
            var_index = abs(value) - 1 ## normalise for clause list
            ## replace with: "combination[var_index]" if you want to use the continuous vector, this line just turns 0.3 in 0 and 0.7 in 1
            is_true = 1 if combination[var_index] > 0.5 else 0
            if value < 0: ## if literal value is below 0, the variable is negated
                is_true = not is_true
            if is_true: ## if bool is true
                clause_fitness = 1
                break
        fitness += clause_fitness
    return fitness

def choose_swarm_size(num_vars: int) -> int:
    if num_vars <= 30:
        return 30
    elif num_vars <= 150:
        return 75
    else:
        return 350
