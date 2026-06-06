import tkinter as tk
from datetime import timedelta

from .styles import STATUS_COLORS


def create_calendar_area(parent):
    frame = tk.Frame(parent)
    frame.pack(fill="both", expand=True)
    return frame


def _format_reservations_by_date(reservations):
    reservations_by_date = {}
    for reservation in reservations:
        reservation_date = reservation.date_course
        try:
            reservation_date = reservation_date.date()
        except AttributeError:
            pass
        reservations_by_date.setdefault(reservation_date, []).append(reservation)
    return reservations_by_date


def render_calendar(calendar_frame, month_start, reservations, on_navigate):
    for widget in calendar_frame.winfo_children():
        widget.destroy()

    calendar_frame._calendar_state = {"month_start": month_start}
    next_month = month_start.replace(
        year=month_start.year + (month_start.month // 12),
        month=(month_start.month % 12) + 1,
        day=1,
    )
    month_end = next_month - timedelta(days=1)

    header_frame = tk.Frame(calendar_frame)
    header_frame.config(bg="#f5f7fa")
    header_frame.grid(row=0, column=0, columnspan=7, sticky="ew", pady=(0, 10))
    header_frame.grid_columnconfigure(1, weight=1)

    tk.Button(
        header_frame,
        text="<",
        width=3,
        command=lambda: on_navigate(-1),
    ).grid(row=0, column=0, sticky="w")

    tk.Label(
        header_frame,
        text=f"Planning - {month_start.strftime('%B %Y')}",
        font=("Arial", 16, "bold"),
        bg="#f5f7fa",
    ).grid(row=0, column=1, sticky="nsew")

    tk.Button(
        header_frame,
        text=">",
        width=3,
        command=lambda: on_navigate(1),
    ).grid(row=0, column=2, sticky="e")

    days = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]

    for index, day in enumerate(days):
        tk.Label(
            calendar_frame,
            text=day,
            font=("Arial", 10, "bold"),
            borderwidth=1,
            relief="solid",
            width=16,
            bg="#eef4fb",
        ).grid(row=1, column=index, sticky="nsew")

    reservations_by_date = _format_reservations_by_date(reservations)

    first_day = month_start - timedelta(days=month_start.weekday())
    total_days = (month_end - first_day).days + 1
    total_weeks = (total_days + 6) // 7

    for row_index in range(total_weeks):
        calendar_frame.grid_rowconfigure(row_index + 2, weight=1)

    for day_offset in range(total_weeks * 7):
        day_date = first_day + timedelta(days=day_offset)
        row_index = day_offset // 7
        column_index = day_offset % 7
        is_current_month = day_date.month == month_start.month

        day_frame = tk.Frame(calendar_frame, borderwidth=1, relief="solid")
        day_frame.grid(row=row_index + 2, column=column_index, sticky="nsew", padx=1, pady=1)

        tk.Label(
            day_frame,
            text=f"{day_date.day} {day_date.strftime('%b')}",
            font=("Arial", 10, "bold"),
            fg="#000000" if is_current_month else "#999999",
        ).pack(anchor="nw")

        for reservation in reservations_by_date.get(day_date, [])[:4]:
            reservation_id = reservation.id
            heure = str(reservation.heure_course)[:5]
            statut = reservation.statut
            chauffeur = reservation.chauffeur
            color = STATUS_COLORS.get(statut, "#FFFFFF")

            reservation_frame = tk.Frame(day_frame, bg=color)
            reservation_frame.pack(fill="x", padx=2, pady=1)

            tk.Label(
                reservation_frame,
                text=f"{heure} - #{reservation_id}\n{chauffeur}",
                bg=color,
                font=("Arial", 8),
                wraplength=200,
                justify="left",
                anchor="w",
            ).pack(fill="x")

    for index in range(7):
        calendar_frame.grid_columnconfigure(index, weight=1)
