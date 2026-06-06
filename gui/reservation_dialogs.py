import tkinter as tk
from tkinter import ttk

from models import RESERVATION_STATUSES


def open_update_status_dialog(parent, reservation_id, current_status, on_saved=None):
    window = tk.Toplevel(parent)
    window.title("Modifier le statut")
    window.geometry("300x150")

    tk.Label(window, text=f"Réservation #{reservation_id}", font=("Arial", 12)).pack(pady=8)

    status_var = tk.StringVar(value=current_status)

    ttk.Combobox(
        window,
        textvariable=status_var,
        values=RESERVATION_STATUSES,
        state="readonly",
        width=20,
    ).pack(pady=6)

    def save():
        new_status = status_var.get()
        if on_saved:
            on_saved(new_status)
        window.destroy()

    tk.Button(window, text="Enregistrer", command=save).pack(pady=8)


def open_assign_chauffeur_dialog(parent, reservation_id, chauffeurs, on_saved=None):
    window = tk.Toplevel(parent)
    window.title("Affecter un chauffeur")
    window.geometry("340x170")
    window.transient(parent)
    window.grab_set()

    tk.Label(
        window,
        text=f"R\u00e9servation #{reservation_id}",
        font=("Arial", 12),
    ).pack(pady=8)

    choices = [chauffeur.nom for chauffeur in chauffeurs]
    chauffeur_by_name = {chauffeur.nom: chauffeur.id for chauffeur in chauffeurs}
    selected = tk.StringVar(value=choices[0] if choices else "")

    ttk.Combobox(
        window,
        textvariable=selected,
        values=choices,
        state="readonly",
        width=28,
    ).pack(pady=6)

    def save():
        chauffeur_id = chauffeur_by_name.get(selected.get())
        if chauffeur_id is None:
            return
        if on_saved:
            on_saved(chauffeur_id)
        window.destroy()

    tk.Button(window, text="Affecter", command=save).pack(pady=8)
