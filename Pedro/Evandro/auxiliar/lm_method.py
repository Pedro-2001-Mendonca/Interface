from math import *
import numpy as np
import matplotlib.pyplot as plt
from random import random
from scipy.optimize import root

#transmiter's true location
bx_t = 0.7
by_t = 0.37

#define beacon location
x_beac = [0.7984,0.9430, 0.683741, 0.1321,0.7227, 0.1104, 0.1175, 0.6407
          ,0.3288,0.6538]
y_beac = [0.7491, 0.5832, 0.7400, 0.2348 , 0.7350, 0.9706, 0.8669, 0.0862
    , 0.3664, 0.3692]

#generate noisy data y and initial guess
noise_level = 0.05
y = np.empty(10)

for i in range(10):
    dx = bx_t-x_beac[i]
    dy = by_t-y_beac[i]
    y[i] = sqrt(dx**2 + dy**2)+noise_level*random()
b_init = np.array([0.4, 0.9])

#function phi to minimize


def phi(x):
    s = 0
    for i in range(10):
        dx = x[0]-x_beac[i]
        dy = x[1]-y_beac[i]
        ss = sqrt(dx**2 + dy**2)-y[i]
        s+= ss**2
    return s


def grad_phi(x):
    f0 = 0
    f1 = 0
    for i in range(10):
        dx = x[0]-x_beac[i]
        dy = y[i]-y_beac[i]
        d = 1/sqrt(dx**2 + dy**2)
        f0 += 2*dx-2*y[i]*dx*d
        f1 += 2*dy-2*y[i]*dy*d
    return np.array([f0,f1])


sol = root(grad_phi,b_init, jac = False, method = 'lm')

print("Predicted location: " + str(sol.x))
print("grad phi: " + str(grad_phi(sol.x)))
print("phi: " + str(phi(sol.x)))




####