import tkinter as tk
from tkinter import ttk

from .styles import apply_styles

from .calendar_view import create_calendar_area
from .chauffeurs_view import create_chauffeurs_view
from .dashboard_handlers import (
    add_client,
    add_chauffeur,
    assign_chauffeur,
    delete_client,
    delete_chauffeur,
    edit_client,
    edit_chauffeur,
    load_calendar,
    load_chauffeurs,
    load_reservations,
    load_stats,
    load_users,
    update_status,
)
from .reservations_view import create_reservations_actions, create_reservations_view
from .users_view import create_users_view


def open_dashboard():
    dashboard = tk.Tk()
    dashboard.title("JH Drivers - Dashboard")
    dashboard.geometry("1500x800")

    notebook = ttk.Notebook(dashboard)
    notebook.pack(fill="both", expand=True)
    apply_styles(dashboard)

    tab_reservations = tk.Frame(notebook)
    tab_planning = tk.Frame(notebook)
    tab_chauffeurs = tk.Frame(notebook)
    tab_users = tk.Frame(notebook)

    notebook.add(tab_reservations, text="Réservations")
    notebook.add(tab_planning, text="Planning")
    notebook.add(tab_chauffeurs, text="Chauffeurs")
    notebook.add(tab_users, text="Clients")

    # Stats tab
    tab_stats = tk.Frame(notebook)
    notebook.add(tab_stats, text="Stats")

    stats_frame = tk.Frame(tab_stats)
    stats_frame.pack(fill="both", expand=True, padx=20, pady=20)

    stats_labels = {
        "total": tk.Label(stats_frame, font=("Arial", 16)),
        "attente": tk.Label(stats_frame, font=("Arial", 16)),
        "confirmees": tk.Label(stats_frame, font=("Arial", 16)),
        "terminees": tk.Label(stats_frame, font=("Arial", 16)),
    }

    # arrange labels vertically
    for lbl in stats_labels.values():
        lbl.pack(anchor="w", pady=4)

    main_reservation_frame = tk.Frame(tab_reservations)
    main_reservation_frame.pack(fill="both", expand=True)

    res_widgets = create_reservations_view(main_reservation_frame)
    reservations_tree = res_widgets["tree"]
    frame_reservations_actions = res_widgets["actions_frame"]
    calendar_frame = create_calendar_area(tab_planning)

    def refresh_chauffeurs():
        load_chauffeurs(chauffeurs_tree)

    def refresh_users():
        load_users(users_tree)

    def refresh_chauffeurs_and_stats():
        load_chauffeurs(chauffeurs_tree)
        load_stats(stats_labels)

    def refresh_reservations_and_calendar():
        load_reservations(reservations_tree)
        load_calendar(calendar_frame)

    ch_widgets = create_chauffeurs_view(
        tab_chauffeurs,
        on_add=lambda: add_chauffeur(
            chauffeurs_tree,
            stats_labels,
            refresh_chauffeurs_and_stats,
        ),
        on_edit=lambda: edit_chauffeur(
            chauffeurs_tree,
            refresh_chauffeurs,
        ),
        on_delete=lambda: delete_chauffeur(
            chauffeurs_tree,
            stats_labels,
            refresh_chauffeurs_and_stats,
        ),
        on_refresh=refresh_chauffeurs,
    )
    chauffeurs_tree = ch_widgets["tree"]

    users_widgets = create_users_view(
        tab_users,
        on_add=lambda: add_client(users_tree, refresh_users),
        on_edit=lambda: edit_client(users_tree, refresh_users),
        on_delete=lambda: delete_client(users_tree, refresh_users),
        on_refresh=refresh_users,
    )
    users_tree = users_widgets["tree"]

    create_reservations_actions(
        frame_reservations_actions,
        on_update_status=lambda: update_status(
            reservations_tree,
            stats_labels,
            calendar_frame,
        ),
        on_assign=lambda: assign_chauffeur(
            reservations_tree,
            chauffeurs_tree,
            stats_labels,
            calendar_frame,
        ),
        on_refresh=refresh_reservations_and_calendar,
    )

    load_stats(stats_labels)
    load_reservations(reservations_tree)
    load_chauffeurs(chauffeurs_tree)
    load_users(users_tree)
    load_calendar(calendar_frame)

    dashboard.mainloop()
