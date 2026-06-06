# JH Drivers App

Application de bureau Python permettant aux administrateurs de gérer les réservations, les chauffeurs, les clients et le planning de JH Drivers.

Cette application constitue le client lourd d'administration de JH Drivers.

---

## Fonctionnalités

- Authentification administrateur par identifiant et mot de passe
- Tableau de bord avec statistiques sur les réservations
- Gestion des réservations et modification de leur statut
- Affectation d'un chauffeur depuis une fenêtre dédiée
- Planning mensuel des courses
- Gestion complète des chauffeurs : ajout, modification et suppression
- Gestion complète des clients : ajout, modification et suppression
- Code couleur selon le statut des réservations

---

## Stack technique

| Composant | Technologie |
|-----------|-------------|
| Langage | Python 3 |
| Interface graphique | Tkinter / ttk |
| Base de données | MySQL / MariaDB |
| Accès BDD | mysql-connector-python avec requêtes préparées |
| Architecture | Couches séparées (modèles / services / GUI) |
| Déploiement cible | VM Debian |
| Versionning | Git / GitHub |

---

## Démo

Pour tester l'application, utilisez le compte administrateur suivant :

| Champ | Valeur |
|-------|--------|
| Identifiant | Maxime Madureira |
| Mot de passe | Efrei2026* |

---

## Structure du projet

```text
.
├── main.py
├── requirements.txt
├── install_app.sh
├── README.md
├── database/
│   ├── __init__.py
│   ├── database.py
│   └── schema.sql
├── models/
│   ├── administrator.py
│   ├── chauffeur.py
│   ├── reservation.py
│   ├── status.py
│   └── user.py
├── services/
│   ├── affectation_service.py
│   ├── auth_service.py
│   ├── chauffeur_service.py
│   ├── reservation_service.py
│   ├── stats_service.py
│   └── user_service.py
└── gui/
    ├── dashboard.py
    ├── dashboard_handlers.py
    ├── login_view.py
    ├── reservations_view.py
    ├── chauffeurs_view.py
    ├── users_view.py
    └── calendar_view.py
```

---

## Installation

### Prérequis

- Python 3.10 ou supérieur
- MySQL ou MariaDB
- Tkinter
- Git
- Base `jhdrivers-e6` initialisée avec `database/schema.sql`

---

### Installation automatique sur Debian

Depuis la racine du dépôt :

```bash
chmod +x install_app.sh
./install_app.sh
```

Le script installe les dépendances système, crée l'environnement virtuel `.venv` et installe les packages Python.

Configurez ensuite la connexion à la base :

```bash
export JHDRIVERS_DB_HOST="localhost"
export JHDRIVERS_DB_USER="jhdrivers"
export JHDRIVERS_DB_PASSWORD="jhdrivers_password"
export JHDRIVERS_DB_NAME="jhdrivers-e6"
```

Le script crée également la base de données et importe `database/schema.sql`.

Lancez ensuite l'application :

```bash
source .venv/bin/activate
python main.py
```

---

### Installation manuelle sous Windows

#### 1. Créer un environnement virtuel

Depuis la racine du dépôt :

```powershell
python -m venv .venv
.venv\Scripts\activate
```

#### 2. Installer les dépendances

```powershell
pip install -r requirements.txt
```

#### 3. Démarrer MySQL

Démarrez MySQL depuis le panneau de contrôle XAMPP et vérifiez que la base `jhdrivers-e6` existe.

#### 4. Lancer l'application

```powershell
python main.py
```

---

### Problèmes fréquents

**`python` n'est pas reconnu** : essayez `python3` ou réinstallez Python en activant l'option d'ajout au `PATH`.

**L'environnement virtuel ne s'active pas sous PowerShell** :

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

**Erreur de connexion MySQL** : vérifiez que MySQL est démarré et que les variables `JHDRIVERS_DB_*` correspondent à votre configuration.

**Erreur Tkinter sous Debian** :

```bash
sudo apt install python3-tk
```
