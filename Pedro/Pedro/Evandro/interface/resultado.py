import flet as ft
import numpy as np
import matplotlib.pyplot as plt
import math
from flet_core.matplotlib_chart import MatplotlibChart
import scipy.stats as st


def main(list_T, list_P, list_q, Tref, model, parameters, resultados):
    principal = ft.Column(controls=[], alignment=ft.MainAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO,
                          width=800, spacing=10)
    qmax = resultados[0][0]
    k1 = resultados[0][1]
    k2 = resultados[0][2]
    other = 0
    erro = resultados[1]
    if len(parameters) > 6:
        other = resultados[0][3]

    container_width = 120
    container_height = 50
    text_q = ft.TextField(label="qmax", value=round(qmax, 4), read_only=True, width=container_width,
                          height=container_height)
    text_k1 = ft.TextField(label="K1", value=round(k1, 4), read_only=True, width=container_width,
                           height=container_height)
    text_k2 = ft.TextField(label="K2", value=round(k2, 4), read_only=True, width=container_width,
                           height=container_height)
    text_other = ft.TextField(label="", value=round(other, 4), read_only=True, width=container_width,
                              height=container_height)

    text_erroQ = ft.TextField(label="Erro quadrático", value=round(erro, 4), read_only=True, width=container_width,
                              height=container_height)

    # Estatísticas - Média dos parâmetros
    qe_sim = __call_model(model, [qmax, k1, k2, other], list_T, list_P, Tref)
    correlation = np.corrcoef(list_q, qe_sim)[0, 1]
    r2 = math.pow(correlation, 2)
    erros_list = []
    for i in range(len(qe_sim)):
        erros_list.append(abs(qe_sim[i] - list_q[i]))
    media_erros = np.mean(erros_list)
    std_erros = np.std(erros_list)
    max_erro = np.max(erros_list)
    min_erro = np.min(erros_list)
    intervalo = st.t.interval(0.95, len(erros_list) - 1, loc=np.mean(erros_list), scale=st.sem(erros_list))
    text_media_erros = ft.TextField(label="Média", value=round(media_erros, 4), read_only=True, width=container_width,
                                    height=container_height)
    text_std_erros = ft.TextField(label="Desvio padrão", value=round(std_erros, 4), read_only=True,
                                  width=container_width,
                                  height=container_height)

    text_erro_min = ft.TextField(label="Erro mínimo", value=round(min_erro, 4), read_only=True, width=container_width,
                                 height=container_height)
    text_erro_max = ft.TextField(label="Erro máximo", value=round(max_erro, 4), read_only=True, width=container_width,
                                 height=container_height)
    intervalo_str = "(" + str(round(intervalo[0], 4)) + " , " + str(round(intervalo[1], 4)) + ")"
    text_intervalo = ft.TextField(label="Intervalo de confiança", value=intervalo_str, read_only=True,
                                  width=(2 * container_width + 10),
                                  height=container_height)
    linha_est_erros1 = ft.Row([text_media_erros, text_std_erros])
    linha_est_erros2 = ft.Row([text_erro_min, text_erro_max])
    linha_est_erros3 = ft.Row([text_intervalo])

    if model == 1:
        text_other.label = "ns"
    elif model == 2:
        text_other.label = "n"
    elif model == 3:
        text_other.label = "α"

    primeira_linha = ft.Row(controls=[], height=80, spacing=10)
    primeira_linha.controls.append(text_q)
    primeira_linha.controls.append(text_k1)
    primeira_linha.controls.append(text_k2)

    if len(parameters) > 6:
        primeira_linha.controls.append(text_other)

    principal.controls.append(ft.Divider())
    principal.controls.append(ft.Text("Parâmetros"))
    principal.controls.append(primeira_linha)

    principal.controls.append(ft.Divider())
    principal.controls.append(ft.Text("Estatística dos Resíduos - Média dos Parâmetros"))
    principal.controls.append(text_erroQ)
    principal.controls.append(linha_est_erros1)
    principal.controls.append(linha_est_erros2)
    principal.controls.append(linha_est_erros3)
    principal.controls.append(ft.Container(height=15))
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
    elif value == 3:
        return __sips(x, T, P, Tref)


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
