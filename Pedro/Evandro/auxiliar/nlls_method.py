import sympy as sp
from sympy import exp, I, pi
import numpy as np
import time
from sympy import *
import math

dadosPCH4 = [0, 0.04, 0.12, 0.19, 0.55, 1.25, 1.65, 2.1, 3.06, 3.45, 4.25, 6.31, 8.19, 10.7, 11.8, 14.1, 17.2, 18.9]
dadosQCH4 = [0, 0.02, 0.089, 0.13, 0.33, 0.71, 0.88, 1.12, 1.47, 1.62, 1.83, 2.36, 2.73, 3.06, 3.26, 3.53, 3.83, 3.99]

dadosPCO2 = [0, 0.0118, 0.061, 0.2905, 0.861, 1.6, 3.1, 5.25, 10.15, 14.45, 19.35, 22.8, 26.6, 32]
dadosQCO2 = [0, 1.147, 2.249, 3.659, 4.5, 5.06, 5.58, 6.04, 6.52, 6.92, 6.96, 7.09, 7.22, 7.372]
dadosT = [298.15, 298.15, 298.15, 298.15, 298.15, 298.15, 298.15, 298.15, 298.15, 298.15, 298.15, 298.15, 298.15,
          298.15, 298.15, 298.15, 298.15, 298.15, 298.15, 298.15, 298.15, 298.15, 298.15]
Alpha = Symbol('Alpha')
K1 = Symbol('K1')
K2 = Symbol('K2')
Qmax = Symbol('Qmax')
X = Symbol('X')
Y = Symbol('Y')
T = Symbol('T')
Tref = 273.15

Fobj = (Y - Qmax * K1 * exp(K2 * (-1 / T + 1 / Tref)) * X * (1 - Y / Qmax) ** Alpha) ** 2

Fobj_subs = 0
for i in range(0, len(dadosPCO2)):
    #Fobj_subs = Fobj_subs + Fobj.subs([(X, dadosPCH4[i],), (Y, dadosQCH4[i]), (T, dadosT[i])])
    Fobj_subs = Fobj_subs + Fobj.subs([(X, dadosPCO2[i],), (Y, dadosQCO2[i]), (T, dadosT[i])])


def f(a, b, c, d):
    return float(Fobj_subs.subs([(Alpha, a), (K1, b), (K2, c), (Qmax, d)]))


def gradf(a, b, c, d):
    jacobian = np.array([diff(Fobj_subs, Alpha).subs([(Alpha, a), (K1, b), (K2, c), (Qmax, d)]),
                         diff(Fobj_subs, K1).subs([(Alpha, a), (K1, b), (K2, c), (Qmax, d)]),
                         diff(Fobj_subs, K2).subs([(Alpha, a), (K1, b), (K2, c), (Qmax, d)]),
                         diff(Fobj_subs, Qmax).subs([(Alpha, a), (K1, b), (K2, c), (Qmax, d)])], dtype='float64')
    return jacobian


def hessianf(a, b, c, d):
    hessian = np.array([[diff(Fobj_subs, Alpha, Alpha).subs([(Alpha, a), (K1, b), (K2, c), (Qmax, d)]),
                         diff(Fobj_subs, Alpha, K1).subs([(Alpha, a), (K1, b), (K2, c), (Qmax, d)]),
                         diff(Fobj_subs, Alpha, K2).subs([(Alpha, a), (K1, b), (K2, c), (Qmax, d)]),
                         diff(Fobj_subs, Alpha, Qmax).subs([(Alpha, a), (K1, b), (K2, c), (Qmax, d)])],
                        [diff(Fobj_subs, K1, Alpha).subs([(Alpha, a), (K1, b), (K2, c), (Qmax, d)]),
                         diff(Fobj_subs, K1, K1).subs([(Alpha, a), (K1, b), (K2, c), (Qmax, d)]),
                         diff(Fobj_subs, K1, K2).subs([(Alpha, a), (K1, b), (K2, c), (Qmax, d)]),
                         diff(Fobj_subs, K1, Qmax).subs([(Alpha, a), (K1, b), (K2, c), (Qmax, d)])],
                        [diff(Fobj_subs, K2, Alpha).subs([(Alpha, a), (K1, b), (K2, c), (Qmax, d)]),
                         diff(Fobj_subs, K2, K1).subs([(Alpha, a), (K1, b), (K2, c), (Qmax, d)]),
                         diff(Fobj_subs, K2, K2).subs([(Alpha, a), (K1, b), (K2, c), (Qmax, d)]),
                         diff(Fobj_subs, K2, Qmax).subs([(Alpha, a), (K1, b), (K2, c), (Qmax, d)])],
                        [diff(Fobj_subs, Qmax, Alpha).subs([(Alpha, a), (K1, b), (K2, c), (Qmax, d)]),
                         diff(Fobj_subs, Qmax, K1).subs([(Alpha, a), (K1, b), (K2, c), (Qmax, d)]),
                         diff(Fobj_subs, Qmax, K2).subs([(Alpha, a), (K1, b), (K2, c), (Qmax, d)]),
                         diff(Fobj_subs, Qmax, Qmax).subs([(Alpha, a), (K1, b), (K2, c), (Qmax, d)])],
                        ], dtype='float64')

    return np.linalg.inv(hessian)




def zeroNewton(a, b, c, d, erro):
    xk = [a, b, c, d] - 0.5*np.matmul(hessianf(a, b, c, d), gradf(a, b, c, d))
    print(xk)
    print(abs(f(xk[0], xk[1],xk[2],xk[3])))
    if abs(f(xk[0], xk[1],xk[2],xk[3])) > abs(erro):
        return zeroNewton(xk[0], xk[1],xk[2],xk[3], erro)
    else:
        return xk

#zeroNewton(1, 0.5, 1000, 20, 0.1)

print(gradf(1,1,1,9))
print(gradf(2,2,2,8))