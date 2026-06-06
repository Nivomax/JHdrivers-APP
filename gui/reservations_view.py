import tkinter as tk
from tkinter import ttk
from .styles import STATUS_COLORS


def create_reservations_view(parent):
    reservations_area = tk.Frame(parent)
    reservations_area.pack(fill="both", expand=True)

    header_reservations = tk.Frame(reservations_area)
    header_reservations.pack(fill="x", pady=10)



    frame_reservations_actions = tk.Frame(header_reservations)
    frame_reservations_actions.pack(side="right")

    columns_reservations = (
        "id",
        "client",
        "telephone",
        "depart",
        "arrivee",
        "date",
        "heure",
        "statut",
        "chauffeur"
    )

    reservations_tree = ttk.Treeview(
        reservations_area,
        columns=columns_reservations,
        show="headings"
    )

    for col, title in zip(columns_reservations, [
        "ID", "Client", "Téléphone", "Départ", "Arrivée",
        "Date", "Heure", "Statut", "Chauffeur"
    ]):
        reservations_tree.heading(col, text=title)

    reservations_tree.column("id", width=40)
    reservations_tree.column("client", width=120)
    reservations_tree.column("telephone", width=100)
    reservations_tree.column("depart", width=150)
    reservations_tree.column("arrivee", width=150)
    reservations_tree.column("date", width=85)
    reservations_tree.column("heure", width=75)
    reservations_tree.column("statut", width=95)
    reservations_tree.column("chauffeur", width=120)

    for status, color in STATUS_COLORS.items():
        reservations_tree.tag_configure(f"status_{status}", background=color)

    reservations_tree.tag_configure('even', background='#ffffff')
    reservations_tree.tag_configure('odd', background='#fbfbfb')

    reservations_tree.pack(fill="both", expand=True)

    return {
        'area': reservations_area,
        'tree': reservations_tree,
        'actions_frame': frame_reservations_actions,
    }


def create_reservations_actions(actions_frame, on_update_status=None, on_assign=None, on_refresh=None):
    tk.Button(
        actions_frame,
        text="Modifier statut",
        command=on_update_status,
    ).pack(side="left", padx=5)

    tk.Button(
        actions_frame,
        text="Affecter",
        command=on_assign,
    ).pack(side="left", padx=5)

    tk.Button(
        actions_frame,
        text="Actualiser",
        command=on_refresh,
    ).pack(side="left", padx=5)
