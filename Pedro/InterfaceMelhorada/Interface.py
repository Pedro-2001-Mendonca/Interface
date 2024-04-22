import colorsys

import flet as ft
import matplotlib
import pandas as pd
import PSO as pso
import numpy as np
import math
import openpyxl
import matplotlib.pyplot as plt
from flet.matplotlib_chart import MatplotlibChart
matplotlib.use("svg")

def main(page: ft.Page):
    page.scroll = 'always'
    A = [ft.Container(content=ft.TextField("oi"))]
    principal = ft.Column(alignment=ft.MainAxisAlignment.CENTER, width=page.window_width, spacing=0)
    secundaria = ft.Column(alignment=ft.MainAxisAlignment.CENTER, width=page.window_width)
    #grafico_principal = MatplotlibChart()
    vetorX = []
    vetorY = []
    vetorT = []
    vetorCol = []
    vetor_inputs = []

    grafico_principal = None
    row_inputs_volume = ft.Row()
    row_inputs_resto = ft.Row()
    row_botoes_inicial = ft.Row()

    #INPUTS
    inputL_bed = ft.TextField(label="L_bed")
    inputD_bed = ft.TextField(label="D_bed")
    inputM_ads = ft.TextField(label="M_ads")
    inputQ_in = ft.TextField(label="Q_in")
    inputT_in = ft.TextField(label="T_in")
    inputPorosidade = ft.TextField(label="Porosidade")
    inputYch4In = ft.TextField(label="Ych4In")
    inputYcho2In = ft.TextField(label="Ycho2In")
    inputPin = ft.TextField(label="P_in")

    page.add(principal, secundaria, row_inputs_volume, row_inputs_resto)


    def inserir_inputs(e):

        row_inputs_volume.clean()
        row_inputs_resto.clean()
        page.controls.remove(row_inputs_volume)
        page.controls.remove(row_inputs_resto)

        for textfield in vetor_inputs:
            textfield.value = ''

        vetor_inputs.append(inputL_bed)
        vetor_inputs.append(inputD_bed)
        vetor_inputs.append(inputM_ads)
        vetor_inputs.append(inputQ_in)
        vetor_inputs.append(inputT_in)
        vetor_inputs.append(inputPorosidade)
        vetor_inputs.append(inputYch4In)
        vetor_inputs.append(inputYcho2In)
        vetor_inputs.append(inputPin)

        for i in range(len(vetor_inputs)):
            vetor_inputs[i].width = 130
            vetor_inputs[i].text_size = 10
        #     row_inputs.controls.append(vetorInputs[i])

        for i in range(len(vetor_inputs)):
            if(i < 2):
                row_inputs_volume.controls.append(vetor_inputs[i])
            else:
                row_inputs_resto.controls.append(vetor_inputs[i])

        btnCalculaLeito = ft.ElevatedButton("Calcular Volume do Leito", on_click=calcula_volume_bed)

        row_inputs_volume.controls.append(btnCalculaLeito)

        page.add(row_inputs_volume, row_inputs_resto)
        page.update()

    def calcula_volume_bed(e):

        def close_dlg_volume(e):
            dlg_erro_volume.open = False
            page.update()

        dlg_erro_volume = ft.AlertDialog(
            modal=True,
            title=ft.Text("Erro!"),
            content=ft.Text("Por favor insira dois valores numéricos"),
            actions=[
                ft.TextButton("Ok", on_click=close_dlg_volume)
            ])

        if inputL_bed.value.isdigit() and inputD_bed.value.isdigit():
            L_bed = float(inputL_bed.value)
            D_bed = float(inputD_bed.value)

            V_bed = L_bed * D_bed
            print(V_bed)
        else:
            page.dialog = dlg_erro_volume
            dlg_erro_volume.open = True
            page.update()



    def alterar_valores(vetor):
        vetorX.clear()
        vetorY.clear()
        vetorT.clear()

        print(len(page.controls[1].controls[0].controls))
        print(page.controls[1].controls[0].controls)
        print(page.controls[1].controls)

        for i in range (0, len(page.controls[1].controls)):
            vetorT.append(page.controls[1].controls[i].controls[0].content.value)
            vetorX.append(page.controls[1].controls[i].controls[1].content.value)
            vetorY.append(page.controls[1].controls[i].controls[2].content.value)
            # print(vetorY)
            # print(vetorX)


        print(vetorT)
        print(vetorY)
        print(vetorX)

        pso.chamaPSO(vetorT, vetorX, vetorY)


        # for j in range (0, len(page.controls[1].controls[0].controls)-1):
        #     for i in range(0, len(page.controls[1].controls[0].controls)):
        # print(page.controls[1].controls[1].controls[0].content.value)
        # Vamos de fora para dentro no estilo: Column -> Row -> Container -> TextField -> Valor do TextField



    def seleciona_arquivo(e: ft.FilePickerResultEvent):
        if e.files != None:
            for f in e.files:
                arquivo = f.path
            cria_textfields(arquivo)

    def cria_textfields(arquivo):
        page.controls.remove(principal)
        page.controls.remove(secundaria)
        excel = pd.read_excel(arquivo)
        for index, row in excel.iterrows():
            vetorLinha = []
            for col, value in row.items():
                if col == 'T':
                    vetorT.append(value)
                elif col == 'X':
                    vetorX.append(value)
                elif col == 'Y':
                    vetorY.append(value)
                vetorLinha.append(
                    ft.Container(content=ft.TextField(value, width=70, text_align=ft.TextAlign.CENTER, height=30, border=ft.InputBorder.NONE))
                )
            vetorCol.append(ft.Row(vetorLinha, alignment=ft.MainAxisAlignment.CENTER))

        page.add(btnAlterar)
        page.update()

        resultado = pso.chamaPSO(vetorT, vetorX, vetorY)
        lista_Parametros = resultado[0]
        erroQ = resultado[1]
        principal.controls = vetorCol
        page.controls.insert(1, principal)
        page.update()
        xx = vetorY
        yy = [0]
        print(lista_Parametros)
        print(vetorX)
        print(vetorY)
        for i in range(1,len(xx)):
            yy.append((lista_Parametros[0]*lista_Parametros[1]*vetorX[i]*math.exp(lista_Parametros[2]*(1/vetorT[i]-1/273.15))*(1-vetorY[i]/lista_Parametros[0])**lista_Parametros[3]))

        print(yy)
        coef = np.polyfit(xx, yy, 1)
        poly1d_fn = np.poly1d(coef)
        # poly1d_fn is now a function which takes in x and returns an estimate for y
        figura, axis = plt.plot(xx, yy, 'yo', xx, poly1d_fn(xx), '--k')
        figura.set_color = 'red'

        grafico = MatplotlibChart(figura.figure)
        fig_container = ft.Container(content=grafico, width=600, height=600, alignment=ft.alignment.center,)
        secundaria.controls.insert(0, fig_container)
        secundaria.controls.insert(1, ft.Container(content=ft.TextField("Soma dos Erros Quadráticos: " + str(erroQ))))
        page.controls.insert(2, secundaria)
        print(principal.controls)
        page.update()

    seleciona_arquivo_dialog = ft.FilePicker(on_result=seleciona_arquivo)

    page.overlay.append(seleciona_arquivo_dialog)
    page.update()

    fp = ft.ElevatedButton("Inserir arquivo", on_click=seleciona_arquivo_dialog.pick_files)

    btnAlterar = ft.ElevatedButton("Alterar Valores", on_click=alterar_valores)
    btnInputs = ft.ElevatedButton(text="Inserir Inputs", on_click=inserir_inputs)

    row_botoes_inicial.controls.insert(0, fp)
    row_botoes_inicial.controls.insert(1, btnInputs)

    page.add(row_botoes_inicial)

    page.update()


ft.app(target=main)
