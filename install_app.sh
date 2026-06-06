#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Installation des dependances Python..."
sudo apt update
sudo apt install -y python3 python3-pip python3-venv python3-tk

echo "Creation de l'environnement virtuel..."
python3 -m venv .venv
source .venv/bin/activate

echo "Installation des packages Python..."
pip install --upgrade pip
pip install -r requirements.txt

echo
echo "Installation app terminee."
echo "La base distante et les identifiants sont geres dans le code ou via variables d'environnement."
echo
echo "Pour lancer l'app :"
echo "source .venv/bin/activate && python main.py"
