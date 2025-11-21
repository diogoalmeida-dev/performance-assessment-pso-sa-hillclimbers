import os
import random

import numpy as np
import pandas as pd
import utils
from src import utils

from particle_swarm_optimisation import particle_swarm_optimisation_with_informants

from utils import choose_swarm_size

CNF_FILES = {
    "1": "../../cnf_files/uf20-01.cnf",
    "2": "../../cnf_files/uf100-01.cnf",
    "3": "../../cnf_files/uf250-01.cnf"
}

INDEPENDENT_RUNS = 30  ## number of independent runs
RESULTS_FILE = "../results/pso_results.xlsx"

## PSO parameters
MAX_EVALUATIONS = 1_000_000

## PSO with informants parameters
NUM_INFORMANTS = 6


def main():
    os.makedirs(os.path.dirname(RESULTS_FILE), exist_ok=True)

    results = []

    for instance_id, cnf_path in CNF_FILES.items():
        print(f"\nLoaded {cnf_path}")
        clauses, num_clauses, num_vars = utils.read_cnf(cnf_path)
        num_clauses = len(clauses)

        NUM_PARTICLES = choose_swarm_size(num_vars)

        ## Then all PSO_informants runs
        for run in range(INDEPENDENT_RUNS):
            seed = run  ## same seeds 0..29 for fairness
            random.seed(seed)
            np.random.seed(seed)

            print(f"\n[PSO_informants] File {instance_id}, run {run}, seed {seed}")

            best_fitness_inf, best_position_inf, evals_inf = (
                particle_swarm_optimisation_with_informants(
                    clauses=clauses,
                    num_clauses=num_clauses,
                    num_vars=num_vars,
                    num_particles=NUM_PARTICLES,
                    num_informants=NUM_INFORMANTS,
                    max_evaluations=MAX_EVALUATIONS,
                )
            )

            results.append(
                {
                    "algorithm": "PSO_informants",
                    "instance_id": instance_id,
                    "cnf_file": cnf_path,
                    "run": run,
                    "seed": seed,
                    "num_vars": num_vars,
                    "num_clauses": num_clauses,
                    "num_particles": NUM_PARTICLES,
                    "num_informants": NUM_INFORMANTS,
                    "max_evaluations": MAX_EVALUATIONS,
                    "evaluations_used": evals_inf,
                    "best_fitness_satisfied": best_fitness_inf,
                }
            )

    df = pd.DataFrame(results)
    df.to_excel(RESULTS_FILE, index=False)
    print(f"\nSaved results to {RESULTS_FILE}")

if __name__ == "__main__":
    main()
