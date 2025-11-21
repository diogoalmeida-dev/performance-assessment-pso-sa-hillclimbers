# Function to find the energy being the number of clauses left to satisfy global optima
def evaluate_energy(clauses, combination):
    fitness = 0
    num_clauses = len(clauses)

    for clause in clauses:

        clause_fitness = 0
        for value in clause:
            var_index = abs(value) - 1 ## normalise for clause list
            is_true = combination[var_index]
            if value < 0: ## if literal value is below 0, the variable is negated
                is_true = not is_true
            if is_true: ## if bool is true
                clause_fitness = 1
                break
        fitness += clause_fitness
    return num_clauses -  fitness