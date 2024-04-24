
import xlsxwriter
import flet as ft
import pandas as pd
import math
import numpy as np
from flet_core.matplotlib_chart import MatplotlibChart

from Evandro.classes import experiment_class as ec
from Evandro.auxiliar import synchronization as sync
from Evandro.db import db_experiment as db
import matplotlib.pyplot as plt

def main(page, tab_name):

    principal = ft.Column(alignment=ft.MainAxisAlignment.START, scroll=ft.ScrollMode.ALWAYS,  spacing=25)

    input_height = 50
    input_cursor_height = 25
    input_width = 250

    #inputs do leito
    inputL_bed = ft.TextField(label="Comprimento", suffix_text="(m)", height=input_height,
                              cursor_height=input_cursor_height, width=input_width)
    inputD_bed = ft.TextField(label="Diâmetro", suffix_text="(m)", height=input_height, cursor_height=input_cursor_height, width=input_width)
    label_row = ft.Row(controls=[ft.Text("Propriedades do Leito")],  spacing=25)
    row_input_leito = ft.Row(controls=[inputL_bed, inputD_bed], spacing=25)
    container_espaco = ft.Container(content=None, height=10)
    column_input_leito = ft.Column(controls=[container_espaco, label_row, row_input_leito],  spacing=5)
    container_leito = ft.Container(content=column_input_leito)
    #inputL_bed.value = "0.1921"
    #inputD_bed.value = "0.0211"




    #inputs adsorvente
    inputM_ads = ft.TextField(label="Massa", suffix_text="(kg)", height=input_height, cursor_height=input_cursor_height, width=input_width)
    inputPorosidade = ft.TextField(label="Porosidade", height=input_height, cursor_height=input_cursor_height, width=input_width)
    label_row_ads = ft.Row(controls=[ft.Text("Propriedades do Adsorvente")], spacing=25)
    row_input_ads = ft.Row(controls=[inputM_ads, inputPorosidade], spacing=25)
    column_input_ads = ft.Column(controls=[label_row_ads, row_input_ads], spacing=5)
    container_ads = ft.Container(content=column_input_ads)
    #inputM_ads.value = "0.0383"
    #inputPorosidade.value = "0.5671"

    #inputs_entrada
    inputP_in = ft.TextField(label="Pressão", suffix_text="(bar)", height=input_height, cursor_height=input_cursor_height, width=input_width)
    inputT_in = ft.TextField(label="Temperatura", suffix_text="(K)", height=input_height, cursor_height=input_cursor_height, width=input_width)
    inputQ_in = ft.TextField(label="Vazão", suffix_text="(L/min)", height=input_height, cursor_height=input_cursor_height, width=input_width)
    inputy_in = ft.TextField(label="Fração molar", height=input_height, cursor_height=input_cursor_height, width=input_width)
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
    input_sync_t = ft.TextField(label="Tempo Final",  height=input_height,
                             cursor_height=input_cursor_height, width=input_width)
    input_sync_int = ft.TextField(label="Número de Intervalos",  height=input_height,
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
    sync_bt = ft.ElevatedButton("Sincronizar")
    linha1 = ft.Row(alignment=ft.MainAxisAlignment.START,)
    linha1.controls.insert(0, fp)
    linha1.controls.insert(1, sync_bt)
    principal.controls.insert(1, linha1)
    principal.controls.insert(2, ft.Column(controls=None))

    vetorQ = []
    vetorTempoQ = []
    vetorT = []
    vetorTempoT = []
    vetory = []
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
            5,
            float(__return_input_value__(inputPorosidade.value))
        )


        vetorCol = ft.Column(controls=None)
        vetorCol.controls.clear()
        vetorLinha = []
        newheigth = 35
        titulo_size = 15
        vertical_up = -0.9
        vetorLinha.append(ft.TextField("Tempo - Temp. (s)", text_align=ft.TextAlign.CENTER, text_size=titulo_size,
                                       width=150,
                                       height=newheigth,
                                       text_vertical_align=vertical_up,
                                       content_padding=ft.padding.only(left=5, right=2, bottom=18),
                                       border=ft.InputBorder.NONE, read_only=True))
        vetorLinha.append(ft.TextField("Temperatura (K)", text_align=ft.TextAlign.CENTER, width=150,text_size=titulo_size,
                                       height=newheigth,
                                       text_vertical_align=vertical_up, content_padding=ft.padding.only(left=5, right=2, bottom=18),
                                       border=ft.InputBorder.NONE, read_only=True))
        vetorLinha.append(ft.TextField("Tempo - Vazão (s)", text_align=ft.TextAlign.CENTER, width=150,text_size=titulo_size,
                                       height=newheigth,
                                       text_vertical_align=vertical_up,
                                       content_padding=ft.padding.only(left=5, right=2, bottom=18),
                                       border=ft.InputBorder.NONE, read_only=True))
        vetorLinha.append(ft.TextField("Vazão (L/min)", text_align=ft.TextAlign.CENTER, width=150,text_size=titulo_size,
                                       height=newheigth,
                                       text_vertical_align=vertical_up, content_padding=ft.padding.only(left=5, right=2, bottom=18),
                                       border=ft.InputBorder.NONE, read_only=True))
        vetorLinha.append(ft.TextField("Tempo - F. Mol. (s)", text_align=ft.TextAlign.CENTER, width=150,text_size=titulo_size,
                                       height=newheigth,
                                       text_vertical_align=vertical_up,
                                       content_padding=ft.padding.only(left=5, right=2, bottom=18),
                                       border=ft.InputBorder.NONE, read_only=True))
        vetorLinha.append(ft.TextField("Fração Molar", text_align=ft.TextAlign.CENTER, width=150,text_size=titulo_size,
                                       height=newheigth,
                                       text_vertical_align=-1, content_padding=ft.padding.only(left=5, right=2, bottom=18),
                                       border=ft.InputBorder.NONE, read_only=True))
        vetorCol.controls.insert(0, ft.Row(vetorLinha, alignment=ft.MainAxisAlignment.START))
        #vetorCol_Export = []

        for i in range(np.max([len(vetorTempoT), len(vetorTempoQ), len(vetorTempoy)])):
            vetorLinha = []
            #vetorLinha_Export = []

            if i < len(vetorTempoT):
                vetorLinha.append(ft.TextField(round(vetorTempoT[i], 5), text_align=ft.TextAlign.CENTER,
                            width=150,
                             height=newheigth,
                             text_vertical_align=-0.73, content_padding=ft.padding.only(left=5, right=2)))
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
                             text_vertical_align=-0.73, content_padding=ft.padding.only(left=5, right=2)))
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
                             text_vertical_align=-0.73, content_padding=ft.padding.only(left=5, right=2)))
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
            #vetorLinha_Export.append(sync_experiment.time_column[i])
            #vetorLinha_Export.append(sync_experiment.temperature_column[i])
            #vetorLinha_Export.append(sync_experiment.flow_column[i])
            #vetorLinha_Export.append(sync_experiment.y_column[i])

            vetorCol.controls.insert(i+1, ft.Row(vetorLinha, alignment=ft.MainAxisAlignment.START))

        def __salvar__():
            db.__create_db_ns_experiment__(tab_name, not_synchronized_experiment)

        salvar = ft.ElevatedButton("Salvar", on_click=lambda _: __salvar__())
        if len(principal.controls) > 2:
            principal.controls.remove(vetorCol)

        principal.controls.insert(2, vetorCol)

        principal.update()

    page.overlay.append(seleciona_arquivo_dialog)
    page.update()
    return principal

def __return_input_value__(input):
    if input != '':
        return input
    else:
        return 0
