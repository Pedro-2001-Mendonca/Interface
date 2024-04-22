import flet as ft
import matplotlib
import pandas as pd
import math
import matplotlib.pyplot as plt
from flet.matplotlib_chart import MatplotlibChart
matplotlib.use("svg")
import Interpolation as itp
import xlsxwriter


def main(page: ft.Page):
    page.scroll = 'always'

    principal = ft.Column(alignment=ft.MainAxisAlignment.CENTER, width=page.window_width)

    vetorQ = []
    vetorTempoQ = []

    vetorT = []
    vetorTempoT = []

    vetoryCO2 = []
    vetoryCH4 = []
    vetorTempoy = []

    # INPUTS
    vetor_inputs = []
    inputL_bed = ft.TextField(label="L_bed")
    inputD_bed = ft.TextField(label="D_bed")
    inputM_ads = ft.TextField(label="M_ads")
    inputQ_in = ft.TextField(label="Q_in")
    inputT_in = ft.TextField(label="T_in")
    inputPorosidade = ft.TextField(label="Porosidade")
    inputYch4In = ft.TextField(label="Ych4In")
    inputYcho2In = ft.TextField(label="Ycho2In")
    inputPin = ft.TextField(label="P_in")

    row_inputs_volume = ft.Row()
    row_inputs_resto = ft.Row()



    page.add(principal, row_inputs_volume, row_inputs_resto)

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


    def seleciona_arquivo(e: ft.FilePickerResultEvent):
        if e.files != None:
            for f in e.files:
                arquivo = f.path
            cria_textfields(arquivo)

    def cria_textfields(arquivo):
        page.controls.remove(principal)
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

        polinomiosT = itp.interpolation(vetorTempoT, vetorT)

        polinomiosQ = itp.interpolation(vetorTempoQ, vetorQ)

        vetornewT = []
        vetornewQ = []
        vetorQLs = []
        vetorConcCH4 = []
        vetorConcCO2 = []
        vetorFoutCH4 = []
        vetorFoutCO2 = []

        for i in range(len(vetorTempoy)):
            vetornewT.append(polinomiosT[itp.get_position(vetorTempoy[i], vetorTempoT)](vetorTempoy[i]))

        for i in range(len(vetorTempoy)):
            vetornewQ.append(polinomiosQ[itp.get_position(vetorTempoy[i], vetorTempoQ)](vetorTempoy[i]))
            vetorQLs.append(vetornewQ[i]/(60*1000))
            vetorConcCH4.append(vetoryCH4[i]*0.9869/((vetornewT[i]+273.15)*0.082057)) #Pressão = 0.98, Constante dos gases ideais =0.082057
            vetorConcCO2.append(vetoryCO2[i] * 0.9869 / (
                        (vetornewT[i]+273.15) * 0.082057459))  # Pressão = 0.98, Constante dos gases ideais =0.082057
            vetorFoutCH4.append(vetorConcCH4[i]*vetorQLs[i])
            vetorFoutCO2.append(vetorConcCO2[i] * vetorQLs[i])

        vetorCol = []
        vetorCol_Export = []
        for i in range(len(vetorTempoy)):
            vetorLinha = []
            vetorLinha_Export = []
            vetorLinha.append(
                ft.Container(content=ft.TextField(vetorTempoy[i], width=100, text_align=ft.TextAlign.CENTER)))
            vetorLinha.append(
                ft.Container(content=ft.TextField(vetornewT[i], width=100, text_align=ft.TextAlign.CENTER)))
            vetorLinha.append(ft.Container(content=ft.TextField(vetornewQ[i], width=100, text_align=ft.TextAlign.CENTER)))
            vetorLinha.append(ft.Container(content=ft.TextField(vetoryCH4[i], width=100, text_align=ft.TextAlign.CENTER)))
            vetorLinha.append(ft.Container(content=ft.TextField(vetoryCO2[i], width=100, text_align=ft.TextAlign.CENTER)))
            vetorLinha_Export.append(vetorTempoy[i])
            vetorLinha_Export.append(vetornewT[i])
            vetorLinha_Export.append(vetornewQ[i])
            vetorLinha_Export.append(vetoryCH4[i])
            vetorLinha_Export.append(vetoryCO2[i])

            vetorCol.append(ft.Row(vetorLinha, alignment=ft.MainAxisAlignment.CENTER))
            vetorCol_Export.append(vetorLinha_Export)

        intFoutCH4 = 0
        intFoutCO2 = 0
        for i in range(1, len(vetorTempoy)):
            intFoutCH4 += ((vetorFoutCH4[i] + vetorFoutCH4[i - 1]) / 2)*60*(vetorTempoy[i] - vetorTempoy[i-1])
            intFoutCO2 += ((vetorFoutCO2[i] + vetorFoutCO2[i - 1]) / 2)*60*(vetorTempoy[i] - vetorTempoy[i-1])

        print("Integral FoutCH4 = "+ str(intFoutCH4))
        print("Integral FoutCO2 = "+ str(intFoutCO2))
        Gascte = 0.08314462
        Lbed = 0.1921
        dbed = 0.0211
        Vbed = 1000*(dbed**2)*Lbed*0.25*math.pi
        epsilonL = 0.5671
        mads = 0.0383
        Qin = 0.5/(60) #L/s
        Tin = 298.15
        CinCH4 = 1 * 0.6/(Gascte*Tin) #mol/L
        CinCO2 = 1 * 0.4 / (Gascte * Tin)  # mol/L
        qch4 = (CinCH4 * Qin * 60 * (vetorTempoy[len(vetorTempoy)-1]-vetorTempoy[0])-intFoutCH4-CinCH4*Vbed*epsilonL) / mads
        qco2 = (CinCO2 * Qin * 60 * (
                    vetorTempoy[len(vetorTempoy) - 1] - vetorTempoy[0]) - intFoutCO2 - CinCO2 * Vbed * epsilonL) / mads
        print("qCH4 = " + str(qch4))
        print("qCO2 = " + str(qco2))
        print((CinCH4*Qin*60*(vetorTempoy[len(vetorTempoy)-1]-vetorTempoy[0])-0.20061-CinCH4*Vbed*epsilonL)/mads)
        workbook = xlsxwriter.Workbook('dados_tratados.xlsx')
        worksheet = workbook.add_worksheet()

        figura = plt.plot(vetorTempoy, vetornewT, 'k-o')
        figura2 = plt.plot(vetorTempoy, vetornewQ, 'r-o')
        figura3 = plt.plot(vetorTempoy, vetoryCH4, 'g-o')
        figura4 = plt.plot(vetorTempoy, vetoryCO2, 'b-o')

        grafico = MatplotlibChart(figura[0].figure)
        grafico2 = MatplotlibChart(figura2[0].figure)
        grafico3 = MatplotlibChart(figura3[0].figure)
        grafico4 = MatplotlibChart(figura4[0].figure)


        fig_container = ft.Container(content=grafico, width=600, height=600, alignment=ft.alignment.center)
        fig_container2 = ft.Container(content=grafico2, width=600, height=600)
        fig_container3 = ft.Container(content=grafico3, width=600, height=600)
        fig_container4 = ft.Container(content=grafico4, width=600, height=600)


        row = 0

        for col, data in enumerate(vetorCol_Export):
            worksheet.write_column(row, col, data)

        workbook.close()

        principal.controls = vetorCol
        page.controls.insert(len(page.controls)+1, principal)
        principal.controls.extend([fig_container, fig_container2, fig_container3, fig_container4])
        page.update()


    seleciona_arquivo_dialog = ft.FilePicker(on_result=seleciona_arquivo)

    page.overlay.append(seleciona_arquivo_dialog)
    page.update()

    fp = ft.ElevatedButton("Inserir arquivo", on_click=seleciona_arquivo_dialog.pick_files)
    btnInputs = ft.ElevatedButton(text="Inserir Inputs", on_click=inserir_inputs)

    page.add(fp, btnInputs)


ft.app(target=main)