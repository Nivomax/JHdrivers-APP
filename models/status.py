import unicodedata


RESERVATION_STATUS_PENDING = "En attente"
RESERVATION_STATUS_CONFIRMED = "Confirm\u00e9e"
RESERVATION_STATUS_COMPLETED = "Termin\u00e9e"
RESERVATION_STATUS_CANCELLED = "Annul\u00e9e"

RESERVATION_STATUSES = [
    RESERVATION_STATUS_PENDING,
    RESERVATION_STATUS_CONFIRMED,
    RESERVATION_STATUS_COMPLETED,
    RESERVATION_STATUS_CANCELLED,
]

RESERVATION_STATUSES_NOT_ASSIGNABLE = (
    RESERVATION_STATUS_CANCELLED,
    RESERVATION_STATUS_COMPLETED,
)


def normalize_reservation_status(status):
    value = str(status or "").strip()
    normalized = "".join(
        character
        for character in unicodedata.normalize("NFD", value.lower())
        if unicodedata.category(character) != "Mn"
    )

    if normalized == "en attente":
        return RESERVATION_STATUS_PENDING
    if normalized.startswith("confirm"):
        return RESERVATION_STATUS_CONFIRMED
    if normalized.startswith("termin"):
        return RESERVATION_STATUS_COMPLETED
    if normalized.startswith("annul"):
        return RESERVATION_STATUS_CANCELLED
    return value
