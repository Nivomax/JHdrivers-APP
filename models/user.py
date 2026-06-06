from dataclasses import dataclass


@dataclass
class User:
    id: int
    prenom: str
    nom: str
    email: str
    telephone: str
