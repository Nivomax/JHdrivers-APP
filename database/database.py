import os

import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("JHDRIVERS_DB_HOST", "localhost"),
        user=os.getenv("JHDRIVERS_DB_USER", "root"),
        password=os.getenv("JHDRIVERS_DB_PASSWORD", ""),
        database=os.getenv("JHDRIVERS_DB_NAME", "jhdrivers-e6"),
    )
