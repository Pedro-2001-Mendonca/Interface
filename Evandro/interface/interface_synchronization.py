
import xlsxwriter
import flet as ft
import pandas as pd
import math
from Evandro.classes import experiment_class as ec
from Evandro.auxiliar import synchronization as sync


def main(page, tab_name):

    principal = ft.Column(alignment=ft.MainAxisAlignment.START, scroll=ft.ScrollMode.ALWAYS, expand=True, spacing=25)
    principal.controls.insert(0, ft.Container(content=None, height=0, width=120))

    def seleciona_arquivo(e: ft.FilePickerResultEvent):
        if e.files != None:
            for f in e.files:
                arquivo = f.path
            cria_textfields(arquivo)

    seleciona_arquivo_dialog = ft.FilePicker(on_result=seleciona_arquivo)
    fp = ft.ElevatedButton("Carregar arquivo", on_click=seleciona_arquivo_dialog.pick_files)

    principal.controls.insert(1, fp)
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
            1,
            500,
            298.15,
            0.0383,
            0.1921,
            0.0211,
            vetorTempoy,
            vetorTempoT,
            vetorTempoQ,
            vetorT,
            vetorQ,
            vetoryCH4,
            "K",
            "bar",
            "L/min"
        )

        sync_experiment = sync.synchronize(
            not_synchronized_experiment,
            not_synchronized_experiment.time_y_column[0],
            19,
            #not_synchronized_experiment.time_y_column[len(not_synchronized_experiment.time_y_column) - 1],
            200
        )


        vetorCol = ft.Column(controls=None)
        vetorCol.controls.clear()
        vetorCol_Export = []
        for i in range(len(sync_experiment.time_column)):
            vetorLinha = []
            vetorLinha_Export = []
            vetorLinha.append(
                ft.Container(content=ft.TextField(sync_experiment.time_column[i],
                                                  width=100, text_align=ft.TextAlign.CENTER)))
            vetorLinha.append(
                ft.Container(content=ft.TextField(sync_experiment.temperature_column[i],
                                                  width=100, text_align=ft.TextAlign.CENTER)))
            vetorLinha.append(
                ft.Container(content=ft.TextField(sync_experiment.flow_column[i],
                                                  width=100, text_align=ft.TextAlign.CENTER)))
            vetorLinha.append(
                ft.Container(content=ft.TextField(sync_experiment.y_column[i],
                                                  width=100, text_align=ft.TextAlign.CENTER)))
            vetorLinha.append(
                ft.Container(content=ft.TextField(sync_experiment.y_column[i],
                                                  width=100, text_align=ft.TextAlign.CENTER)))
            vetorLinha_Export.append(sync_experiment.time_column[i])
            vetorLinha_Export.append(sync_experiment.temperature_column[i])
            vetorLinha_Export.append(sync_experiment.flow_column[i])
            vetorLinha_Export.append(sync_experiment.y_column[i])
            vetorLinha_Export.append(sync_experiment.y_column[i])

            vetorCol.controls.insert(i, ft.Row(vetorLinha, alignment=ft.MainAxisAlignment.START))
            vetorCol_Export.append(vetorLinha_Export)

        intFoutCH4 = 0
        intFoutCO2 = 0
        for i in range(1, len(sync_experiment.time_column)):
            intFoutCH4 += (((sync_experiment.f_out_column[i] + sync_experiment.f_out_column[i - 1]) / 2) * 60 *
                           (sync_experiment.time_column[i] - sync_experiment.time_column[i - 1]))
            intFoutCO2 += (((sync_experiment.f_out_column[i] + sync_experiment.f_out_column[i - 1]) / 2) * 60 *
                           (sync_experiment.time_column[i] - sync_experiment.time_column[i - 1]))

        print("Integral FoutCH4 = " + str(intFoutCH4))
        print("Integral FoutCO2 = " + str(intFoutCO2))

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
        print("qCO2 = " + str(qco2))
        print((CinCH4 * Qin * 60 * (
                    vetorTempoy[len(vetorTempoy) - 1] - vetorTempoy[0]) - 0.20061 - CinCH4 * Vbed * epsilonL) / mads)
        #workbook = xlsxwriter.Workbook('dados_tratados.xlsx')
        #worksheet = workbook.add_worksheet()

        row = 0

        #for col, data in enumerate(vetorCol_Export):
           # worksheet.write_column(row, col, data)

        nCols = 5
        principal.width = 150 * nCols

        #workbook.close()

        principal.controls.insert(2, vetorCol)

        page.update()

    page.overlay.append(seleciona_arquivo_dialog)
    page.update()
    return principal
