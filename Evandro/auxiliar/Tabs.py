import flet as ft

from Evandro.interface import interface_synchronization as i_sc

def __create_tabs__(LinhaPrincipal, page):
    if LinhaPrincipal.controls[2] is not None:
        LinhaPrincipal.controls[2].clean()
        LinhaPrincipal.controls.remove(LinhaPrincipal.controls[2])
    colunaPrincipal = ft.Column(controls=None, alignment=ft.MainAxisAlignment.START, expand=True)
    primeiraLinha = ft.Row(controls=None, alignment=ft.MainAxisAlignment.START)

    tabs = ft.Tabs(tabs=[], height=600, expand=True, tab_alignment=ft.TabAlignment.START, animation_duration=300,)

    bt_add = ft.ElevatedButton("Adicionar Experimento", on_click=lambda _: __add_tabs__(tabs, page))
    bt_remove = ft.ElevatedButton("Remover Experimento", on_click=lambda _: __remove_tabs__(tabs, 1, page))
    primeiraLinha.controls.insert(0, bt_add)
    primeiraLinha.controls.insert(1, bt_remove)

    colunaPrincipal.controls.insert(0, primeiraLinha)

    colunaPrincipal.controls.insert(1, tabs)

    LinhaPrincipal.controls.insert(2, colunaPrincipal)

    page.update()


def __add_tabs__(tabs, page,):
    index = tabs.selected_index
    column = ft.Column(controls=None, alignment=ft.MainAxisAlignment.START, expand=True)
    tab_name = "Experimento " + str(len(tabs.tabs) + 1)
    tab = ft.Tab(
        text=tab_name,
        content=ft.Container(
                    content=i_sc.main(page, tab_name), alignment=ft.alignment.top_left
                ),
    )

    tabs.tabs.append(tab)
    tabs.update()


def __remove_tabs__(tabs, index, page):
    tabs.tabs.remove(tabs.tabs[index])
    page.update()
