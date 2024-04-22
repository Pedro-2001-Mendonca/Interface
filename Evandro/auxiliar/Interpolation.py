import numpy as np


def interpolation(x, y):
    poly = []
    if len(x) != len(y):
        return print("Tamanhos não são iguais!") ##### Corrigir para msg de erro!
    else:
        for i in range(len(x)-1):
            coef = np.polyfit([x[i], x[i+1]], [y[i], y[i+1]], 1)
            poly1d_fn = np.poly1d(coef)
            poly.append(poly1d_fn)
        return poly


def get_position(value, vector):

    for j in range(len(vector)):
        if vector[j] > value:
            return j-1
    return len(vector)-1



