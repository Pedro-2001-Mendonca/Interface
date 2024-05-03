import random
import math
import numpy as np
import warnings

warnings.filterwarnings("error")


# Define Class Particles
class Particle:
    def __init__(self, position):
        self.position = position
        self.velocity = np.zeros_like(position)
        self.best_position = position
        self.best_fitness = float('inf')


def PSO(T, P, qe, Tref, ObjF, Pop_Size, max_iter):
    particles = []

    # Posotion Initialization
    for i in range(Pop_Size):
        position = np.array(
            [10 * abs(random.random()), abs(random.random()), 100 * abs(random.random()), 0.1 + abs(random.random())])
        particle = Particle(position)

        # Fitness Update
        fitness = ObjF(position, T, P, qe, Tref)

        if i == 0:
            swarm_best_position = position
            swarm_best_fitness = fitness

        particle.best_position = position
        particle.best_fitness = fitness

        if fitness < swarm_best_fitness:
            swarm_best_fitness = fitness
            swarm_best_position = position

        particles.append(particle)

    # PSO Main Loop
    for itr in range(max_iter):

        for particle in particles:

            # Update Velocity
            w = 0.8
            c1 = 1.2
            c2 = 1.2

            r1 = random.random()
            r2 = random.random()

            # Velocity Calculation
            particle.velocity = w * particle.velocity + c1 * r1 * (
                    particle.best_position - particle.position) + c2 * r2 * (
                                        swarm_best_position - particle.position)

            # New Position
            particle.position = particle.position + particle.velocity

            # Evaluate Fitness
            fitness = ObjF(particle.position, T, P, qe, Tref)

            # Update PBest
            if fitness < particle.best_fitness:
                particle.best_fitness = fitness
                particle.best_position = particle.position

            # Update GBest
            if fitness < swarm_best_fitness:
                swarm_best_fitness = fitness
                swarm_best_position = particle.position

    return swarm_best_position, swarm_best_fitness


# Iterate over each objective function and run PSO
def chama_pso(T, P, qe, Tref, model, pop_size, max_iter):
    if model == 0:
        return PSO(T, P, qe, Tref, langmuir, pop_size, max_iter)
    if model == 1:
        return PSO(T, P, qe, Tref, sips, pop_size, max_iter)
    if model == 2:
        return PSO(T, P, qe, Tref, toth, pop_size, max_iter)


def langmuir(x, T, P, qe, Tref):
    result = 0
    for i in range(len(P)):
        try:
            conta = (x[0] * x[1] * math.exp(x[2] * ((1 / T[i]) - (1 / Tref))) * P[i]) / (
                    1 + x[1] * math.exp(x[2] * (1 / T[i] - 1 / Tref)) * P[i])
            result = result + (qe[i] - conta) ** 2

        except:
            result += 100000000

    return result


def sips(x, T, P, qe, Tref):
    result = 0
    for i in range(len(P)):
        try:
            conta = (x[0] * (math.exp(x[2] * ((1 / T[i]) - (1 / Tref))) * x[1] * P[i]) ** (1 / x[3])) / (
                    1 + (math.exp(x[2] * (1 / T[i] - 1 / Tref)) * x[1] * P[i]) ** (1 / x[3]))
            result = result + (qe[i] - conta) ** 2

        except:
            result += 100000000

    return result


def toth(x, T, P, qe, Tref):
    result = 0
    for i in range(len(P)):
        try:
            conta = (x[0] * math.exp(x[2] * ((1 / T[i]) - (1 / Tref))) * x[1] * P[i]) / ((
                                                                                                 1 + (math.exp(x[2] * (
                                                                                                 1 / T[
                                                                                             i] - 1 / Tref)) * x[
                                                                                                          1] * P[
                                                                                                          i]) ** (
                                                                                                     x[3])) ** (
                                                                                                 1 / x[3]))
            result = result + (qe[i] - conta) ** 2

        except:
            result += 100000000

    return result



T = [298.15, 298.15, 298.15, 298.15, 298.15, 298.15, 298.15, 298.15, 298.15, 298.15, 298.15, 298.15, 298.15, 298.15,
     308.15, 308.15, 308.15, 308.15, 308.15, 308.15, 308.15, 308.15, 308.15, 308.15, 308.15, 308.15, 308.15, 308.15,
     323.15, 323.15, 323.15, 323.15, 323.15, 323.15, 323.15, 323.15, 323.15, 323.15, 323.15, 323.15, 323.15, 323.15]

X = [0, 0.0118, 0.061, 0.2905, 0.861, 1.6, 3.1, 5.25, 10.15, 14.45, 19.35, 22.8, 26.6, 32, 0, 0.0126, 0.0407, 0.0905,
     0.1325, 0.2007, 0.4515, 0.9503, 1.6, 2.2, 2.8, 3.7, 4.85, 5.7, 0, 0.0106, 0.0214, 0.0501, 0.0907, 0.2423, 0.422,
     0.7503, 1.45, 2.7, 3.9, 5.45, 7.05, 8.5]

Y = [0, 1.147, 2.249, 3.659, 4.5, 5.06, 5.58, 6.04, 6.52, 6.92, 6.96, 7.09, 7.22, 7.372, 0, 0.825, 1.458, 2.06, 2.4,
     2.734, 3.38, 4.05, 4.49, 4.74, 4.96, 5.167, 5.315, 5.399, 0, 0.356, 0.529, 1.06, 1.43, 2.09, 2.49, 2.9, 3.4, 3.915,
     4.1, 4.329, 4.532, 4.74]

print(chama_pso(T, X, Y, 273.15, 2, pop_size=200, max_iter=2000))
