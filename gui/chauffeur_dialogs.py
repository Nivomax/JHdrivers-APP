import tkinter as tk
from tkinter import messagebox



def open_add_chauffeur_dialog(parent, on_success=None):
    window = tk.Toplevel(parent)
    window.title("Ajouter un chauffeur")
    window.geometry("400x300")

    tk.Label(window, text="Nom").pack()
    entry_nom = tk.Entry(window)
    entry_nom.pack()

    tk.Label(window, text="Téléphone").pack()
    entry_telephone = tk.Entry(window)
    entry_telephone.pack()

    tk.Label(window, text="Email").pack()
    entry_email = tk.Entry(window)
    entry_email.pack()

    def save():
        if entry_nom.get().strip() == "":
            messagebox.showwarning("Attention", "Le nom est obligatoire.")
            return

        # Return entered values to caller via on_success
        if on_success:
            on_success({
                "nom": entry_nom.get(),
                "telephone": entry_telephone.get(),
                "email": entry_email.get(),
            })

        window.destroy()

    tk.Button(window, text="Ajouter", command=save).pack(pady=20)


def open_edit_chauffeur_dialog(parent, chauffeur, on_success=None):
    window = tk.Toplevel(parent)
    window.title("Modifier un chauffeur")
    window.geometry("400x350")

    tk.Label(window, text="Nom").pack()
    entry_nom = tk.Entry(window)
    entry_nom.insert(0, chauffeur.nom)
    entry_nom.pack()

    tk.Label(window, text="Téléphone").pack()
    entry_telephone = tk.Entry(window)
    entry_telephone.insert(0, chauffeur.telephone)
    entry_telephone.pack()

    tk.Label(window, text="Email").pack()
    entry_email = tk.Entry(window)
    entry_email.insert(0, chauffeur.email)
    entry_email.pack()

    def save():
        if on_success:
            on_success({
                "id": chauffeur.id,
                "nom": entry_nom.get(),
                "telephone": entry_telephone.get(),
                "email": entry_email.get(),
            })

        window.destroy()

    tk.Button(window, text="Enregistrer", command=save).pack(pady=20)


def confirm_delete_chauffeur(parent, chauffeur_id, on_confirm=None):
    if not messagebox.askyesno("Confirmation", "Supprimer ce chauffeur ?"):
        return

    if on_confirm:
        on_confirm()

    messagebox.showinfo("Succès", "Chauffeur supprimé.")
