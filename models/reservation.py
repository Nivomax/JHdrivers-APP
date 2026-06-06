from dataclasses import dataclass
from datetime import date, time


@dataclass
class Reservation:
    id: int
    nom_client: str
    telephone: str
    adresse_depart: str
    adresse_arrivee: str
    date_course: date
    heure_course: time
    statut: str
    chauffeur: str | None = None


@dataclass
class CalendarReservation:
    id: int
    date_course: date
    heure_course: time
    nom_client: str
    statut: str
    chauffeur: str | None = None
