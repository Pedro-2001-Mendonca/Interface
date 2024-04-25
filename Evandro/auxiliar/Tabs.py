import flet as ft

from Evandro.interface import interface_synchronization2 as i_sc
from Evandro.classes import experiment_class as ec

experiment_list = []

def __create_tabs__(LinhaPrincipal, page):
    if LinhaPrincipal.controls[2] is not None:
        LinhaPrincipal.controls[2].clean()
        LinhaPrincipal.controls.remove(LinhaPrincipal.controls[2])
    colunaPrincipal = ft.Column(controls=None, alignment=ft.MainAxisAlignment.START, expand=True)
    primeiraLinha = ft.Row(controls=None, alignment=ft.MainAxisAlignment.START)

    tabs = ft.Tabs(tabs=[], height=600, expand=True, tab_alignment=ft.TabAlignment.START, animation_duration=300,)

    bt_add = ft.ElevatedButton("Adicionar Experimento", on_click=lambda _: __add_tabs__(tabs, page))
    bt_remove = ft.ElevatedButton("Remover Experimento", on_click=lambda _: __remove_tabs__(tabs))
    bt_compile = ft.ElevatedButton("Compilar Experimentos", on_click=lambda _: __compile_exp__())
    primeiraLinha.controls.insert(0, bt_add)
    primeiraLinha.controls.insert(1, bt_remove)
    primeiraLinha.controls.insert(2, bt_compile)

    colunaPrincipal.controls.insert(0, primeiraLinha)

    colunaPrincipal.controls.insert(1, tabs)

    LinhaPrincipal.controls.insert(2, colunaPrincipal)

    page.update()


def __add_tabs__(tabs, page,):

    column = ft.Column(controls=None, alignment=ft.MainAxisAlignment.START, expand=True)
    tab_name = "Experimento " + str(len(tabs.tabs) + 1)
    new_exp_class = __create_sync_exp__
    experiment_list.append(new_exp_class)
    tab = ft.Tab(
        text=tab_name,
        content=ft.Container(
                    content=i_sc.main(page, tab_name, experiment_list[len(tabs.tabs) -1]), alignment=ft.alignment.top_left
                ),
    )

    tabs.tabs.append(tab)
    tabs.update()


def __remove_tabs__(tabs):
    if len(tabs.tabs) > 0:
        tabs.tabs.remove(tabs.tabs[tabs.selected_index])
        for i in range(len(tabs.tabs)):
            tabs.tabs[i].text = "Experimento "+str(i+1)
        tabs.update()
        tabs.selected_index = 0


def __compile_exp__():
    print(experiment_list[0].inlet_pressure)
    print(experiment_list[1].inlet_pressure)


def __create_sync_exp__():

    return ec.SynchronizedExperiment(
    experiment_name="",
    inlet_pressure=0,
    inlet_flow=0,
    inlet_temperature=0,
    inlet_y=0,
    adsorbent_mass=0,
    bed_length=0,
    bed_diameter=0,
    time_column=[],
    temperature_column=[],
    flow_column=[],
    y_column=[],
    temperature_unit="K",
    pressure_unit="bar",
    flow_unit="L/min",
    poly_flow=[],
    poly_temperature=[],
    poly_y=[],
    f_out_column=[],
    c_out_column=[],
    porosity=0)