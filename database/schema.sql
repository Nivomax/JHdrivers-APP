CREATE TABLE IF NOT EXISTS clients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    prenom VARCHAR(100) NOT NULL,
    nom VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    telephone VARCHAR(20) NOT NULL,
    mot_de_passe VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS administrateurs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    identifiant VARCHAR(100) NOT NULL UNIQUE,
    mot_de_passe VARCHAR(255) NOT NULL
);

INSERT INTO administrateurs (identifiant, mot_de_passe)
VALUES ('Maxime Madureira', 'Efrei2026*')
ON DUPLICATE KEY UPDATE identifiant = identifiant;

CREATE TABLE IF NOT EXISTS chauffeurs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(150) NOT NULL,
    telephone VARCHAR(20) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS reservations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom_client VARCHAR(150) NOT NULL,
    email_client VARCHAR(150) NOT NULL,
    telephone VARCHAR(20) NOT NULL,
    adresse_depart VARCHAR(255) NOT NULL,
    adresse_arrivee VARCHAR(255) NOT NULL,
    date_course DATE NOT NULL,
    heure_course TIME NOT NULL,
    statut VARCHAR(50) NOT NULL DEFAULT 'En attente',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS affectations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    reservation_id INT NOT NULL,
    chauffeur_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_reservation_affectation (reservation_id),
    CONSTRAINT fk_affectations_reservation
        FOREIGN KEY (reservation_id)
        REFERENCES reservations(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_affectations_chauffeur
        FOREIGN KEY (chauffeur_id)
        REFERENCES chauffeurs(id)
        ON DELETE CASCADE
);

INSERT INTO clients (prenom, nom, email, telephone, mot_de_passe) VALUES
    ('Alice', 'Martin', 'alice.martin@example.com', '0610203040', 'Demo2026*'),
    ('Thomas', 'Bernard', 'thomas.bernard@example.com', '0620304050', 'Demo2026*'),
    ('Sofia', 'Moreau', 'sofia.moreau@example.com', '0630405060', 'Demo2026*'),
    ('Lucas', 'Dubois', 'lucas.dubois@example.com', '0670809010', 'Demo2026*'),
    ('Emma', 'Laurent', 'emma.laurent@example.com', '0680901020', 'Demo2026*')
ON DUPLICATE KEY UPDATE email = VALUES(email);

INSERT INTO chauffeurs (nom, telephone, email) VALUES
    ('Julien Leroy', '0640506070', 'julien.leroy@example.com'),
    ('Nadia Petit', '0650607080', 'nadia.petit@example.com'),
    ('Karim Robert', '0660708090', 'karim.robert@example.com')
ON DUPLICATE KEY UPDATE email = VALUES(email);

INSERT INTO reservations
    (nom_client, email_client, telephone, adresse_depart, adresse_arrivee, date_course, heure_course, statut)
VALUES
    ('Alice Martin', 'alice.martin@example.com', '0610203040', '10 avenue des Champs-Elysees, Paris', 'Aeroport Charles-de-Gaulle', '2026-06-12', '08:30:00', 'Confirmé'),
    ('Thomas Bernard', 'thomas.bernard@example.com', '0620304050', 'Gare de Lyon, Paris', 'La Defense, Courbevoie', '2026-06-15', '14:00:00', 'En attente'),
    ('Sofia Moreau', 'sofia.moreau@example.com', '0630405060', 'Orly 4', 'Place Vendome, Paris', '2026-05-28', '19:15:00', 'Terminé'),
    ('Alice Martin', 'alice.martin@example.com', '0610203040', 'Hotel de Ville, Paris', 'Versailles', '2026-06-20', '10:00:00', 'Annulé'),
    ('Lucas Dubois', 'lucas.dubois@example.com', '0670809010', 'Gare du Nord, Paris', 'Aeroport Paris-Orly', '2026-06-22', '06:45:00', 'En attente'),
    ('Emma Laurent', 'emma.laurent@example.com', '0680901020', 'Montparnasse, Paris', 'Neuilly-sur-Seine', '2026-06-23', '09:30:00', 'Confirmé'),
    ('Thomas Bernard', 'thomas.bernard@example.com', '0620304050', 'Bercy, Paris', 'Boulogne-Billancourt', '2026-06-24', '18:00:00', 'En attente'),
    ('Sofia Moreau', 'sofia.moreau@example.com', '0630405060', 'Opera Garnier, Paris', 'Aeroport Charles-de-Gaulle', '2026-06-25', '05:30:00', 'Confirmé'),
    ('Alice Martin', 'alice.martin@example.com', '0610203040', 'Saint-Germain-des-Pres, Paris', 'Disneyland Paris', '2026-06-27', '08:00:00', 'En attente'),
    ('Lucas Dubois', 'lucas.dubois@example.com', '0670809010', 'La Defense, Courbevoie', 'Gare de Lyon, Paris', '2026-05-30', '16:20:00', 'Terminé'),
    ('Emma Laurent', 'emma.laurent@example.com', '0680901020', 'Place de la Concorde, Paris', 'Versailles', '2026-06-28', '11:15:00', 'Annulé'),
    ('Thomas Bernard', 'thomas.bernard@example.com', '0620304050', 'Aeroport Paris-Orly', 'Le Marais, Paris', '2026-06-29', '13:40:00', 'Confirmé'),
    ('Sofia Moreau', 'sofia.moreau@example.com', '0630405060', 'Trocadero, Paris', 'Gare Montparnasse, Paris', '2026-07-01', '17:10:00', 'En attente'),
    ('Emma Laurent', 'emma.laurent@example.com', '0680901020', 'Aeroport Charles-de-Gaulle', 'Champs-Elysees, Paris', '2026-07-03', '20:30:00', 'En attente');

INSERT INTO affectations (reservation_id, chauffeur_id) VALUES
    (1, 1),
    (3, 2);
