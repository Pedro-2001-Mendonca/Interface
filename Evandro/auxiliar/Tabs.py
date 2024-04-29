import flet as ft

from Interface.Evandro.interface import interface_synchronization2 as i_sc
from Interface.Evandro.classes import experiment_class as ec

experiment_list = []


def __create_tabs__(LinhaPrincipal, page):
    if LinhaPrincipal.controls[2] is not None:
        LinhaPrincipal.controls[2].clean()
        LinhaPrincipal.controls.remove(LinhaPrincipal.controls[2])
    colunaPrincipal = ft.Column(controls=None, alignment=ft.MainAxisAlignment.START, expand=True)
    primeiraLinha = ft.Row(controls=None, alignment=ft.MainAxisAlignment.START)

    tabs = ft.Tabs(tabs=[], height=600, expand=True, tab_alignment=ft.TabAlignment.START, animation_duration=300,)

    #bt_add = ft.ElevatedButton("Adicionar Experimento", on_click=lambda _: __add_tabs__(tabs, page))
    #bt_remove = ft.ElevatedButton("Remover Experimento", on_click=lambda _: __remove_tabs__(tabs))
    #bt_compile = ft.ElevatedButton("Compilar Experimentos", on_click=lambda _: __compile_exp__())
    #primeiraLinha.controls.insert(0, bt_add)
    #primeiraLinha.controls.insert(1, bt_remove)
    #primeiraLinha.controls.insert(2, bt_compile)

    #colunaPrincipal.controls.insert(0, primeiraLinha)

    colunaPrincipal.controls.insert(0, tabs)

    LinhaPrincipal.controls.insert(2, colunaPrincipal)
    __add_tabs__(tabs, page)
    page.update()


def __add_tabs__(tabs, page,):

    column = ft.Column(controls=None, alignment=ft.MainAxisAlignment.START, expand=True)
    tab_name = "Experimento" #+ str(len(tabs.tabs) + 1)
    coluna = i_sc.main(page, tab_name)

    tab = ft.Tab(
        text=tab_name,
        content=ft.ResponsiveRow([ft.Container(content=coluna)]))

    tabs.tabs.append(tab)
    tabs.update()


def __remove_tabs__(tabs):
    if len(tabs.tabs) > 0:
        tabs.tabs.remove(tabs.tabs[tabs.selected_index])
        for i in range(len(tabs.tabs)):
            tabs.tabs[i].text = "Experimento "+str(i+1)
        tabs.update()
        tabs.selected_index = 0



