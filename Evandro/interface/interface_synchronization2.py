import xlsxwriter
import flet as ft
import pandas as pd
import math
import numpy as np
from flet_core.matplotlib_chart import MatplotlibChart
from Evandro.auxiliar import load_excel_file as excel

from Evandro.classes import experiment_class as ec
from Evandro.auxiliar import synchronization as sync
from Evandro.db import db_experiment as db

import matplotlib.pyplot as plt

input_height = 50
input_cursor_height = 25
input_width = 250

button_width = 200

# inputs do leito
inputP_in = ft.TextField(label="Pressão", suffix_text="(bar)", height=input_height,
                         cursor_height=input_cursor_height, width=input_width)
inputL_bed = ft.TextField(label="Comprimento", suffix_text="(m)", height=input_height,
                          cursor_height=input_cursor_height, width=input_width)
inputD_bed = ft.TextField(label="Diâmetro", suffix_text="(m)", height=input_height,
                          cursor_height=input_cursor_height, width=input_width)
label_row = ft.Row(controls=[ft.Text("Propriedades do Leito")], spacing=25)
row_input_leito = ft.Row(controls=[inputL_bed, inputD_bed], spacing=25)
container_espaco = ft.Container(content=None, height=10)
column_input_leito = ft.Column(controls=[container_espaco, label_row, row_input_leito], spacing=5)
container_leito = ft.Container(content=column_input_leito)
inputL_bed.value = "0.1921"
inputD_bed.value = "0.0211"

# inputs adsorvente
inputM_ads = ft.TextField(label="Massa", suffix_text="(kg)", height=input_height, cursor_height=input_cursor_height,
                          width=input_width)
inputPorosidade = ft.TextField(label="Porosidade", height=input_height, cursor_height=input_cursor_height,
                               width=input_width)
label_row_ads = ft.Row(controls=[ft.Text("Propriedades do Adsorvente")], spacing=25)
row_input_ads = ft.Row(controls=[inputM_ads, inputPorosidade], spacing=25)
column_input_ads = ft.Column(controls=[label_row_ads, row_input_ads], spacing=5)
container_ads = ft.Container(content=column_input_ads)
inputM_ads.value = "0.0383"
inputPorosidade.value = "0.5671"

# inputs_entrada

inputT_in = ft.TextField(label="Temperatura", suffix_text="(K)", height=input_height,
                         cursor_height=input_cursor_height, width=input_width)
inputQ_in = ft.TextField(label="Vazão", suffix_text="(L/s)", height=input_height,
                         cursor_height=input_cursor_height, width=input_width)
inputy_in = ft.TextField(label="Fração molar", height=input_height, cursor_height=input_cursor_height,
                         width=input_width)
label_row_in = ft.Row(controls=[ft.Text("Dados de Entrada")], spacing=25)
row_input_in1 = ft.Row(controls=[inputP_in, inputT_in], spacing=25)
container_espaco_in = ft.Container(content=None, height=5)
row_input_in2 = ft.Row(controls=[inputQ_in, inputy_in], spacing=25)
column_input_in = ft.Column(controls=[label_row_in, row_input_in1, container_espaco_in, row_input_in2], spacing=5)
container_in = ft.Container(content=column_input_in)
inputP_in.value = "1"
inputT_in.value = "297.15"
inputQ_in.value = "0.008333"
inputy_in.value = "0.6"

# input_sincronização
input_sync_t = ft.TextField(label="Tempo Final", height=input_height,
                            cursor_height=input_cursor_height, width=input_width, suffix_text="(s)")
input_sync_t.value = "1140"
input_sync_int = ft.TextField(label="Número de Intervalos", height=input_height,
                              cursor_height=input_cursor_height, width=input_width)
input_sync_int.value = "100"

label_row_sync = ft.Row(controls=[ft.Text("Sincronização")], spacing=25)
row_input_sync = ft.Row(controls=[input_sync_t, input_sync_int], spacing=25)
column_input_sync = ft.Column(controls=[label_row_sync, row_input_sync], spacing=5)
container_sync = ft.Container(content=column_input_sync)

input_column = ft.Column(controls=[container_leito, ft.Divider(thickness=0.5), container_ads,
                                   ft.Divider(thickness=0.5), container_in, ft.Divider(thickness=0.5),
                                   container_sync], spacing=7)
input_container = ft.Container(content=input_column)


def main(page, tab_name):
    principal = ft.Column(alignment=ft.MainAxisAlignment.START, scroll=ft.ScrollMode.ALWAYS, spacing=25)

    principal.controls.insert(0, input_container)

    def seleciona_arquivo(e: ft.FilePickerResultEvent):

        if e.files != None:
            for f in e.files:
                arquivo = f.path
            cria_textfields(arquivo)

    seleciona_arquivo_dialog = ft.FilePicker(on_result=seleciona_arquivo)

    fp = ft.ElevatedButton("Carregar Planilha", on_click=lambda _: seleciona_arquivo_dialog.pick_files(
        allowed_extensions=["xlsx"]), width=button_width)

    linha1 = ft.Row(alignment=ft.MainAxisAlignment.START, )
    linha1.controls.insert(0, fp)

    principal.controls.insert(1, linha1)
    principal.controls.insert(2, ft.Column(controls=None))

    def cria_textfields(arquivo):

        vetorQ = []
        vetorTempoQ = []
        vetorT = []
        vetorTempoT = []
        vetory = []
        vetorTempoy = []

        while len(principal.controls) > 2:
            principal.controls.remove(principal.controls[2])

        excel = pd.read_excel(arquivo)

        for index, row in excel.iterrows():

            for col, value in row.items():
                if col == 'tempoT' and value >= 0:
                    vetorTempoT.append(value)
                elif col == 'T' and value >= 0:
                    vetorT.append(value)
                elif col == 'tempoQ' and value >= 0:
                    vetorTempoQ.append(value)
                elif col == 'Q' and value >= 0:
                    vetorQ.append(value)
                elif col == 'tempoy' and value >= 0:
                    vetorTempoy.append(value)
                elif col == 'y' and value >= 0:
                    vetory.append(value)

        not_synchronized_experiment = ec.NotSynchronizedExperiment(
            "tab_name",
            float(__return_input_value__(inputP_in.value)),
            float(__return_input_value__(inputQ_in.value)),
            float(__return_input_value__(inputT_in.value)),
            float(__return_input_value__(inputy_in.value)),
            float(__return_input_value__(inputM_ads.value)),
            float(__return_input_value__(inputL_bed.value)),
            float(__return_input_value__(inputD_bed.value)),
            vetorTempoy,
            vetorTempoT,
            vetorTempoQ,
            vetorT,
            vetorQ,
            vetory,
            "K",
            "bar",
            "L/min",
            float(__return_input_value__(inputPorosidade.value))
        )

        vetorCol = ft.Column(controls=None, alignment=ft.MainAxisAlignment.CENTER)
        vetorCol.controls.clear()

        titulo_size = 15
        vertical_up = -0.9
        newheigth = 35

        vetorCol.controls.append(ft.TextField("Dados não sincronizados", text_align=ft.TextAlign.START,
                                              text_size=titulo_size,
                                              width=250,
                                              height=newheigth,
                                              text_vertical_align=vertical_up,
                                              content_padding=ft.padding.only(left=5, right=2, bottom=18),
                                              border=ft.InputBorder.NONE, read_only=True))

        vetorLinha = []

        vetorLinha.append(ft.TextField("Tempo - Temp. (s)", text_align=ft.TextAlign.CENTER, text_size=titulo_size,
                                       width=150,
                                       height=newheigth,
                                       text_vertical_align=vertical_up,
                                       content_padding=ft.padding.only(left=5, right=2, bottom=18),
                                       border=ft.InputBorder.NONE, read_only=True))
        vetorLinha.append(
            ft.TextField("Temperatura (K)", text_align=ft.TextAlign.CENTER, width=150, text_size=titulo_size,
                         height=newheigth,
                         text_vertical_align=vertical_up, content_padding=ft.padding.only(left=5, right=2, bottom=18),
                         border=ft.InputBorder.NONE, read_only=True))
        vetorLinha.append(
            ft.TextField("Tempo - Vazão (s)", text_align=ft.TextAlign.CENTER, width=150, text_size=titulo_size,
                         height=newheigth,
                         text_vertical_align=vertical_up,
                         content_padding=ft.padding.only(left=5, right=2, bottom=18),
                         border=ft.InputBorder.NONE, read_only=True))
        vetorLinha.append(
            ft.TextField("Vazão (L/s)", text_align=ft.TextAlign.CENTER, width=150, text_size=titulo_size,
                         height=newheigth,
                         text_vertical_align=vertical_up, content_padding=ft.padding.only(left=5, right=2, bottom=18),
                         border=ft.InputBorder.NONE, read_only=True))
        vetorLinha.append(
            ft.TextField("Tempo - F. Mol. (s)", text_align=ft.TextAlign.CENTER, width=150, text_size=titulo_size,
                         height=newheigth,
                         text_vertical_align=vertical_up,
                         content_padding=ft.padding.only(left=5, right=2, bottom=18),
                         border=ft.InputBorder.NONE, read_only=True))
        vetorLinha.append(ft.TextField("Fração Molar", text_align=ft.TextAlign.CENTER, width=150, text_size=titulo_size,
                                       height=newheigth,
                                       text_vertical_align=-1,
                                       content_padding=ft.padding.only(left=5, right=2, bottom=18),
                                       border=ft.InputBorder.NONE, read_only=True))
        vetorCol.controls.insert(1, ft.Row(vetorLinha, alignment=ft.MainAxisAlignment.START))
        # vetorCol_Export = []

        for i in range(np.max([len(vetorTempoT), len(vetorTempoQ), len(vetorTempoy)])):
            vetorLinha = []
            # vetorLinha_Export = []

            if i < len(vetorTempoT):
                vetorLinha.append(ft.TextField(round(vetorTempoT[i], 5), text_align=ft.TextAlign.CENTER,
                                               width=150,
                                               height=newheigth,
                                               text_vertical_align=-0.73,
                                               content_padding=ft.padding.only(left=5, right=2)))
                vetorLinha.append(
                    ft.TextField(round(vetorT[i], 5), text_align=ft.TextAlign.CENTER, width=150,
                                 height=newheigth,
                                 text_vertical_align=-0.73, content_padding=ft.padding.only(left=5, right=2)))
            else:
                vetorLinha.append(
                    ft.TextField('-', text_align=ft.TextAlign.CENTER, width=150,
                                 height=newheigth,
                                 text_vertical_align=-0.73, content_padding=ft.padding.only(left=5, right=2)))
                vetorLinha.append(
                    ft.TextField('-', text_align=ft.TextAlign.CENTER, width=150,
                                 height=newheigth,
                                 text_vertical_align=-0.73, content_padding=ft.padding.only(left=5, right=2)))
            if i < len(vetorTempoQ):
                vetorLinha.append(ft.TextField(round(vetorTempoQ[i], 5), text_align=ft.TextAlign.CENTER,
                                               width=150,
                                               height=newheigth,
                                               text_vertical_align=-0.73,
                                               content_padding=ft.padding.only(left=5, right=2)))
                vetorLinha.append(
                    ft.TextField(round(vetorQ[i], 5), text_align=ft.TextAlign.CENTER, width=150,
                                 height=newheigth,
                                 text_vertical_align=-0.73, content_padding=ft.padding.only(left=5, right=2)))
            else:
                vetorLinha.append(
                    ft.TextField('-', text_align=ft.TextAlign.CENTER, width=150,
                                 height=newheigth,
                                 text_vertical_align=-0.73, content_padding=ft.padding.only(left=5, right=2)))
                vetorLinha.append(
                    ft.TextField('-', text_align=ft.TextAlign.CENTER, width=150,
                                 height=newheigth,
                                 text_vertical_align=-0.73, content_padding=ft.padding.only(left=5, right=2)))

            if i < len(vetorTempoy):
                vetorLinha.append(ft.TextField(round(vetorTempoy[i], 5), text_align=ft.TextAlign.CENTER,
                                               width=150,
                                               height=newheigth,
                                               text_vertical_align=-0.73,
                                               content_padding=ft.padding.only(left=5, right=2)))
                vetorLinha.append(
                    ft.TextField(round(vetory[i], 5), text_align=ft.TextAlign.CENTER, width=150,
                                 height=newheigth,
                                 text_vertical_align=-0.73, content_padding=ft.padding.only(left=5, right=2)))
            else:
                vetorLinha.append(
                    ft.TextField('-', text_align=ft.TextAlign.CENTER, width=150,
                                 height=newheigth,
                                 text_vertical_align=-0.73, content_padding=ft.padding.only(left=5, right=2)))
                vetorLinha.append(
                    ft.TextField('-', text_align=ft.TextAlign.CENTER, width=150,
                                 height=newheigth,
                                 text_vertical_align=-0.73, content_padding=ft.padding.only(left=5, right=2)))
            # vetorLinha_Export.append(sync_experiment.time_column[i])
            # vetorLinha_Export.append(sync_experiment.temperature_column[i])
            # vetorLinha_Export.append(sync_experiment.flow_column[i])
            # vetorLinha_Export.append(sync_experiment.y_column[i])

            vetorCol.controls.insert(i + 2, ft.Row(vetorLinha, alignment=ft.MainAxisAlignment.START))

        while len(principal.controls) > 2:
            principal.controls.remove(principal.controls[2])

        principal.controls.insert(2, vetorCol)

        __update_sync__(not_synchronized_experiment)
        #not_synchronized_experiment.inlet_pressure = float(__return_input_value__(inputP_in.value))
        #not_synchronized_experiment.inlet_flow = float(__return_input_value__(inputQ_in.value))
        #not_synchronized_experiment.inlet_temperature = float(__return_input_value__(inputT_in.value))
        #not_synchronized_experiment.inlet_y = float(__return_input_value__(inputy_in.value))
        #not_synchronized_experiment.adsorbent_mass = float(__return_input_value__(inputM_ads.value))
        #not_synchronized_experiment.bed_length = float(__return_input_value__(inputL_bed.value))
        #not_synchronized_experiment.bed_diameter = float(__return_input_value__(inputD_bed.value))
        #not_synchronized_experiment.porosity = float(__return_input_value__(inputPorosidade.value))

        sync_bt = ft.ElevatedButton("Sincronizar",
                                    on_click=lambda _: __sincronizar_dados__(principal, not_synchronized_experiment,
                                                                             linha1, page), width=button_width)
        while len(linha1.controls) > 1:
            linha1.controls.remove(linha1.controls[1])
        linha1.controls.insert(1, sync_bt)

        principal.update()

    page.overlay.append(seleciona_arquivo_dialog)
    page.update()
    return principal


def __return_input_value__(input):
    if input != '':
        return input
    else:
        return 0


def __sincronizar_dados__(
        principal,
        ns_exp, linha1, page):
    principal.update()
    sync_experiment = sync.synchronize(
        ns_exp,
        ns_exp.time_y_column[0],
        float(__return_input_value__(input_sync_t.value)),
        int(__return_input_value__(input_sync_int.value))
    )

    __update_sync__(sync_experiment)
    #sync_experiment.inlet_pressure = float(__return_input_value__(inputP_in.value))
    #sync_experiment.inlet_flow = float(__return_input_value__(inputQ_in.value))
    #sync_experiment.inlet_temperature = float(__return_input_value__(inputT_in.value))
    #sync_experiment.inlet_y = float(__return_input_value__(inputy_in.value))
    #sync_experiment.adsorbent_mass = float(__return_input_value__(inputM_ads.value))
    #sync_experiment.bed_length = float(__return_input_value__(inputL_bed.value))
    #sync_experiment.bed_diameter = float(__return_input_value__(inputD_bed.value))
    #sync_experiment.porosity = float(__return_input_value__(inputPorosidade.value))


    vetorCol = ft.Column(controls=None)
    vetorCol.controls.clear()
    vetorLinha = []
    newheigth = 35
    vetorLinha.append(ft.TextField("Tempo (s)", text_align=ft.TextAlign.CENTER, width=150,
                                   height=newheigth,
                                   text_vertical_align=-1,
                                   content_padding=ft.padding.only(left=5, right=2, bottom=18),
                                   border=ft.InputBorder.NONE, read_only=True))
    vetorLinha.append(ft.TextField("Temperatura (K)", text_align=ft.TextAlign.CENTER, width=150,
                                   height=newheigth,
                                   text_vertical_align=-1, content_padding=ft.padding.only(left=5, right=2, bottom=18),
                                   border=ft.InputBorder.NONE, read_only=True))
    vetorLinha.append(ft.TextField("Vazão (L/min)", text_align=ft.TextAlign.CENTER, width=150,
                                   height=newheigth,
                                   text_vertical_align=-1, content_padding=ft.padding.only(left=5, right=2, bottom=18),
                                   border=ft.InputBorder.NONE, read_only=True))
    vetorLinha.append(ft.TextField("Fração Molar", text_align=ft.TextAlign.CENTER, width=150,
                                   height=newheigth,
                                   text_vertical_align=-1, content_padding=ft.padding.only(left=5, right=2, bottom=18),
                                   border=ft.InputBorder.NONE, read_only=True))
    vetorCol.controls.insert(0, ft.Row(vetorLinha, alignment=ft.MainAxisAlignment.START))
    vetorCol_Export = []
    for i in range(len(sync_experiment.time_column)):
        vetorLinha = []
        vetorLinha_Export = []

        vetorLinha.append(
            ft.TextField(round(sync_experiment.time_column[i], 5), text_align=ft.TextAlign.CENTER, width=150,
                         height=newheigth,
                         text_vertical_align=-0.73, content_padding=ft.padding.only(left=5, right=2)))
        vetorLinha.append(
            ft.TextField(round(sync_experiment.temperature_column[i], 5), text_align=ft.TextAlign.CENTER, width=150,
                         height=newheigth,
                         text_vertical_align=-0.73, content_padding=ft.padding.only(left=5, right=2)))
        vetorLinha.append(
            ft.TextField(round(sync_experiment.flow_column[i], 5), text_align=ft.TextAlign.CENTER, width=150,
                         height=newheigth,
                         text_vertical_align=-0.73, content_padding=ft.padding.only(left=5, right=2)))
        vetorLinha.append(
            ft.TextField(round(sync_experiment.y_column[i], 5), text_align=ft.TextAlign.CENTER, width=150,
                         height=newheigth,
                         text_vertical_align=-0.73, content_padding=ft.padding.only(left=5, right=2)))
        vetorLinha_Export.append(sync_experiment.time_column[i])
        vetorLinha_Export.append(sync_experiment.temperature_column[i])
        vetorLinha_Export.append(sync_experiment.flow_column[i])
        vetorLinha_Export.append(sync_experiment.y_column[i])

        vetorCol.controls.insert(i + 1, ft.Row(vetorLinha, alignment=ft.MainAxisAlignment.START))
        vetorCol_Export.append(vetorLinha_Export)

    intFoutCH4 = 0

    for i in range(1, len(sync_experiment.time_column)):
        intFoutCH4 += (((sync_experiment.f_out_column[i] + sync_experiment.f_out_column[i - 1]) / 2) *
                       (sync_experiment.time_column[i] - sync_experiment.time_column[i - 1]))

    Gascte = 0.08314462
    Vbed = 1000 * (sync_experiment.bed_diameter ** 2) * sync_experiment.bed_length * 0.25 * math.pi
    epsilonL = sync_experiment.porosity
    mads = sync_experiment.adsorbent_mass
    Qin = sync_experiment.inlet_flow  # L/s
    CinCH4 = sync_experiment.inlet_pressure * sync_experiment.inlet_y / (Gascte * sync_experiment.inlet_temperature)  # mol/L

    qch4 = (CinCH4 * Qin * (
            sync_experiment.time_column[len(sync_experiment.time_column) - 1] - sync_experiment.time_column[
        0]) - intFoutCH4 - CinCH4 * Vbed * epsilonL) / mads

    print("qCH4 = " + str(qch4))

    sync_experiment.q = qch4

    figura1 = plt.plot(ns_exp.time_temperature_column,
                       ns_exp.temperature_column, 'r-o')
    plt.xlabel("tempo (min)")
    plt.ylabel("temperatura (K)")
    plt.title("Dados não sincronizados")
    plt.close()
    figura11 = plt.plot(sync_experiment.time_column, sync_experiment.temperature_column, 'r-o')
    plt.xlabel("tempo (min)")
    plt.ylabel("temperatura (K)")
    plt.title("Dados sincronizados")
    plt.close()

    figura2 = plt.plot(ns_exp.time_flow_column,
                       ns_exp.flow_column, 'b-o')
    plt.xlabel("tempo (s)")
    plt.ylabel("vazão (L/s)")
    plt.title("Dados não sincronizados")
    plt.close()
    figura22 = plt.plot(sync_experiment.time_column, sync_experiment.flow_column, 'b-o')
    plt.xlabel("tempo (s)")
    plt.ylabel("vazão (L/s)")
    plt.title("Dados sincronizados")
    plt.close()

    figura3 = plt.plot(ns_exp.time_y_column,
                       ns_exp.y_column, 'k-o')
    plt.xlabel("tempo (s)")
    plt.ylabel("fração molar")
    plt.title("Dados não sincronizados")
    plt.close()
    figura33 = plt.plot(sync_experiment.time_column, sync_experiment.y_column, 'k-o')
    plt.xlabel("tempo (min)")
    plt.ylabel("fração molar")
    plt.title("Dados sincronizados")
    plt.close()

    grafico1 = MatplotlibChart(figura1[0].figure)
    grafico11 = MatplotlibChart(figura11[0].figure)

    grafico2 = MatplotlibChart(figura2[0].figure)
    grafico22 = MatplotlibChart(figura22[0].figure)

    grafico3 = MatplotlibChart(figura3[0].figure)
    grafico33 = MatplotlibChart(figura33[0].figure)

    row_figure1 = ft.Row([grafico1, grafico11])
    fig_container1 = ft.Container(content=row_figure1, width=1000, height=400, )

    row_figure2 = ft.Row([grafico2, grafico22])
    fig_container2 = ft.Container(content=row_figure2, width=1000, height=400)

    row_figure3 = ft.Row([grafico3, grafico33])
    fig_container3 = ft.Container(content=row_figure3, width=1000, height=400)

    fig_column = ft.Column(controls=[fig_container1, fig_container2, fig_container3], spacing=0)

    text_q = ft.Container(
        content=ft.TextField(label="Quantidade Adsorvida (q)", value=round(qch4, 8), read_only=True,
                             suffix_text="L/kg", width=200))

    def save_file_result(e: ft.FilePickerResultEvent):
        save_file_path = e.path if e.path else None
        if save_file_path:
            __update_sync__(sync_experiment)
            db.__create_db_ns_experiment__(save_file_path.title(), ns_exp)

    save_file_dialog = ft.FilePicker(on_result=save_file_result)

    page.overlay.append(save_file_dialog)

    save_bt = ft.ElevatedButton("Salvar Experimento", on_click=lambda _: save_file_dialog.save_file(
        allowed_extensions=["exp"]), width=button_width)

    def export_file_result(e: ft.FilePickerResultEvent):
        save_file_path = e.path if e.path else None
        if save_file_path:
            __update_sync__(sync_experiment)
            excel.__export__(save_file_path, sync_experiment)

    export_file_dialog = ft.FilePicker(on_result=export_file_result)

    page.overlay.append(export_file_dialog)

    export_bt = ft.ElevatedButton("Exportar Planilha", on_click=lambda _: export_file_dialog.save_file(
        allowed_extensions=["xlsx"]), width=button_width)

    while len(principal.controls) > 2:
        principal.controls.remove(principal.controls[2])
    if len(linha1.controls) < 3:
        linha1.controls.insert(2, save_bt)
        linha1.controls.insert(3, export_bt)

    principal.controls.insert(3, vetorCol)
    principal.controls.insert(4, text_q)
    principal.controls.insert(5, fig_column)
    principal.update()
    page.update()

def __update_sync__(sync_exp):
    sync_exp.inlet_pressure = float(__return_input_value__(inputP_in.value))
    sync_exp.inlet_flow = float(__return_input_value__(inputQ_in.value))
    sync_exp.inlet_temperature = float(__return_input_value__(inputT_in.value))
    sync_exp.inlet_y = float(__return_input_value__(inputy_in.value))
    sync_exp.adsorbent_mass = float(__return_input_value__(inputM_ads.value))
    sync_exp.bed_length = float(__return_input_value__(inputL_bed.value))
    sync_exp.bed_diameter = float(__return_input_value__(inputD_bed.value))
    sync_exp.porosity = float(__return_input_value__(inputPorosidade.value))