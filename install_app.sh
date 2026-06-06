#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

DB_NAME="${DB_NAME:-jhdrivers-e6}"
DB_USER="${DB_USER:-jhdrivers}"
DB_PASS="${DB_PASS:-jhdrivers_password}"
DB_HOST="${DB_HOST:-localhost}"

echo "Installation des dependances Python..."
sudo apt update
sudo apt install -y python3 python3-pip python3-venv python3-tk mariadb-server

echo "Demarrage de MariaDB..."
sudo systemctl enable mariadb
sudo systemctl start mariadb

echo "Creation de la base et de l'utilisateur..."
sudo mysql <<SQL
CREATE DATABASE IF NOT EXISTS \`$DB_NAME\` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASS';
GRANT ALL PRIVILEGES ON \`$DB_NAME\`.* TO '$DB_USER'@'localhost';
FLUSH PRIVILEGES;
SQL

echo "Import du schema SQL..."
mysql -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" < database/schema.sql

echo "Creation de l'environnement virtuel..."
python3 -m venv .venv
source .venv/bin/activate

echo "Installation des packages Python..."
pip install --upgrade pip
pip install -r requirements.txt

cat > .env.example <<ENV
JHDRIVERS_DB_HOST=$DB_HOST
JHDRIVERS_DB_USER=$DB_USER
JHDRIVERS_DB_PASSWORD=$DB_PASS
JHDRIVERS_DB_NAME=$DB_NAME
ENV

echo
echo "Installation app terminee."
echo "Avant de lancer l'app, configure les variables si besoin :"
echo "export JHDRIVERS_DB_HOST=\"$DB_HOST\""
echo "export JHDRIVERS_DB_USER=\"$DB_USER\""
echo "export JHDRIVERS_DB_PASSWORD=\"$DB_PASS\""
echo "export JHDRIVERS_DB_NAME=\"$DB_NAME\""
echo
echo "Pour lancer l'app :"
echo "source .venv/bin/activate && python main.py"
