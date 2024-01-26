from pydantic import BaseModel, Field
from typing import Optional


class CreateMassiveEnrollmentSchema(BaseModel):
    """
    Structure that controls the type of data for create a massive enrollment

    Attributes:
        student_id (int): Student ID.
        room_id (int): Room Name.
    """

    student_id: Optional[int] = Field(alias="Student ID")
    room_id: int = Field(alias="Room ID")
