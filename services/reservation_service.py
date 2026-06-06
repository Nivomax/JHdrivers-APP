from database import get_connection
from models import CalendarReservation, Reservation, normalize_reservation_status


def _reservation_from_row(row):
    values = list(row)
    values[7] = normalize_reservation_status(values[7])
    return Reservation(*values)


def _calendar_reservation_from_row(row):
    values = list(row)
    values[4] = normalize_reservation_status(values[4])
    return CalendarReservation(*values)


def get_all_reservations():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            r.id,
            r.nom_client,
            r.telephone,
            r.adresse_depart,
            r.adresse_arrivee,
            r.date_course,
            r.heure_course,
            r.statut,
            COALESCE(c.nom, 'Non affecté') AS chauffeur
        FROM reservations r
        LEFT JOIN affectations a ON r.id = a.reservation_id
        LEFT JOIN chauffeurs c ON a.chauffeur_id = c.id
        ORDER BY r.date_course DESC, r.heure_course DESC
        """
    )
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [_reservation_from_row(row) for row in rows]


def get_reservation_by_id(reservation_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            r.id,
            r.nom_client,
            r.telephone,
            r.adresse_depart,
            r.adresse_arrivee,
            r.date_course,
            r.heure_course,
            r.statut,
            COALESCE(c.nom, 'Non affecté') AS chauffeur
        FROM reservations r
        LEFT JOIN affectations a ON r.id = a.reservation_id
        LEFT JOIN chauffeurs c ON a.chauffeur_id = c.id
        WHERE r.id = %s
        """,
        (reservation_id,),
    )
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return _reservation_from_row(row) if row else None


def get_reservations_between(start_date, end_date):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            r.id,
            r.date_course,
            r.heure_course,
            r.nom_client,
            r.statut,
            COALESCE(c.nom, 'Non affecté') AS chauffeur
        FROM reservations r
        LEFT JOIN affectations a ON r.id = a.reservation_id
        LEFT JOIN chauffeurs c ON a.chauffeur_id = c.id
        WHERE r.date_course BETWEEN %s AND %s
        ORDER BY r.heure_course
        """,
        (start_date, end_date),
    )
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [_calendar_reservation_from_row(row) for row in rows]


def update_reservation_status(reservation_id, new_status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE reservations
        SET statut = %s
        WHERE id = %s
        """,
        (new_status, reservation_id),
    )

    conn.commit()
    cursor.close()
    conn.close()
