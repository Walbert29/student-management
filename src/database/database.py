import psycopg2

from settings import Settings


def create_connection():
    """
    Function that returns the connection to the database and the cursor.

    Returns:
        db_connection (MySQLConnection): Database connection.
        db_cursor (MySQLCursor): Cursor to execute queries in the database.
    """

    db_connection = psycopg2.connect(
        host=Settings.HOST_DB,
        port=int(Settings.PORT_DB),
        user=Settings.USERNAME_DB,
        password=Settings.USERPASSWORD_DB,
        database=Settings.DB_NAME,
    )

    db_cursor = db_connection.cursor()

    return db_connection, db_cursor
