import flet as ft
import pandas as pd
import xlsxwriter
import numpy as np

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


def __export__(nome, sync_exp):
    if ".xlsx" in nome:
        workbook = xlsxwriter.Workbook(nome)
    else:
        workbook = xlsxwriter.Workbook(nome+'.xlsx')
    worksheet = workbook.add_worksheet()
    time_col = sync_exp.time_column.tolist()
    time_col.insert(0, "t")

    temperature_col = ["T"]
    for i in range(len(sync_exp.temperature_column)):
        temperature_col.append(sync_exp.temperature_column[i])

    flow_col = ["Q"]
    for i in range(len(sync_exp.flow_column)):
        flow_col.append(sync_exp.flow_column[i])

    y_col = ["y"]
    for i in range(len(sync_exp.y_column)):
        y_col.append(sync_exp.y_column[i])

    f_out_col = ["F"]
    for i in range(len(sync_exp.f_out_column)):
        f_out_col.append(sync_exp.f_out_column[i])

    row_export = [time_col, temperature_col, flow_col, y_col, f_out_col]
    row = 0
    for col, data in enumerate(row_export):
        worksheet.write_column(row, col, data)
    workbook.close()

