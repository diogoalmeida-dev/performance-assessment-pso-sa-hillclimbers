import sys

import utils
from src import utils

from multistart_next_ascent_hillclimbing import multistart_next_ascent_hillclimbing
from multistart_variable_neighbourhood_ascent import multistart_variable_next_ascent_hillclimbing
from variable_neighbourhood_ascent import variable_neighbourhood_hillclimbing
from next_ascent_hillclimbing import next_ascent_hillclimbing

CNF_FILES = {
    "1": "../../cnf_files/uf20-01.cnf",
    "2": "../../cnf_files/uf100-01.cnf",
    "3": "../../cnf_files/uf250-01.cnf"
}

max_evaluations = 500000
max_k = 3

def run_algorithm(choice, num_runs, clauses, num_clauses, num_vars):
    best_fitness = None

    for run in range(1, num_runs + 1):
        if choice == "1":
            solution, fitness, evaluations = next_ascent_hillclimbing(clauses, num_clauses, num_vars,max_evaluations)
        elif choice == "2":
            solution_data, evaluations = multistart_next_ascent_hillclimbing(clauses, num_clauses, num_vars,max_evaluations)
            solution, fitness, _ = solution_data
        elif choice == "3":
            solution, fitness, evaluations  = variable_neighbourhood_hillclimbing(clauses, num_clauses, num_vars, max_evaluations)
        elif choice == "4":
            solution, fitness, evaluations = multistart_variable_next_ascent_hillclimbing(clauses, num_clauses, num_vars, max_evaluations, max_k)
        else:
            print("Invalid choice.")
            sys.exit(1)

        if (best_fitness is None or
            fitness > best_fitness or
            (fitness == best_fitness)):
            best_fitness = fitness

    print(f"Best Fitness: {best_fitness}")

def main():
    while True:
        print("Select CNF file:")
        print("1 - uf20-01.cnf")
        print("2 - uf100-01.cnf")
        print("3 - uf250-01.cnf")
        cnf_choice = input("Enter choice (1-3): ").strip()
        if cnf_choice not in CNF_FILES:
            print("Invalid CNF file choice.")
            continue

        cnf_path = CNF_FILES[cnf_choice]
        clauses, num_clauses, num_vars = utils.read_cnf(cnf_path)
        print(f"\nLoaded: {cnf_path} — vars={num_vars}, clauses={num_clauses}")

        print("\nSelect Algorithm:")
        print("1 - Next Ascent Hillclimbing")
        print("2 - Multistart Next Ascent Hillclimbing")
        print("3 - Variable Neighbourhood Hillclimbing")
        print("4 - Multistart Variable Neighbourhood Hillclimbing")
        algo_choice = input("Enter choice (1-4): ").strip()
        if algo_choice not in ["1", "2", "3", "4"]:
            print("Invalid algorithm choice.")
            continue

        while True:
            try:
                num_runs = int(input("Enter number of runs: ").strip())
                if num_runs <= 0:
                    raise ValueError
                break
            except ValueError:
                print("Please enter a valid positive integer.")

        run_algorithm(algo_choice, num_runs, clauses, num_clauses, num_vars)

        again = input("\nDo you want to run another algorithm? (y/n): ").strip().lower()
        if again != 'y':
            print("Exiting...")
            break

if __name__ == "__main__":
    main()
