import pandas as pd
from scipy.stats import kruskal, mannwhitneyu

file = "Results/results.xlsx"

## 1) Ler todos os sheets
all_sheets = pd.read_excel(file, sheet_name=None)

## 2) Ficar só com os algoritmos (ignorar TESTS)
algo_sheets = {name: df for name, df in all_sheets.items() if name != "TESTS"}

fitness_data = {}  # algoritmo -> lista de fitness (90 valores)
eval_data = {}     # algoritmo -> lista de evaluations (90 valores)

for name, df in algo_sheets.items():
    fitness_data[name] = df["best_fitness_satisfied"].tolist()
    eval_data[name] = df["evaluations_used"].tolist()

## 3) Dividir em blocos de 30 por instância

instances = ["uf20", "uf100", "uf250"]
runs_per_instance = 30

## dicionários: instância -> (algoritmo -> lista de valores)
fitness_by_instance = {inst: {} for inst in instances}
eval_by_instance = {inst: {} for inst in instances}

for algo_name, fitness_list in fitness_data.items():
    eval_list = eval_data[algo_name]

    for i, inst in enumerate(instances):
        start = i * runs_per_instance
        end = (i + 1) * runs_per_instance

        fitness_by_instance[inst][algo_name] = fitness_list[start:end]
        eval_by_instance[inst][algo_name] = eval_list[start:end]

## 4) Kruskal–Wallis por instância (fitness e evals)
for inst in instances:
    print(f"Instância: {inst}")

    ## FITNESS
    fitness_lists = list(fitness_by_instance[inst].values())
    stat_f, p_f = kruskal(*fitness_lists)
    print("Kruskal – FITNESS")
    print("stat:", stat_f, " p:", p_f)

    ## EVALUATIONS
    eval_lists = list(eval_by_instance[inst].values())
    stat_e, p_e = kruskal(*eval_lists)
    print("Kruskal – EVALUATIONS")
    print("stat:", stat_e, " p:", p_e)

    print("\n")

targets = ["PSO", "SA"]

for inst in instances:
    print(f"Instância: {inst}")

    algos = list(fitness_by_instance[inst].keys())

    for target in targets:
        print(f"\n--- {target} vs outros ---")

        for other in algos:
            if other == target:
                continue

            ## FITNESS
            x = fitness_by_instance[inst][target]
            y = fitness_by_instance[inst][other]

            stat_f, p_f = mannwhitneyu(x, y, alternative="two-sided")

            ## EVALUATIONS
            ex = eval_by_instance[inst][target]
            ey = eval_by_instance[inst][other]

            stat_e, p_e = mannwhitneyu(ex, ey, alternative="two-sided")

            print(f"\n{target} vs {other}")
            print(f"Fitness: U={stat_f:.1f}, p={p_f:.3e}")
            print(f"Eval:    U={stat_e:.1f}, p={p_e:.3e}")
