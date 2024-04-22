import flet as ft
import matplotlib
import pandas as pd
import math
matplotlib.use("svg")
import Interpolation as itp
import xlsxwriter


def main(page: ft.Page):
    page.scroll = 'always'

    principal = ft.Column(alignment=ft.MainAxisAlignment.CENTER, width=page.window_width)
    inputs_col = ft.Column(alignment=ft.MainAxisAlignment.CENTER, width=page.window_width)




    vetorQ = []
    vetorTempoQ = []

    vetorT = []
    vetorTempoT = []

    vetoryCO2 = []
    vetoryCH4 = []
    vetorTempoy = []



    page.add(principal)


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

            row = 0

            for col, data in enumerate(vetorCol_Export):
                worksheet.write_column(row, col, data)





            workbook.close()

            principal.controls = vetorCol
            page.controls.insert(1, principal)
            page.update()


    seleciona_arquivo_dialog = ft.FilePicker(on_result=seleciona_arquivo)

    page.overlay.append(seleciona_arquivo_dialog)
    page.update()

    fp = ft.ElevatedButton("Inserir arquivo", on_click=seleciona_arquivo_dialog.pick_files)

    page.add(fp)



ft.app(target=main)