from database import get_connection
from models import User


def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, prenom, nom, email, telephone
        FROM clients
        ORDER BY nom, prenom
        """
    )
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [User(*row) for row in rows]


def get_user_by_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, prenom, nom, email, telephone FROM clients WHERE id = %s",
        (user_id,),
    )
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return User(*row) if row else None


def add_user(prenom, nom, email, telephone, mot_de_passe):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO clients (prenom, nom, email, telephone, mot_de_passe)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (prenom, nom, email, telephone, mot_de_passe),
    )
    conn.commit()
    cursor.close()
    conn.close()


def update_user(user_id, prenom, nom, email, telephone, mot_de_passe=None):
    conn = get_connection()
    cursor = conn.cursor()

    if mot_de_passe:
        cursor.execute(
            """
            UPDATE clients
            SET prenom = %s, nom = %s, email = %s, telephone = %s, mot_de_passe = %s
            WHERE id = %s
            """,
            (prenom, nom, email, telephone, mot_de_passe, user_id),
        )
    else:
        cursor.execute(
            """
            UPDATE clients
            SET prenom = %s, nom = %s, email = %s, telephone = %s
            WHERE id = %s
            """,
            (prenom, nom, email, telephone, user_id),
        )

    conn.commit()
    cursor.close()
    conn.close()


def delete_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clients WHERE id = %s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()
