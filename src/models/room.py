from database.database import Base
from sqlalchemy import ForeignKey, Column, Integer, String


class RoomModel(Base):
    """
    Room Model
    """

    __tablename__ = "rooms"

    __table_args__ = {"schema": "students_mngt"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    group_id = Column(Integer, ForeignKey("students_mngt.groups.id"), nullable=False)
    teacher_id = Column(
        Integer, ForeignKey("students_mngt.teachers.id"), nullable=False
    )
