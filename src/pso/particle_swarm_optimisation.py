"""
Particle Swarm Optimisation is a population based metaheuristic
- The state of the system at any given time is defined by the positions and velocities of all particles

How it works:
- starts with a population of particles with rand positions and velocities
- positions are the float random values assigned to each value, velocities is how much they change
- each particle is evaluated at their current position (fitness)
- we store a global best position "global_best_fitness" and for a particle best "particle.best_fitness"
- if a certain pbest is greater than gbest, we update gbest
- the velocity of each particle is calculated based on pbest, gbest, current velocity and rand values

step 1: initialise particles with random x (position) and v (velocity)
step 2: evaluate fitness
step 3: find global best fitness
step 4: for each particle, update velocity
step 5: for each particle, update position
step 6: for each particle, update the best personal fitness and the best global fitness
step 7: for each particle, if the global best fitness is a global optimum (satisfies all clauses) early exit
step 8: return to step 2
"""

import random
from particle import *
from utils import evaluate_particle_fitness

def particle_swarm_optimisation(clauses, num_clauses, num_vars, num_particles, max_evaluations):
    swarm = [initialise_particle(clauses,num_vars) for _ in range(num_particles)] ## arr of particles, size = number of particles (arg), step 1 and 2

    global_best_fitness, global_best_position = find_global_best(swarm) ## initialise best_global fitness and position, step 3

    evaluations = len(swarm) ## when constructing the swarm every particle had their fitness evaluated
    patience = 250_000
    last_improvement = evaluations

    while (evaluations < max_evaluations
           and global_best_fitness < num_clauses
           and (evaluations - last_improvement) < patience):
        for particle in swarm:
            if evaluations >= max_evaluations or (evaluations - last_improvement) >= patience:
                break

            particle.update_velocity(global_best_position) ## step 4
            particle.update_position()                     ## step 5

            particle.fitness = evaluate_particle_fitness(clauses, particle.position)

            if particle.fitness > particle.best_fitness:   ## step 6
                particle.update_best_state()
            if particle.fitness > global_best_fitness:
                global_best_fitness = particle.fitness   ## update global best fitness
                global_best_position = particle.position.copy()
                last_improvement = evaluations  # reset ao relógio da estagnação
                print(last_improvement)

            evaluations += 1

    return global_best_fitness, global_best_position, evaluations


def particle_swarm_optimisation_with_informants(clauses, num_clauses, num_vars, num_particles, num_informants, max_evaluations):
    """ [cont.]
    step 5.1: find informants best fitness
    """
    swarm = [initialise_particle(clauses, num_vars) for _ in range(num_particles)]  ## arr of particles, size = number of particles (arg), step 1 and 2

    global_best_fitness, global_best_position = find_global_best(swarm) ## initialise best_global fitness and position

    evaluations = len(swarm) ## when constructing the swarm every particle had their fitness evaluated
    patience = 1000000
    last_improvement = evaluations

    while (evaluations < max_evaluations
        and global_best_fitness < num_clauses
        and (evaluations - last_improvement) < patience):

        for particle in swarm:
            if evaluations >= max_evaluations or (evaluations - last_improvement) >= patience:
                break

            informants_best_position = find_informants_best_position(swarm, num_informants, particle)
            particle.update_velocity_with_informants(global_best_position, informants_best_position)  ## step 3
            particle.update_position()  ## step 4

            particle.fitness = evaluate_particle_fitness(clauses, particle.position)

            if particle.fitness > particle.best_fitness:  ## step 6
                particle.update_best_state()
            if particle.fitness > global_best_fitness:
                global_best_fitness = particle.fitness  ## update global best fitness
                global_best_position = particle.position.copy()
                last_improvement = evaluations  # reset ao relógio da estagnação
                print(last_improvement)

            evaluations+=1

    return global_best_fitness, global_best_position, evaluations



"""utils: """
def initialise_particle(clauses, num_vars):
    p = Particle(num_vars)
    p.fitness = evaluate_particle_fitness(clauses, p.position)
    p.update_best_state()
    return p

def find_informants_best_position(swarm, num_informants, particle):
    informants = random.sample(swarm, num_informants - 1)
    informants.append(particle)

    best_informant = max(informants, key=lambda p: p.best_fitness)
    return best_informant.best_position.copy()


def find_global_best(swarm):
    global_best_fitness = max(p.fitness for p in swarm)
    best_index = np.argmax([p.fitness for p in swarm])
    global_best_position = swarm[best_index].position.copy()
    return global_best_fitness, global_best_position