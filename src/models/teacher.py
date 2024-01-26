from database.database import Base
from sqlalchemy import Column, Integer, String


class TeacherModel(Base):
    """
    Teacher Model
    """

    __tablename__ = "teachers"

    __table_args__ = {"schema": "students_mngt"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    document_type_id = Column(Integer)
    document_number = Column(Integer)
    country_id = Column(Integer)
