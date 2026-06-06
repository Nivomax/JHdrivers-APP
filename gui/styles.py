from tkinter import ttk

from models import (
    RESERVATION_STATUS_CANCELLED,
    RESERVATION_STATUS_COMPLETED,
    RESERVATION_STATUS_CONFIRMED,
    RESERVATION_STATUS_PENDING,
)

STATUS_COLORS = {
    RESERVATION_STATUS_PENDING: "#F6E58D",
    RESERVATION_STATUS_CONFIRMED: "#BADFB0",
    RESERVATION_STATUS_COMPLETED: "#DADADA",
    RESERVATION_STATUS_CANCELLED: "#F5B7B1",
}


def apply_styles(root):
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except Exception:
        pass

    style.configure("Treeview", font=("Arial", 10), rowheight=24)
    style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#e8eef6")
    style.configure("TButton", padding=6)
    style.configure("TCombobox", padding=4)
