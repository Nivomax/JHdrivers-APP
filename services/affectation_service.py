from database import get_connection
from models import (
    RESERVATION_STATUS_CONFIRMED,
    RESERVATION_STATUSES_NOT_ASSIGNABLE,
    normalize_reservation_status,
)


class AffectationError(ValueError):
    pass


def remove_affectation(reservation_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM affectations WHERE reservation_id = %s", (reservation_id,))

    conn.commit()
    cursor.close()
    conn.close()


def assign_chauffeur(reservation_id, chauffeur_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT statut, date_course, heure_course
        FROM reservations
        WHERE id = %s
        """,
        (reservation_id,),
    )
    reservation = cursor.fetchone()
    if reservation is None:
        cursor.close()
        conn.close()
        raise AffectationError("Cette réservation n'existe plus.")

    statut, date_course, heure_course = reservation
    statut = normalize_reservation_status(statut)
    if statut in RESERVATION_STATUSES_NOT_ASSIGNABLE:
        cursor.close()
        conn.close()
        raise AffectationError(
            "Impossible d'affecter une réservation annulée ou terminée."
        )

    cursor.execute("SELECT id FROM chauffeurs WHERE id = %s", (chauffeur_id,))
    chauffeur = cursor.fetchone()
    if chauffeur is None:
        cursor.close()
        conn.close()
        raise AffectationError("Ce chauffeur n'existe plus.")

    cursor.execute(
        """
        SELECT 1
        FROM affectations a
        JOIN reservations r ON r.id = a.reservation_id
        WHERE a.chauffeur_id = %s
          AND a.reservation_id <> %s
          AND r.date_course = %s
          AND r.heure_course = %s
          AND LOWER(r.statut) NOT LIKE 'annul%'
          AND LOWER(r.statut) NOT LIKE 'termin%'
        LIMIT 1
        """,
        (
            chauffeur_id,
            reservation_id,
            date_course,
            heure_course,
        ),
    )
    if cursor.fetchone():
        cursor.close()
        conn.close()
        raise AffectationError("Ce chauffeur a déjà une course sur ce créneau.")

    cursor.execute("DELETE FROM affectations WHERE reservation_id = %s", (reservation_id,))
    cursor.execute(
        """
        INSERT INTO affectations (reservation_id, chauffeur_id)
        VALUES (%s, %s)
        """,
        (reservation_id, chauffeur_id),
    )
    cursor.execute(
        """
        UPDATE reservations
        SET statut = %s
        WHERE id = %s
        """,
        (RESERVATION_STATUS_CONFIRMED, reservation_id),
    )

    conn.commit()
    cursor.close()
    conn.close()
