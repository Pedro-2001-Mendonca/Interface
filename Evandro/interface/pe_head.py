import flet as ft
from flet_core.matplotlib_chart import MatplotlibChart
import numpy as np
from Evandro.auxiliar import load_excel_file as excel
from Evandro.db import db_experiment as db
import matplotlib.pyplot as plt
from Evandro.interface import pe_body as pb

sync_exp_list = []





def __onchange(coluna, row, page):

    if str(row.controls[0].value) == "Langmuir":
        row.controls[1].src = f"../Langmuir.jpeg"
        pb.main(coluna, page)
        page.update()
    elif str(row.controls[0].value) == "Sips":
        row.controls[1].src = f"../Sips.jpeg"
    elif str(row.controls[0].value) == "Toth":
        row.controls[1].src = f"../Toth.jpeg"
    elif str(row.controls[0].value) == "Langmuir Multissítios":
        row.controls[1].src = f"../Multissitios.jpeg"
    row.controls[1].visible = True
    coluna.update()


def main(page, off_sync):
    if off_sync:
        off_sync = False
        principal = ft.Column(scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.START, spacing=25)
        def seleciona_arquivo(e: ft.FilePickerResultEvent):
            sync_exp_list.clear()
            if e.files:
                for f in e.files:
                    db_name = f.path
                    sync_exp_list.append(db.__load_db_pack_experiment__(db_name))
                __update_page__(principal)

        seleciona_arquivo_dialog = ft.FilePicker(on_result=seleciona_arquivo)



        row = ft.Row(controls=[
            ft.Dropdown(
                width=200,
                options=[
                    ft.dropdown.Option("Langmuir"),
                    ft.dropdown.Option("Sips"),
                    ft.dropdown.Option("Toth"),
                    ft.dropdown.Option("Langmuir Multissítios"),
                ],
                on_change=lambda _: __onchange(principal, row, page),
            ),
            ft.Image(visible=False, width=150, height=70),

        ])
        principal.controls.insert(0, row)
        page.overlay.append(seleciona_arquivo_dialog)
        off_sync = True
        return principal


def __update_page__(principal):
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

    list_T = []
    list_P = []
    list_q = []
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

    ax.scatter(list_T, list_P, list_q, c=list_q, marker="o", cmap="seismic")

    ax.set_xlabel('T (K)')
    ax.set_ylabel('P (bar)')
    ax.set_zlabel('q (mol/kg)')

    grafico = MatplotlibChart(fig.figure)
    row_figure = ft.Row([grafico])
    fig_container = ft.Container(content=row_figure, width=1000, height=400, )

    principal.controls.insert(3, vetorCol)
    principal.controls.insert(4, fig_container)
    plt.close()

    principal.update()
