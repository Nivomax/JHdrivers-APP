from database import get_connection


def get_stats():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM reservations")
    total = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM reservations WHERE LOWER(statut) = 'en attente'",
    )
    attente = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM reservations WHERE LOWER(statut) LIKE 'confirm%'",
    )
    confirmees = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM reservations WHERE LOWER(statut) LIKE 'termin%'",
    )
    terminees = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return {
        "total": total,
        "attente": attente,
        "confirmees": confirmees,
        "terminees": terminees,
    }
