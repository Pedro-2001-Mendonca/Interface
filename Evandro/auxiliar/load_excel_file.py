import flet as ft
import pandas as pd

def __seleciona_arquivo__(e: ft.FilePickerResultEvent):
    if e.files is not None:
        for f in e.files:
            arquivo = f.path
    excel = pd.read_excel(arquivo)

    vetorTempoT = []
    vetorT = []
    vetorTempoQ = []
    vetorQ =[]
    vetorTempoy = []
    vetory = []

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

def __load_nSync__(linha_principal):
    return 0
