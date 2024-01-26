import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings import Settings

Base = declarative_base()


def create_connection():
    """
    Establishes a connection to the PostgreSQL database and returns a session object.

    Returns:
        session (Session): A SQLAlchemy database session.
    """

    # Create an SQLAlchemy engine using the provided database connection settings.
    engine = create_engine(
        sqlalchemy.engine.url.URL(
            drivername="postgresql",
            username=Settings.USERNAME_DB,
            password=Settings.USERPASSWORD_DB,
            host=Settings.HOST_DB,
            port=int(Settings.PORT_DB),
            database=Settings.DB_NAME,
            query={},
        ),
    )

    # Create a session
    session_maker = sessionmaker(bind=engine)
    session = session_maker()
    return session
