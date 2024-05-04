import flet as ft
import pandas as pd
from flet_core.matplotlib_chart import MatplotlibChart

import numpy as np
from Evandro.auxiliar import load_excel_file as excel
from Evandro.db import db_experiment as db
import matplotlib.pyplot as plt
from Evandro.auxiliar import PSO2 as pso
from Evandro.interface import resultado as res
sync_exp_list = []




def __get_resultados__(page, coluna_principal, list_T, list_P, list_q, Tref,
                       model, pop_size,
                       max_iter, parameters, prog_column):

    parametros, erroQ = pso.chama_pso(coluna_principal, list_T, list_P, list_q, Tref,
                  model, pop_size,
                  max_iter, parameters, prog_column)

    dlg = ft.AlertDialog(
        title=ft.Text("")
    )
    def open_dlg():
        page.dialog = dlg
        dlg.open = True
        page.update()

    def open_dlg_modal():
        page.dialog = dlg_modal
        dlg_modal.open = True
        page.update()

    def close_dlg(e):
        dlg_modal.open = False
        page.update()

    conteudo_resultados = ft.Column(controls=[])

    conteudo_resultados.controls.append(ft.Text("Erro Quadrático = " + str(erroQ)))

    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Resultados da Estimação"),
        content=res.main(page, coluna_principal, list_T, list_P, list_q, Tref,
                       model, pop_size,
                       max_iter, parameters, prog_column, [parametros, erroQ]),
        actions=[
            ft.TextButton("Salvar", on_click=close_dlg),
            ft.TextButton("Cancelar", on_click=close_dlg),
        ],
        actions_alignment=ft.MainAxisAlignment.END,

    )

    open_dlg_modal()



def main(coluna_principal, page, list_T, list_P, list_q, model, pop_size, max_iter, parameters):
    principal = ft.Column(alignment=ft.MainAxisAlignment.START, scroll=ft.ScrollMode.ALWAYS, spacing=25)

    def seleciona_arquivo1(e: ft.FilePickerResultEvent):
        sync_exp_list.clear()
        if e.files:
            for f in e.files:
                db_name = f.path
                sync_exp_list.append(db.__load_db_pack_experiment__(db_name))
            __update_page__(principal, list_T, list_P, list_q)

    seleciona_arquivo_dialog1 = ft.FilePicker(on_result=seleciona_arquivo1)
    btn_exp = ft.ElevatedButton("Carregar Experimentos", on_click=lambda _: seleciona_arquivo_dialog1.pick_files(
        allowed_extensions=["exp"], allow_multiple=True), width=200)

    def seleciona_arquivo2(e: ft.FilePickerResultEvent):
        sync_exp_list.clear()
        if e.files:
            for f in e.files:
                arquivo = f.path
                __load_excel(arquivo, list_T, list_P, list_q)
            __update_page__2(principal, list_T, list_P, list_q)

    seleciona_arquivo_dialog2 = ft.FilePicker(on_result=seleciona_arquivo2)

    btn_exc = ft.ElevatedButton("Carregar Planilha", on_click=lambda _: seleciona_arquivo_dialog2.pick_files(
        allowed_extensions=["xlsx"], allow_multiple=True), width=200)

    while len(coluna_principal.controls) > 2:
        coluna_principal.controls.remove(coluna_principal.controls[2])


    btn_pso = ft.ElevatedButton("Estimar parâmetros", width=200,
                                on_click=lambda _: __get_resultados__(page, coluna_principal, list_T, list_P, list_q, 273.15,
                                                                      model, int(pop_size.value),
                                                                      int(max_iter.value), parameters, prog_column))
    prog_label = ft.Text("Teste", visible=True, size=10)
    prog_bar = ft.ProgressBar(visible=True, width=200, value=0, height=10, border_radius=ft.border_radius.all(30))
    prog_column = ft.Column(controls=[prog_label, prog_bar], spacing=5, visible=False)
    linha_botoes = ft.Row(controls=[
        btn_exp,
        btn_exc,
        btn_pso,
        prog_column
    ], spacing=20)



    principal.controls.insert(0, linha_botoes)
    coluna_principal.controls.insert(2, principal)
    page.overlay.append(seleciona_arquivo_dialog1)
    page.overlay.append(seleciona_arquivo_dialog2)

    coluna_principal.update()


def __update_page__(principal, list_T, list_P, list_q):
    list_T.clear()
    list_P.clear()
    list_q.clear()
    while len(principal.controls) > 1:
        principal.controls.remove(principal.controls[1])

    new_list = sorted(sync_exp_list, key=lambda x: x[0])

    vetorCol = ft.Column(controls=None)
    vetorCol.controls.clear()
    newheigth = 35
    vetorLinha = [ft.TextField("Temperatura (K)", text_align=ft.TextAlign.CENTER, width=150,
                               height=newheigth,
                               text_vertical_align=-1,
                               content_padding=ft.padding.only(left=5, right=2, bottom=18),
                               border=ft.InputBorder.NONE, read_only=True),
                  ft.TextField("Pressão (bar)", text_align=ft.TextAlign.CENTER, width=150,
                               height=newheigth,
                               text_vertical_align=-1, content_padding=ft.padding.only(left=5, right=2, bottom=18),
                               border=ft.InputBorder.NONE, read_only=True),
                  ft.TextField("q (mol/kg)", text_align=ft.TextAlign.CENTER, width=150,
                               height=newheigth,
                               text_vertical_align=-1, content_padding=ft.padding.only(left=5, right=2, bottom=18),
                               border=ft.InputBorder.NONE, read_only=True)]

    vetorCol.controls.insert(0, ft.Row(vetorLinha, alignment=ft.MainAxisAlignment.START))

    for i in range(len(new_list)):
        vetorLinha = [
            ft.TextField(round(new_list[i][0], 5), text_align=ft.TextAlign.CENTER, width=150,
                         height=newheigth,
                         text_vertical_align=-0.73, content_padding=ft.padding.only(left=5, right=2)),
            ft.TextField(round(new_list[i][1], 5), text_align=ft.TextAlign.CENTER,
                         width=150,
                         height=newheigth,
                         text_vertical_align=-0.73, content_padding=ft.padding.only(left=5, right=2)),
            ft.TextField(round(new_list[i][2], 5), text_align=ft.TextAlign.CENTER, width=150,
                         height=newheigth,
                         text_vertical_align=-0.73, content_padding=ft.padding.only(left=5, right=2))]
        list_T.insert(i, new_list[i][0])
        list_P.insert(i, new_list[i][1])
        list_q.insert(i, new_list[i][2])

        vetorCol.controls.insert(i + 1, ft.Row(vetorLinha, alignment=ft.MainAxisAlignment.START))

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    ax.view_init(elev=25, azim=215, roll=0)
    ax.grid(False)
    ax.set_xlabel('Temperatura (K)')
    ax.set_ylabel('Pressão (bar)')
    ax.set_zlabel('q (mol/kg)')
    ax.scatter(list_T, list_P, list_q, c=list_q, marker="o", cmap="rainbow")
    grafico = MatplotlibChart(fig.figure)
    row_figure = ft.Row([grafico])
    fig_container = ft.Container(content=row_figure, width=1000, height=400, )

    principal.controls.insert(3, vetorCol)
    principal.controls.insert(4, fig_container)
    plt.close()


    principal.update()


def __load_excel(arquivo, list_T, list_P, list_q):
    list_T.clear()
    list_P.clear()
    list_q.clear()
    excelFile = pd.read_excel(arquivo)
    i = 0
    for index, row in excelFile.iterrows():

        for col, value in row.items():
            if col == 'T' and value >= 0:
                list_T.append(value)
            elif col == 'P' and value >= 0:
                list_P.append(value)
            elif col == 'q' and value >= 0:
                list_q.append(value)
        sync_exp_list.append([list_T[i], list_P[i], list_q[i]])
        i += 1


def __update_page__2(principal, list_T, list_P, list_q):

    while len(principal.controls) > 1:
        principal.controls.remove(principal.controls[1])
    new_list = sorted(sync_exp_list, key=lambda x: x[0])
    vetorCol = ft.Column(controls=None)
    vetorCol.controls.clear()
    newheigth = 35
    vetorLinha = [ft.TextField("Temperatura (K)", text_align=ft.TextAlign.CENTER, width=150,
                               height=newheigth,
                               text_vertical_align=-1,
                               content_padding=ft.padding.only(left=5, right=2, bottom=18),
                               border=ft.InputBorder.NONE, read_only=True),
                  ft.TextField("Pressão (bar)", text_align=ft.TextAlign.CENTER, width=150,
                               height=newheigth,
                               text_vertical_align=-1, content_padding=ft.padding.only(left=5, right=2, bottom=18),
                               border=ft.InputBorder.NONE, read_only=True),
                  ft.TextField("q (mol/kg)", text_align=ft.TextAlign.CENTER, width=150,
                               height=newheigth,
                               text_vertical_align=-1, content_padding=ft.padding.only(left=5, right=2, bottom=18),
                               border=ft.InputBorder.NONE, read_only=True)]

    vetorCol.controls.insert(0, ft.Row(vetorLinha, alignment=ft.MainAxisAlignment.START))

    for i in range(len(new_list)):
        vetorLinha = [
            ft.TextField(round(new_list[i][0], 5), text_align=ft.TextAlign.CENTER, width=150,
                         height=newheigth,
                         text_vertical_align=-0.73, content_padding=ft.padding.only(left=5, right=2)),
            ft.TextField(round(new_list[i][1], 5), text_align=ft.TextAlign.CENTER,
                         width=150,
                         height=newheigth,
                         text_vertical_align=-0.73, content_padding=ft.padding.only(left=5, right=2)),
            ft.TextField(round(new_list[i][2], 5), text_align=ft.TextAlign.CENTER, width=150,
                         height=newheigth,
                         text_vertical_align=-0.73, content_padding=ft.padding.only(left=5, right=2))]

        vetorCol.controls.insert(i + 1, ft.Row(vetorLinha, alignment=ft.MainAxisAlignment.START))

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    ax.view_init(elev=25, azim=215, roll=0)
    ax.grid(False)
    ax.set_xlabel('Temperatura (K)')
    ax.set_ylabel('Pressão (bar)')
    ax.set_zlabel('q (mol/kg)')
    ax.scatter(list_T, list_P, list_q, c=list_q, marker="o", cmap="rainbow")
    grafico = MatplotlibChart(fig.figure)
    row_figure = ft.Row([grafico])
    fig_container = ft.Container(content=row_figure, width=1000, height=400, )

    principal.controls.insert(3, vetorCol)
    principal.controls.insert(4, fig_container)
    plt.close()

    principal.update()
