import tkinter as tk
from tkinter import messagebox


def _client_dialog(parent, title, client=None, on_success=None):
    window = tk.Toplevel(parent)
    window.title(title)
    window.geometry("400x420")
    window.transient(parent)
    window.grab_set()

    fields = {}
    labels = (
        ("prenom", "Pr\u00e9nom"),
        ("nom", "Nom"),
        ("email", "Email"),
        ("telephone", "T\u00e9l\u00e9phone"),
        ("mot_de_passe", "Mot de passe"),
    )

    for key, label in labels:
        tk.Label(window, text=label).pack()
        entry = tk.Entry(window, show="*" if key == "mot_de_passe" else "")
        if client is not None and key != "mot_de_passe":
            entry.insert(0, getattr(client, key))
        entry.pack()
        fields[key] = entry

    if client is not None:
        tk.Label(
            window,
            text="Laisser le mot de passe vide pour le conserver.",
        ).pack(pady=(4, 0))

    def save():
        data = {key: entry.get().strip() for key, entry in fields.items()}
        if not all(data[key] for key in ("prenom", "nom", "email", "telephone")):
            messagebox.showwarning("Attention", "Tous les champs sont obligatoires.")
            return
        if client is None and not data["mot_de_passe"]:
            messagebox.showwarning("Attention", "Le mot de passe est obligatoire.")
            return
        if client is not None:
            data["id"] = client.id
        if on_success:
            on_success(data)
        window.destroy()

    tk.Button(
        window,
        text="Enregistrer" if client else "Ajouter",
        command=save,
    ).pack(pady=20)


def open_add_client_dialog(parent, on_success=None):
    _client_dialog(parent, "Ajouter un client", on_success=on_success)


def open_edit_client_dialog(parent, client, on_success=None):
    _client_dialog(parent, "Modifier un client", client=client, on_success=on_success)


def confirm_delete_client(parent, on_confirm=None):
    if not messagebox.askyesno("Confirmation", "Supprimer ce client ?"):
        return
    if on_confirm:
        on_confirm()
    messagebox.showinfo("Succ\u00e8s", "Client supprim\u00e9.")
