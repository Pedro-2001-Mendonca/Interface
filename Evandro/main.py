from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import flet as ft
from Evandro.auxiliar import Tabs as tbs
from interface import visulize_experiment as pe
from interface import compile_exp as cp
import matplotlib
import operator
import sqlite3
import numpy as np
import pandas as pd
import xlsxwriter
from flet_core.matplotlib_chart import MatplotlibChart
import math
matplotlib.use("svg")


Base = declarative_base()


def __change_page__(index, LinhaPrincipal, page):
    if index == 0:
        tbs.__create_tabs__(LinhaPrincipal, page)
    if index == 1:
        pe.main(LinhaPrincipal, page)
    if index == 2:
        cp.main(LinhaPrincipal, page)


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    LinhaPrincipal = ft.Row(controls=None, vertical_alignment=ft.CrossAxisAlignment.START)
    page.add(LinhaPrincipal)

    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=400,
        # leading=ft.FloatingActionButton(icon=ft.icons.CREATE, text="Add"),
        # extended=True,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.TIMER_OFF, selected_icon=ft.icons.TIMER, label="Sincronização",
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.BOOKMARK_BORDER),
                selected_icon_content=ft.Icon(ft.icons.BOOKMARK),
                label="Parâmetros",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.PROPANE_TANK_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.PROPANE_TANK),
                label_content=ft.Text("Simulação"),
            ),
        ],
        on_change=lambda e: __change_page__(e.control.selected_index, LinhaPrincipal, page),
    )

    LinhaPrincipal = ft.Row([
        rail,
        ft.VerticalDivider(width=1),
        ft.Column(controls=None, alignment=ft.MainAxisAlignment.START)
    ],
        expand=True, spacing=20
    )

    page.add(LinhaPrincipal)
    page.update()


ft.app(target=main)
