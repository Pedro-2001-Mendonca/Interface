
import xlsxwriter
import flet as ft
import pandas as pd
import math

from flet_core.matplotlib_chart import MatplotlibChart

from Evandro.classes import experiment_class as ec
from Evandro.auxiliar import synchronization as sync
from Evandro.db import db_experiment as db
import matplotlib.pyplot as plt

def main(page, tab_name):

    principal = ft.Column(alignment=ft.MainAxisAlignment.START, scroll=ft.ScrollMode.ALWAYS,  spacing=25)

    input_heigth = 50
    input_cursor_height = 25
    input_width = 250

    #inputs do leito
    inputL_bed = ft.TextField(label="Comprimento", suffix_text="(m)", height=input_heigth, cursor_height=input_cursor_height, width=input_width)
    inputD_bed = ft.TextField(label="Diâmetro", suffix_text="(m)", height=input_heigth, cursor_height=input_cursor_height, width=input_width)
    label_row = ft.Row(controls=[ft.Text("Propriedades do Leito")],  spacing=25)
    row_input_leito = ft.Row(controls=[inputL_bed, inputD_bed], spacing=25)
    container_espaco = ft.Container(content=None, height=10)
    column_input_leito = ft.Column(controls=[container_espaco, label_row, row_input_leito],  spacing=5)
    container_leito = ft.Container(content=column_input_leito)
    #inputL_bed.value = "0.1921"
    #inputD_bed.value = "0.0211"




    #inputs adsorvente
    inputM_ads = ft.TextField(label="Massa", suffix_text="(kg)", height=input_heigth, cursor_height=input_cursor_height, width=input_width)
    inputPorosidade = ft.TextField(label="Porosidade", height=input_heigth, cursor_height=input_cursor_height, width=input_width)
    label_row_ads = ft.Row(controls=[ft.Text("Propriedades do Adsorvente")], spacing=25)
    row_input_ads = ft.Row(controls=[inputM_ads, inputPorosidade], spacing=25)
    column_input_ads = ft.Column(controls=[label_row_ads, row_input_ads], spacing=5)
    container_ads = ft.Container(content=column_input_ads)
    #inputM_ads.value = "0.0383"
    #inputPorosidade.value = "0.5671"

    #inputs_entrada
    inputP_in = ft.TextField(label="Pressão", suffix_text="(bar)", height=input_heigth, cursor_height=input_cursor_height, width=input_width)
    inputT_in = ft.TextField(label="Temperatura", suffix_text="(K)", height=input_heigth, cursor_height=input_cursor_height, width=input_width)
    inputQ_in = ft.TextField(label="Vazão", suffix_text="(L/min)", height=input_heigth, cursor_height=input_cursor_height, width=input_width)
    inputy_in = ft.TextField(label="Fração molar", height=input_heigth, cursor_height=input_cursor_height, width=input_width)
    label_row_in = ft.Row(controls=[ft.Text("Dados de Entrada")], spacing=25)
    row_input_in1 = ft.Row(controls=[inputP_in, inputT_in], spacing=25)
    container_espaco_in = ft.Container(content=None, height=5)
    row_input_in2 = ft.Row(controls=[inputQ_in, inputy_in], spacing=25)
    column_input_in = ft.Column(controls=[label_row_in, row_input_in1, container_espaco_in, row_input_in2], spacing=5)
    container_in = ft.Container(content=column_input_in)
    #inputP_in.value = "1"
    #inputT_in.value = "298.15"
    #inputQ_in.value = "0.5"
    #inputy_in.value = "0.6"

    #input_sincronização
    input_sync_t = ft.TextField(label="Tempo Final",  height=input_heigth,
                             cursor_height=input_cursor_height, width=input_width)
    input_sync_int = ft.TextField(label="Número de Intervalos",  height=input_heigth,
                             cursor_height=input_cursor_height, width=input_width)
    label_row_sync = ft.Row(controls=[ft.Text("Sincronização")], spacing=25)
    row_input_sync = ft.Row(controls=[input_sync_t, input_sync_int], spacing=25)
    column_input_sync = ft.Column(controls=[label_row_sync, row_input_sync], spacing=5)
    container_sync = ft.Container(content=column_input_sync)

    input_column = ft.Column(controls=[container_leito, ft.Divider(thickness=0.5), container_ads,
                                       ft.Divider(thickness=0.5), container_in, ft.Divider(thickness=0.5),
                                       container_sync], spacing=7)
    input_container = ft.Container(content=input_column)

    principal.controls.insert(0, input_container)


    def seleciona_arquivo(e: ft.FilePickerResultEvent):
        if e.files != None:
            for f in e.files:
                arquivo = f.path
            cria_textfields(arquivo)

    seleciona_arquivo_dialog = ft.FilePicker(on_result=seleciona_arquivo)
    fp = ft.ElevatedButton("Carregar arquivo", on_click=seleciona_arquivo_dialog.pick_files)

    linha1 = ft.Row(alignment=ft.MainAxisAlignment.START,)
    linha1.controls.insert(0, fp)
    principal.controls.insert(1, linha1)
    principal.controls.insert(2, ft.Column(controls=None))

    vetorQ = []
    vetorTempoQ = []
    vetorT = []
    vetorTempoT = []
    vetoryCO2 = []
    vetoryCH4 = []
    vetorTempoy = []

    def cria_textfields(arquivo):

        if principal.controls[2] is not None:
            principal.controls[2].clean()
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
                elif col == 'yCH4' and value >= 0:
                    vetoryCH4.append(value)
                elif col == 'yCO2' and value >= 0:
                    vetoryCO2.append(value)

        not_synchronized_experiment = ec.NotSynchronizedExperiment(
            "tab_name",
            float(inputP_in.value),
            float(inputQ_in.value),
            float(inputT_in.value),
            float(inputy_in.value),
            float(inputM_ads.value),
            float(inputL_bed.value),
            float(inputD_bed.value),
            vetorTempoy,
            vetorTempoT,
            vetorTempoQ,
            vetorT,
            vetorQ,
            vetoryCH4,
            "K",
            "bar",
            "L/min",
            5,
            float(inputPorosidade.value)
        )

        sync_experiment = sync.synchronize(
            not_synchronized_experiment,
            not_synchronized_experiment.time_y_column[0],
            float(input_sync_t.value),
            int(input_sync_int.value)
        )

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


            vetorCol.controls.insert(i+1, ft.Row(vetorLinha, alignment=ft.MainAxisAlignment.START))
            vetorCol_Export.append(vetorLinha_Export)

        intFoutCH4 = 0
        intFoutCO2 = 0
        for i in range(1, len(sync_experiment.time_column)):
            intFoutCH4 += (((sync_experiment.f_out_column[i] + sync_experiment.f_out_column[i - 1]) / 2) * 60 *
                           (sync_experiment.time_column[i] - sync_experiment.time_column[i - 1]))
            intFoutCO2 += (((sync_experiment.f_out_column[i] + sync_experiment.f_out_column[i - 1]) / 2) * 60 *
                           (sync_experiment.time_column[i] - sync_experiment.time_column[i - 1]))

        print("Integral FoutCH4 = " + str(intFoutCH4))
        #print("Integral FoutCO2 = " + str(intFoutCO2))

        Gascte = 0.08314462
        Lbed = 0.1921
        dbed = 0.0211
        Vbed = 1000 * (dbed ** 2) * Lbed * 0.25 * math.pi
        epsilonL = 0.5671
        mads = 0.0383
        Qin = 0.5 / 60  # L/s
        Tin = 298.15
        CinCH4 = 1 * 0.6 / (Gascte * Tin)  # mol/L
        CinCO2 = 1 * 0.4 / (Gascte * Tin)  # mol/L
        qch4 = (CinCH4 * Qin * 60 * (
                    sync_experiment.time_column[len(sync_experiment.time_column) - 1] - sync_experiment.time_column[0]) - intFoutCH4 - CinCH4 * Vbed * epsilonL) / mads
        qco2 = (CinCO2 * Qin * 60 * (
                vetorTempoy[len(vetorTempoy) - 1] - vetorTempoy[0]) - intFoutCO2 - CinCO2 * Vbed * epsilonL) / mads
        print("qCH4 = " + str(qch4))

        #workbook = xlsxwriter.Workbook('dados_tratados.xlsx')
        #worksheet = workbook.add_worksheet()

        row = 0

        #for col, data in enumerate(vetorCol_Export):
           # worksheet.write_column(row, col, data)

        nCols = 5


        #workbook.close()

        figura1 = plt.plot(not_synchronized_experiment.time_temperature_column,
                           not_synchronized_experiment.temperature_column, 'r-o')
        plt.xlabel("tempo (min)")
        plt.ylabel("temperatura (K)")
        plt.close()
        figura11 = plt.plot(sync_experiment.time_column, sync_experiment.temperature_column, 'r-o')
        plt.xlabel("tempo (min)")
        plt.ylabel("temperatura (K)")
        plt.close()

        figura2 = plt.plot(not_synchronized_experiment.time_flow_column,
                           not_synchronized_experiment.flow_column, 'b-o')
        plt.xlabel("tempo (min)")
        plt.ylabel("vazão (ml/min)")
        plt.close()
        figura22 = plt.plot(sync_experiment.time_column, sync_experiment.flow_column, 'b-o')
        plt.xlabel("tempo (min)")
        plt.ylabel("vazão (ml/min)")
        plt.close()

        figura3 = plt.plot(not_synchronized_experiment.time_y_column,
                           not_synchronized_experiment.y_column, 'k-o')
        plt.xlabel("tempo (min)")
        plt.ylabel("fração molar")
        plt.close()
        figura33 = plt.plot(sync_experiment.time_column, sync_experiment.y_column, 'k-o')
        plt.xlabel("tempo (min)")
        plt.ylabel("fração molar")
        plt.close()

        grafico1 = MatplotlibChart(figura1[0].figure)
        grafico11 = MatplotlibChart(figura11[0].figure)

        grafico2 = MatplotlibChart(figura2[0].figure)
        grafico22 = MatplotlibChart(figura22[0].figure)

        grafico3 = MatplotlibChart(figura3[0].figure)
        grafico33 = MatplotlibChart(figura33[0].figure)

        row_figure1 = ft.Row([grafico1,grafico11])
        fig_container1 = ft.Container(content=row_figure1, width=1000, height=400,)

        row_figure2 = ft.Row([grafico2, grafico22])
        fig_container2 = ft.Container(content=row_figure2, width=1000, height=400)

        row_figure3 = ft.Row([grafico3, grafico33])
        fig_container3 = ft.Container(content=row_figure3, width=1000, height=400)

        fig_column = ft.Column(controls=[fig_container1, fig_container2, fig_container3], spacing=0)

        def __salvar__():
            db.__create_db_ns_experiment__(tab_name, not_synchronized_experiment)

        salvar = ft.ElevatedButton("Salvar", on_click=lambda _: __salvar__())
        if len(linha1.controls) == 1:
            linha1.controls.insert(1, salvar)

        text_q = ft.Container(
            content=ft.TextField(label="Quantidade Adsorvida (q)", value=round(qch4, 8), read_only=True,
                                 suffix_text="L/kg", width=200))
        if len(principal.controls) > 2:
            principal.controls.remove(vetorCol)
            principal.controls.remove(text_q)
            principal.controls.remove(fig_column)

        principal.controls.insert(2, vetorCol)
        principal.controls.insert(3, text_q)
        principal.controls.insert(4, fig_column)
        principal.update()

    page.overlay.append(seleciona_arquivo_dialog)
    page.update()
    return principal
