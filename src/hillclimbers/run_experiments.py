import os
import random
import numpy as np
import pandas as pd

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

INDEPENDENT_RUNS = 30
RESULTS_FILE = "../results/hillclimbing_results.xlsx"

MAX_EVALUATIONS = 1_000_000
MAX_K_VNH = 3  # k máximo para as versões de variable neighbourhood


def main():
    os.makedirs(os.path.dirname(RESULTS_FILE), exist_ok=True)

    results = []

    for instance_id, cnf_path in CNF_FILES.items():
        print(f"\nLoaded {cnf_path}")
        clauses, num_clauses, num_vars = utils.read_cnf(cnf_path)
        num_clauses = len(clauses)

        ## Next-Ascent Hillclimbing (NAHC)
        for run in range(INDEPENDENT_RUNS):
            seed = run
            random.seed(seed)
            np.random.seed(seed)

            print(f"[NAHC] File {instance_id}, run {run}, seed {seed}")

            solution, best_fitness, evaluations_used = next_ascent_hillclimbing(
                clauses=clauses,
                num_clauses=num_clauses,
                num_vars=num_vars,
                max_evaluations=MAX_EVALUATIONS,
            )

            results.append(
                {
                    "algorithm": "NAHC",
                    "instance_id": instance_id,
                    "cnf_file": cnf_path,
                    "run": run,
                    "seed": seed,
                    "num_vars": num_vars,
                    "num_clauses": num_clauses,
                    "max_evaluations": MAX_EVALUATIONS,
                    "evaluations_used": evaluations_used,
                    "best_fitness_satisfied": best_fitness,
                }
            )

        ## Multistart NAHC (MS-NAHC)
        for run in range(INDEPENDENT_RUNS):
            seed = run
            random.seed(seed)
            np.random.seed(seed)

            print(f"[MS-NAHC] File {instance_id}, run {run}, seed {seed}")

            # multistart_next_ascent_hillclimbing devolve:
            # best_solution = (current_solution, fitness, eval_at_best), evaluations
            best_solution, evaluations_used = multistart_next_ascent_hillclimbing(
                clauses=clauses,
                num_clauses=num_clauses,
                num_vars=num_vars,
                max_evaluations=MAX_EVALUATIONS,
            )

            if best_solution is None:
                # fallback defensivo, mas na prática não deve acontecer
                best_fitness = -1
            else:
                _, best_fitness, _ = best_solution

            results.append(
                {
                    "algorithm": "MS_NAHC",
                    "instance_id": instance_id,
                    "cnf_file": cnf_path,
                    "run": run,
                    "seed": seed,
                    "num_vars": num_vars,
                    "num_clauses": num_clauses,
                    "max_evaluations": MAX_EVALUATIONS,
                    "evaluations_used": evaluations_used,
                    "best_fitness_satisfied": best_fitness,
                }
            )

        ## Variable Neighbourhood Hillclimbing (VNH, k=1..3)
        for run in range(INDEPENDENT_RUNS):
            seed = run
            random.seed(seed)
            np.random.seed(seed)

            print(f"[VNH] File {instance_id}, run {run}, seed {seed}")

            solution, best_fitness, evaluations_used = variable_neighbourhood_hillclimbing(
                clauses=clauses,
                num_clauses=num_clauses,
                num_vars=num_vars,
                max_evaluations=MAX_EVALUATIONS,
            )

            results.append(
                {
                    "algorithm": "VNH",
                    "instance_id": instance_id,
                    "cnf_file": cnf_path,
                    "run": run,
                    "seed": seed,
                    "num_vars": num_vars,
                    "num_clauses": num_clauses,
                    "max_evaluations": MAX_EVALUATIONS,
                    "evaluations_used": evaluations_used,
                    "best_fitness_satisfied": best_fitness,
                    "max_k": MAX_K_VNH,
                }
            )

        ## Multistart Variable Neighbourhood Hillclimbing (MS-VNH)
        for run in range(INDEPENDENT_RUNS):
            seed = run
            random.seed(seed)
            np.random.seed(seed)

            print(f"[MS-VNH] File {instance_id}, run {run}, seed {seed}")

            best_solution, best_fitness, evaluations_used = (
                multistart_variable_next_ascent_hillclimbing(
                    clauses=clauses,
                    num_clauses=num_clauses,
                    num_vars=num_vars,
                    max_evaluations=MAX_EVALUATIONS,
                    max_k=MAX_K_VNH,
                )
            )

            results.append(
                {
                    "algorithm": "MS_VNH",
                    "instance_id": instance_id,
                    "cnf_file": cnf_path,
                    "run": run,
                    "seed": seed,
                    "num_vars": num_vars,
                    "num_clauses": num_clauses,
                    "max_evaluations": MAX_EVALUATIONS,
                    "evaluations_used": evaluations_used,
                    "best_fitness_satisfied": best_fitness,
                    "max_k": MAX_K_VNH,
                }
            )

    df = pd.DataFrame(results)
    df.to_excel(RESULTS_FILE, index=False)
    print(f"\nSaved results to {RESULTS_FILE}")


if __name__ == "__main__":
    main()
