import numpy as np

# parameters
max_velocity = 0.4
w = 0.72984 # inertia weight
c1 = 1.496172 # cognitive coefficient
c2 = 0.75 # global coefficient
c3 = 1.496172 # social coefficient

class Particle:
    def __init__(self, num_vars):
        self.num_vars = num_vars ## number of max sat variables
        self.position = np.random.rand(num_vars) ## numpy array of values between 0 and 1
        self.velocity = np.random.uniform(-max_velocity, max_velocity, num_vars)
        self.fitness = 0
        self.best_fitness = -999 ## any value below your bounds
        self.best_position = None

    def update_velocity(self, global_best_position):
        """ Update velocity method:
        new_velocity = w*v + c1(x@ - xti) + c2(x! - xti)
        The velocity formula in english:
        new velocity of the particle x =
        random value "w" multiplied by current velocity "v" -> inertia term
        plus random val "c1" multiplied by best particle position minus current particle position -> personal term
        plus random value "c2" multiplied by global best position minus current particle position -> global term
        """
        inertia_term = w * self.velocity
        personal_term = c1 * (self.best_position - self.position)
        global_term = c2 * (global_best_position -  self.position)

        self.velocity = inertia_term + personal_term + global_term
        self.velocity = np.clip(self.velocity, -max_velocity, max_velocity) ## holds velocity in between bounds to avoid over/under shooting

    def update_velocity_with_informants(self, global_best_position, informant_best_position):
        """ Update velocity with informants method:
        new_velocity = w*v + c1(x@ - xti) + c2(x! - xti) + c3(x* - xti)
        The velocity formula in english:
        new velocity of the particle x =
        random value "w" multiplied by current velocity "v" -> inertia term
        plus random val "c1" multiplied by best particle position minus current particle position -> personal term
        plus random value "c2" multiplied by global best position minus current particle position -> global term
        plus random value "c3" multiplied by informant best position minius current particle position -> social term
        """
        inertia_term = w * self.velocity
        personal_term = c1 * (self.best_position - self.position)
        global_term = c2 * (global_best_position - self.position)
        social_term = c3 * (informant_best_position - self.position)

        self.velocity = inertia_term + personal_term + social_term + global_term
        self.velocity = np.clip(self.velocity, -max_velocity, max_velocity)  ## holds velocity in between bounds to avoid over/under shooting

    def update_position(self):
        """Update position method:
        new_position = xi + vi
        The position formula in english:
        new position of the particle x =
        old position of x + velocity of x
        """
        self.position = self.position + self.velocity
        self.position = np.clip(self.position, 0.0, 1.0) ## holds particle position in between bounds

    def update_best_state(self):
        self.best_fitness = self.fitness
        self.best_position = self.position.copy()