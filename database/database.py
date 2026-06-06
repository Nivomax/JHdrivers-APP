import os
from pathlib import Path

import mysql.connector


_SCHEMA_INITIALIZED = False


def _ensure_schema(conn):
    global _SCHEMA_INITIALIZED

    if _SCHEMA_INITIALIZED:
        return

    schema_path = Path(__file__).with_name("schema.sql")
    sql_script = schema_path.read_text(encoding="utf-8")

    cursor = conn.cursor()
    try:
        # schema.sql does not contain procedures/triggers, so a simple split is enough.
        for statement in sql_script.split(";"):
            stmt = statement.strip()
            if stmt:
                cursor.execute(stmt)
        conn.commit()
        _SCHEMA_INITIALIZED = True
    finally:
        cursor.close()


def get_connection():
    host = os.getenv("DB_HOST") or os.getenv("JHDRIVERS_DB_HOST") or "mysql-jhdrivers.alwaysdata.net"
    port = int(os.getenv("DB_PORT") or os.getenv("JHDRIVERS_DB_PORT") or "3306")
    database = os.getenv("DB_NAME") or os.getenv("JHDRIVERS_DB_NAME") or "jhdrivers_e6"
    user = os.getenv("DB_USER") or os.getenv("JHDRIVERS_DB_USER") or "jhdrivers_max"
    password = (
        os.getenv("DB_PASS")
        or os.getenv("DB_PASSWORD")
        or os.getenv("JHDRIVERS_DB_PASSWORD")
        or "Maxime94400"
    )

    conn = mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
    )
    _ensure_schema(conn)
    return conn
