from database import get_connection
from models import Administrator


def authenticate_administrator(identifiant, mot_de_passe):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, identifiant
        FROM administrateurs
        WHERE identifiant = %s AND mot_de_passe = %s
        """,
        (identifiant, mot_de_passe),
    )
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return Administrator(*row) if row else None
