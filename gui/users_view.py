import tkinter as tk
from tkinter import ttk


def create_users_view(parent, on_add=None, on_edit=None, on_delete=None, on_refresh=None):
    frame = tk.Frame(parent)
    frame.pack(fill="both", expand=True)

    header = tk.Frame(frame)
    header.pack(fill="x", pady=10)

    tk.Label(
        header,
        text="Liste des clients",
        font=("Arial", 18),
    ).pack(side="left")

    actions = tk.Frame(header)
    actions.pack(side="right", padx=10)

    for text, command in (
        ("Ajouter", on_add),
        ("Modifier", on_edit),
        ("Supprimer", on_delete),
        ("Actualiser", on_refresh),
    ):
        tk.Button(actions, text=text, command=command).pack(side="left", padx=5)

    columns_users = (
        "id",
        "prenom",
        "nom",
        "email",
        "telephone",
    )

    tree = ttk.Treeview(
        frame,
        columns=columns_users,
        show="headings",
    )

    for col, title in zip(
        columns_users,
        ["ID", "Prenom", "Nom", "Email", "Telephone"],
    ):
        tree.heading(col, text=title)

    tree.column("id", width=50)
    tree.column("prenom", width=140)
    tree.column("nom", width=140)
    tree.column("email", width=220)
    tree.column("telephone", width=130)

    tree.pack(fill="both", expand=True, padx=20, pady=20)

    tree.tag_configure("even", background="#ffffff")
    tree.tag_configure("odd", background="#fbfbfb")

    return {
        "area": frame,
        "tree": tree,
    }
