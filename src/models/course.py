from database.database import Base
from sqlalchemy import Column, Integer, String, Text


class CourseModel(Base):
    """
    Course Model
    """

    __tablename__ = "courses"

    __table_args__ = {"schema": "students_mngt"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
