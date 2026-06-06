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
- Accès MySQL avec droits de lecture/écriture (et idéalement création de tables)

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
export DB_HOST="mysql-jhdrivers.alwaysdata.net"
export DB_PORT="3306"
export DB_NAME="jhdrivers_e6"
export DB_USER="jhdrivers_max"
export DB_PASS="Maxime94400"
```

Au démarrage, l'application vérifie et initialise automatiquement le schéma SQL depuis `database/schema.sql` (création des tables si elles n'existent pas).

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

Assurez-vous que MySQL est accessible, puis configurez les variables d'environnement si nécessaire :

```powershell
$env:DB_HOST="mysql-jhdrivers.alwaysdata.net"
$env:DB_PORT="3306"
$env:DB_NAME="jhdrivers_e6"
$env:DB_USER="jhdrivers_max"
$env:DB_PASS="Maxime94400"
```

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

**Erreur de connexion MySQL** : vérifiez l'hôte, le port, la base, l'utilisateur et le mot de passe (`DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASS`).

**Erreur "Table ... doesn't exist"** : l'application tente de créer automatiquement les tables à partir de `database/schema.sql` au premier accès. Si l'erreur persiste, vérifiez que l'utilisateur MySQL a bien les droits `CREATE`/`ALTER` sur la base.

**Erreur Tkinter sous Debian** :

```bash
sudo apt install python3-tk
```
