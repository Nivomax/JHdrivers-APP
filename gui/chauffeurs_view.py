import tkinter as tk
from tkinter import ttk


def create_chauffeurs_view(parent, on_add=None, on_edit=None, on_delete=None, on_refresh=None):
    frame = tk.Frame(parent)
    frame.pack(fill="both", expand=True)

    actions_frame = tk.Frame(frame)
    actions_frame.pack(fill="x", padx=20, pady=10)

    buttons_frame = tk.Frame(actions_frame)
    buttons_frame.pack(side="right")

    tk.Button(
        buttons_frame,
        text="Ajouter",
        command=on_add,
    ).pack(side="left", padx=10)

    tk.Button(
        buttons_frame,
        text="Modifier",
        command=on_edit,
    ).pack(side="left", padx=10)

    tk.Button(
        buttons_frame,
        text="Supprimer",
        command=on_delete,
    ).pack(side="left", padx=10)

    tk.Button(
        buttons_frame,
        text="Actualiser",
        command=on_refresh,
    ).pack(side="left", padx=10)

    columns_chauffeurs = (
        "id",
        "nom",
        "telephone",
        "email"
    )

    tree = ttk.Treeview(
        frame,
        columns=columns_chauffeurs,
        show="headings"
    )

    for col, title in zip(columns_chauffeurs, [
        "ID", "Nom", "Téléphone", "Email"
    ]):
        tree.heading(col, text=title)

    tree.column("id", width=50)
    tree.column("nom", width=150)
    tree.column("telephone", width=120)
    tree.column("email", width=190)

    tree.pack(fill="both", expand=True, padx=20, pady=20)

    tree.tag_configure('even', background='#ffffff')
    tree.tag_configure('odd', background='#fbfbfb')

    return {
        'area': frame,
        'actions_frame': actions_frame,
        'tree': tree
    }
