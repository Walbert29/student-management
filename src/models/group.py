from database.database import Base
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey


class GroupModel(Base):
    """
    Group Model
    """

    __tablename__ = "groups"

    __table_args__ = {"schema": "students_mngt"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    start_time = Column(TIMESTAMP(timezone=False))
    end_time = Column(TIMESTAMP(timezone=False))
    course_id = Column(Integer, ForeignKey("students_mngt.courses.id"), nullable=False)
