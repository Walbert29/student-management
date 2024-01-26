from database.database import Base
from sqlalchemy import ForeignKey, Column, Integer, String


class StudentModel(Base):
    """
    Student Model
    """

    __tablename__ = "students"

    __table_args__ = {"schema": "students_mngt"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    guardian_id = Column(
        Integer, ForeignKey("students_mngt.guardians.id"), nullable=False
    )
