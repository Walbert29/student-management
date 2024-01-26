from database.database import Base
from sqlalchemy import Column, Integer, ForeignKey


class EnrollmentModel(Base):
    """
    Enrollment Model
    """

    __tablename__ = "enrollments"

    __table_args__ = {"schema": "students_mngt"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer)
    room_id = Column(Integer, ForeignKey("students_mngt.rooms.id"), nullable=False)
