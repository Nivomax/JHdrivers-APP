import tkinter as tk
from tkinter import messagebox

from services.auth_service import authenticate_administrator


def open_login(on_success):
    root = tk.Tk()
    root.title("JH Drivers - Client lourd")
    root.geometry("400x300")

    tk.Label(root, text="Connexion administrateur", font=("Arial", 16)).pack(pady=20)

    tk.Label(root, text="Identifiant").pack()
    entry_identifiant = tk.Entry(root)
    entry_identifiant.pack()

    tk.Label(root, text="Mot de passe").pack()
    entry_password = tk.Entry(root, show="*")
    entry_password.pack()

    def login():
        administrator = authenticate_administrator(
            entry_identifiant.get(),
            entry_password.get(),
        )

        if administrator:
            messagebox.showinfo("Connexion", "Connexion réussie")
            root.destroy()
            on_success(administrator)
        else:
            messagebox.showerror("Erreur", "Identifiants incorrects")

    tk.Button(root, text="Se connecter", command=login).pack(pady=20)
    root.mainloop()
