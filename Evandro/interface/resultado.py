import flet as ft
import numpy as np
import matplotlib.pyplot as plt
import math
from flet_core.matplotlib_chart import MatplotlibChart

def main(page, coluna_principal, list_T, list_P, list_q, Tref,
         model, pop_size,
         max_iter, parameters, prog_column, resultados):
    principal = ft.Column(controls=[], alignment=ft.MainAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO, width=800)
    qmax = resultados[0][0]
    k1 = resultados[0][1]
    k2 = resultados[0][2]
    other = 0
    erro = resultados[1]
    if len(parameters) > 6:
        other = resultados[0][3]

    text_q = ft.Container(
        content=ft.TextField(label="qmax", value=round(qmax, 8), read_only=True,
                             suffix_text="mol/kg", width=200))
    text_k1 = ft.Container(
        content=ft.TextField(label="K1", value=round(k1, 8), read_only=True,
                              width=200))
    text_k2 = ft.Container(
        content=ft.TextField(label="K2", value=round(k2, 8), read_only=True,
                              width=200))
    text_other = ft.Container(
        content=ft.TextField(label="", value=round(other, 8), read_only=True,
                             width=200))
    text_erroQ = ft.Container(
        content=ft.TextField(label="Erro quadrático", value=round(erro, 8), read_only=True, width=200))

    if model == 1:
        text_other.content.label = "ns"
    elif model == 2:
        text_other.content.label = "n"
    elif model == 3:
        text_other.content.label = "alpha"

    principal.controls.append(text_q)
    principal.controls.append(text_k1)
    principal.controls.append(text_k2)
    if len(parameters) > 6:
        principal.controls.append(text_other)
    principal.controls.append(text_erroQ)

    qe_sim = __call_model(model, [qmax, k1, k2, other], list_T, list_P, 273.15)
    correlation = np.corrcoef(list_q, qe_sim)[0, 1]
    r2 = math.pow(correlation, 2)


    figuraxy = plt.plot(list_q, qe_sim, 'ro', label='Dados Sincronizados')
    plt.xlabel("q Experimental (mol/kg)")
    plt.ylabel("q Simulado (mol/kg)")
    plt.title("Comparação entre dados experimentais e simulados")

    max_value1 = max(list_q)
    max_value2 = max(qe_sim)
    max_value = max(max_value1, max_value2)

    plt.plot([0, max_value], [0, max_value], 'k-')
    plt.text(max_value * 0.05, max_value * 0.9, "r$^2$ = " + str(round(r2, 4)))
    plt.close()
    grafico = MatplotlibChart(figuraxy[0].figure)

    principal.controls.append(ft.Container(content=grafico, width=500))

    return principal


def __call_model(value, x, T, P, Tref):
    if value == 0:
        return __langmuir(x, T, P, Tref)
    elif value == 1:
        return __sips(x, T, P, Tref)
    elif value == 2:
        return __toth(x, T, P, Tref)


def __langmuir(x, T, P, Tref):
    qe_sim = []
    for i in range(len(P)):
        np.seterr(all='ignore')
        qe_sim.append((x[0] * x[1] * math.exp(x[2] * ((1 / T[i]) - (1 / Tref))) * P[i]) / (
                1 + x[1] * math.exp(x[2] * (1 / T[i] - 1 / Tref)) * P[i]))
    return qe_sim


def __sips(x, T, P, Tref):
    qe_sim = []
    for i in range(len(P)):
        np.seterr(all='ignore')
        qe_sim.append((x[0] * (math.exp(x[2] * ((1 / T[i]) - (1 / Tref))) * x[1] * P[i]) ** (1 / x[3])) / (
                1 + (math.exp(x[2] * (1 / T[i] - 1 / Tref)) * x[1] * P[i]) ** (1 / x[3])))
    return qe_sim


def __toth(x, T, P, Tref):
    qe_sim = []
    for i in range(len(P)):
        np.seterr(all='ignore')
        qe_sim.append((x[0] * math.exp(x[2] * ((1 / T[i]) - (1 / Tref)))
                       * x[1] * P[i]) / (math.pow(1 + math.pow(math.exp(x[2] * (1 / T[i] - 1 / Tref))
                                                               * x[1] * P[i], (x[3])), (1 / x[3]))))
    return qe_sim
