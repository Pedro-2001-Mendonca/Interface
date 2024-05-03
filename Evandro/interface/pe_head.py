import flet as ft
from flet_core.matplotlib_chart import MatplotlibChart
import numpy as np
from Interface.Evandro.auxiliar import load_excel_file as excel
from Interface.Evandro.db import db_experiment as db
import matplotlib.pyplot as plt
from Interface.Evandro.interface import pe_body as pb

input_height = 50
input_cursor_height = 25
input_width = 250
button_width = 200

sync_exp_list = []

list_T = []
list_P = []
list_q = []

input_n_iter = ft.TextField(label="Número de iterações", height=input_height,
                         cursor_height=input_cursor_height, width=input_width, value= "10")
input_n_particulas = ft.TextField(label="Número de partículas", height=input_height,
                         cursor_height=input_cursor_height, width=input_width, value= "100")
input_qmax_min = ft.TextField(label="Valor mínimo de qmax", height=input_height,
                         cursor_height=input_cursor_height, width=input_width)
input_qmax_max = ft.TextField(label="Valor máximo de qmax", height=input_height,
                         cursor_height=input_cursor_height, width=input_width)
input_k1_min = ft.TextField(label="Valor mínimo de K1", height=input_height,
                         cursor_height=input_cursor_height, width=input_width)
input_k1_max = ft.TextField(label="Valor máximo de K1", height=input_height,
                         cursor_height=input_cursor_height, width=input_width)
input_k2_min = ft.TextField(label="Valor mínimo de K2", height=input_height,
                         cursor_height=input_cursor_height, width=input_width)
input_k2_max = ft.TextField(label="Valor máximo de K2", height=input_height,
                         cursor_height=input_cursor_height, width=input_width)
input_alpha_min = ft.TextField(label="Valor mínimo de alpha", height=input_height,
                         cursor_height=input_cursor_height, width=input_width)
input_alpha_max = ft.TextField(label="Valor máximo de alpha", height=input_height,
                         cursor_height=input_cursor_height, width=input_width)
input_n_min = ft.TextField(label="Valor mínimo de n", height=input_height,
                         cursor_height=input_cursor_height, width=input_width)
input_n_max = ft.TextField(label="Valor máximo de n", height=input_height,
                         cursor_height=input_cursor_height, width=input_width)
input_ns_min = ft.TextField(label="Valor mínimo de ns", height=input_height,
                         cursor_height=input_cursor_height, width=input_width)
input_ns_max = ft.TextField(label="Valor máximo de ns", height=input_height,
                         cursor_height=input_cursor_height, width=input_width)

def cria_linha(index):
    linha1 = ft.Row(controls=[
        input_n_iter,
        input_n_particulas
    ])
    linha2 = ft.Row(controls=[
        input_qmax_min,
        input_qmax_max,
    ])
    linha3 = ft.Row(controls=[
        input_k1_min,
        input_k1_max,
    ])
    linha4 = ft.Row(controls=[
        input_k2_min,
        input_k2_max,
    ])
    coluna1 = ft.Column(controls=[
        linha1,
        ft.Divider(),
        linha2,
        linha3,
        linha4
    ])

    if index == 0:
        pass
    elif index == 1:
        coluna1.controls.append(
            ft.Row(controls=[
                input_ns_min,
                input_ns_max
            ])
        )
    elif index == 2:
        coluna1.controls.append(
            ft.Row(controls=[
                input_n_min,
                input_n_max
            ])
        )
    elif index == 3:
        coluna1.controls.append(
            ft.Row(controls=[
                input_alpha_min,
                input_alpha_max
            ])
        )

    return coluna1





def __onchange(coluna, row, page):

    if str(row.controls[0].value) == "Langmuir":
        row.controls[1].src = f"../Langmuir.jpeg"
        coluna.controls.insert(1, cria_linha(0))
        pb.main(coluna, page, list_T, list_P, list_q, 0, int(input_n_particulas.value), int(input_n_iter.value))
        page.update()
    elif str(row.controls[0].value) == "Sips":
        row.controls[1].src = f"../Sips.jpeg"
        coluna.controls.insert(1, cria_linha(1))
        pb.main(coluna, page, list_T, list_P, list_q, 0, int(input_n_particulas.value), int(input_n_iter.value))
        page.update()
    elif str(row.controls[0].value) == "Toth":
        row.controls[1].src = f"../Toth.jpeg"
        coluna.controls.insert(1, cria_linha(2))
        pb.main(coluna, page, list_T, list_P, list_q, 0, int(input_n_particulas.value), int(input_n_iter.value))
        page.update()
    elif str(row.controls[0].value) == "Langmuir Multissítios":
        row.controls[1].src = f"../Multissitios.jpeg"
        coluna.controls.insert(1, cria_linha(3))
        pb.main(coluna, page, list_T, list_P, list_q, 0, int(input_n_particulas.value), int(input_n_iter.value))
        page.update()
    row.controls[1].visible = True
    coluna.update()


def main(page, off_sync):
    if off_sync:
        off_sync = False
        principal = ft.Column(scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.START, spacing=25)

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
        off_sync = True
        return principal

