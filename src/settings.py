import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """
    This class holds the configuration settings for the application.
    It includes the database connection details such as host, port, database name,
    username, and password.

    Attributes:
        HOST_DB (str): The host address of the database server.
        PORT_DB (str): The port number of the database server.
        DB_NAME (str): The name of the database.
        USERNAME_DB (str): The username for accessing the database.
        USERPASSWORD_DB (str): The password for accessing the database.
    """

    HOST_DB = os.getenv("HOST_DB")
    PORT_DB = os.getenv("PORT_DB")
    DB_NAME = os.getenv("DB_NAME")
    USERNAME_DB = os.getenv("USERNAME_DB")
    USERPASSWORD_DB = os.getenv("USERPASSWORD_DB")
