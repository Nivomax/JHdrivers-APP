from database import get_connection
from models import Chauffeur


def get_all_chauffeurs():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, nom, telephone, email
        FROM chauffeurs
        ORDER BY nom
        """
    )
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [Chauffeur(*row) for row in rows]


def get_available_chauffeurs():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, nom, telephone, email
        FROM chauffeurs
        ORDER BY nom
        """
    )
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [Chauffeur(*row) for row in rows]


def add_chauffeur(nom, telephone, email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO chauffeurs (nom, telephone, email)
        VALUES (%s, %s, %s)
        """,
        (nom, telephone, email),
    )

    conn.commit()
    cursor.close()
    conn.close()


def get_chauffeur_by_id(chauffeur_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, nom, telephone, email
        FROM chauffeurs
        WHERE id = %s
        """,
        (chauffeur_id,),
    )
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return Chauffeur(*row) if row else None


def update_chauffeur(chauffeur_id, nom, telephone, email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE chauffeurs
        SET nom = %s,
            telephone = %s,
            email = %s
        WHERE id = %s
        """,
        (nom, telephone, email, chauffeur_id),
    )

    conn.commit()
    cursor.close()
    conn.close()


def delete_chauffeur(chauffeur_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM affectations WHERE chauffeur_id = %s", (chauffeur_id,))
    cursor.execute("DELETE FROM chauffeurs WHERE id = %s", (chauffeur_id,))

    conn.commit()
    cursor.close()
    conn.close()
