from datetime import date, timedelta
from tkinter import messagebox

from models import RESERVATION_STATUSES_NOT_ASSIGNABLE
from services.affectation_service import (
    AffectationError,
    assign_chauffeur as service_assign_chauffeur,
)
from services.chauffeur_service import (
    add_chauffeur as service_add_chauffeur,
    delete_chauffeur as service_delete_chauffeur,
    get_all_chauffeurs,
    get_available_chauffeurs,
    get_chauffeur_by_id,
    update_chauffeur as service_update_chauffeur,
)
from services.reservation_service import (
    get_all_reservations,
    get_reservation_by_id,
    get_reservations_between,
    update_reservation_status,
)
from services.stats_service import get_stats
from services.user_service import (
    add_user as service_add_user,
    delete_user as service_delete_user,
    get_all_users,
    get_user_by_id,
    update_user as service_update_user,
)

from .calendar_view import render_calendar
from .chauffeur_dialogs import (
    confirm_delete_chauffeur,
    open_add_chauffeur_dialog,
    open_edit_chauffeur_dialog,
)
from .client_dialogs import (
    confirm_delete_client,
    open_add_client_dialog,
    open_edit_client_dialog,
)
from .reservation_dialogs import (
    open_assign_chauffeur_dialog,
    open_update_status_dialog,
)


def load_stats(labels):
    stats = get_stats()

    labels["total"].config(text=f"Réservations totales : {stats['total']}")
    labels["attente"].config(text=f"En attente : {stats['attente']}")
    labels["confirmees"].config(text=f"Confirmées : {stats['confirmees']}")
    labels["terminees"].config(text=f"Terminées : {stats['terminees']}")


def load_chauffeurs(tree):
    for row in tree.get_children():
        tree.delete(row)
    for index, chauffeur in enumerate(get_all_chauffeurs()):
        stripe = "even" if index % 2 == 0 else "odd"
        tree.insert(
            "",
            "end",
            values=(chauffeur.id, chauffeur.nom, chauffeur.telephone, chauffeur.email),
            tags=(stripe,),
        )


def load_users(tree):
    for row in tree.get_children():
        tree.delete(row)
    for index, user in enumerate(get_all_users()):
        stripe = "even" if index % 2 == 0 else "odd"
        tree.insert(
            "",
            "end",
            values=(user.id, user.prenom, user.nom, user.email, user.telephone),
            tags=(stripe,),
        )


def add_chauffeur(chauffeurs_tree, stats_labels, refresh_callbacks=None):
    parent = chauffeurs_tree.winfo_toplevel() if chauffeurs_tree else None

    def on_success(data):
        service_add_chauffeur(data["nom"], data["telephone"], data["email"])
        if refresh_callbacks:
            refresh_callbacks()

    open_add_chauffeur_dialog(parent, on_success=on_success)


def edit_chauffeur(chauffeurs_tree, refresh_callbacks=None):
    selected = chauffeurs_tree.selection()

    if not selected:
        messagebox.showwarning("Attention", "Sélectionnez un chauffeur.")
        return

    chauffeur_id = chauffeurs_tree.item(selected[0])["values"][0]
    chauffeur = get_chauffeur_by_id(chauffeur_id)
    if chauffeur is None:
        messagebox.showerror("Erreur", "Ce chauffeur n'existe plus.")
        return

    parent = chauffeurs_tree.winfo_toplevel()

    def on_success(data):
        service_update_chauffeur(
            data["id"],
            data["nom"],
            data["telephone"],
            data["email"],
        )
        if refresh_callbacks:
            refresh_callbacks()

    open_edit_chauffeur_dialog(parent, chauffeur, on_success=on_success)


def delete_chauffeur(chauffeurs_tree, stats_labels, refresh_callbacks=None):
    selected = chauffeurs_tree.selection()

    if not selected:
        messagebox.showwarning("Attention", "Sélectionnez un chauffeur.")
        return

    chauffeur_id = chauffeurs_tree.item(selected[0])["values"][0]
    parent = chauffeurs_tree.winfo_toplevel()

    def on_confirm():
        service_delete_chauffeur(chauffeur_id)
        if refresh_callbacks:
            refresh_callbacks()

    confirm_delete_chauffeur(parent, chauffeur_id, on_confirm)


def add_client(clients_tree, refresh_callbacks=None):
    def on_success(data):
        service_add_user(
            data["prenom"],
            data["nom"],
            data["email"],
            data["telephone"],
            data["mot_de_passe"],
        )
        if refresh_callbacks:
            refresh_callbacks()

    open_add_client_dialog(clients_tree.winfo_toplevel(), on_success=on_success)


def edit_client(clients_tree, refresh_callbacks=None):
    selected = clients_tree.selection()
    if not selected:
        messagebox.showwarning("Attention", "S\u00e9lectionnez un client.")
        return

    client_id = clients_tree.item(selected[0])["values"][0]
    client = get_user_by_id(client_id)
    if client is None:
        messagebox.showerror("Erreur", "Ce client n'existe plus.")
        return

    def on_success(data):
        service_update_user(
            data["id"],
            data["prenom"],
            data["nom"],
            data["email"],
            data["telephone"],
            data["mot_de_passe"],
        )
        if refresh_callbacks:
            refresh_callbacks()

    open_edit_client_dialog(
        clients_tree.winfo_toplevel(),
        client,
        on_success=on_success,
    )


def delete_client(clients_tree, refresh_callbacks=None):
    selected = clients_tree.selection()
    if not selected:
        messagebox.showwarning("Attention", "S\u00e9lectionnez un client.")
        return

    client_id = clients_tree.item(selected[0])["values"][0]

    def on_confirm():
        service_delete_user(client_id)
        if refresh_callbacks:
            refresh_callbacks()

    confirm_delete_client(clients_tree.winfo_toplevel(), on_confirm=on_confirm)


def _selected_reservation(tree):
    selected = tree.selection()
    if not selected:
        return None
    reservation_id = tree.item(selected[0])["values"][0]
    return get_reservation_by_id(reservation_id)


def load_reservations(tree):
    for row in tree.get_children():
        tree.delete(row)
    for reservation in get_all_reservations():
        tree.insert(
            "",
            "end",
            values=(
                reservation.id,
                reservation.nom_client,
                reservation.telephone,
                reservation.adresse_depart,
                reservation.adresse_arrivee,
                reservation.date_course,
                reservation.heure_course,
                reservation.statut,
                reservation.chauffeur,
            ),
            tags=(f"status_{reservation.statut}",),
        )


def update_status(reservations_tree, stats_labels, calendar_frame):
    reservation = _selected_reservation(reservations_tree)

    if reservation is None:
        messagebox.showwarning("Attention", "Sélectionnez une réservation.")
        return

    parent = reservations_tree.winfo_toplevel()

    def on_saved(new_status):
        update_reservation_status(reservation.id, new_status)
        load_reservations(reservations_tree)
        load_stats(stats_labels)
        load_calendar(calendar_frame)

    open_update_status_dialog(parent, reservation.id, reservation.statut, on_saved=on_saved)


def assign_chauffeur(reservations_tree, chauffeurs_tree, stats_labels, calendar_frame):
    reservation = _selected_reservation(reservations_tree)

    if reservation is None:
        messagebox.showwarning("Attention", "Sélectionnez une réservation.")
        return

    if reservation.statut in RESERVATION_STATUSES_NOT_ASSIGNABLE:
        messagebox.showwarning(
            "Action impossible",
            "Impossible d'affecter une réservation annulée ou terminée.",
        )
        return

    chauffeurs = get_available_chauffeurs()
    if not chauffeurs:
        messagebox.showwarning("Attention", "Aucun chauffeur disponible.")
        return

    def on_saved(chauffeur_id):
        try:
            service_assign_chauffeur(reservation.id, chauffeur_id)
        except AffectationError as error:
            messagebox.showwarning("Action impossible", str(error))
            return

        load_reservations(reservations_tree)
        load_chauffeurs(chauffeurs_tree)
        load_stats(stats_labels)
        load_calendar(calendar_frame)
        messagebox.showinfo("Succès", "Réservation affectée.")

    open_assign_chauffeur_dialog(
        reservations_tree.winfo_toplevel(),
        reservation.id,
        chauffeurs,
        on_saved=on_saved,
    )


def _add_months(month_start, delta_months):
    month = month_start.month - 1 + delta_months
    year = month_start.year + month // 12
    month = month % 12 + 1
    return date(year, month, 1)


def load_calendar(calendar_frame, month_start=None):
    state = getattr(calendar_frame, "_calendar_state", None)
    if month_start is None:
        if state is None:
            today = date.today()
            month_start = date(today.year, today.month, 1)
        else:
            month_start = state["month_start"]

    next_month = _add_months(month_start, 1)
    month_end = next_month - timedelta(days=1)
    reservations = get_reservations_between(month_start, month_end)

    def on_navigate(delta_months):
        load_calendar(calendar_frame, month_start=_add_months(month_start, delta_months))

    render_calendar(calendar_frame, month_start, reservations, on_navigate)
