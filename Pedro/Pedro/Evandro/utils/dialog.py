import flet as ft


sair_dialog = ft.CupertinoAlertDialog(
        title=ft.Text("Ao sair da página todos os dados não salvos serão perdidos!"),
        content=ft.Text("Confirma sair?"),
        actions=[
            ft.CupertinoDialogAction(
                "Sair",
                is_destructive_action=True,
            ),
            ft.CupertinoDialogAction(text="Cancelar"),
        ],
    )