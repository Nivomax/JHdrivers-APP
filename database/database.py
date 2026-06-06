import mysql.connector


def get_connection():
    conn = mysql.connector.connect(
        host="mysql-jhdrivers.alwaysdata.net",
        port=3306,
        user="jhdrivers_max",
        password="Maxime94400",
        database="jhdrivers_e6",
    )
    return conn
