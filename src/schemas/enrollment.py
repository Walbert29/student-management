from pydantic import BaseModel, Field
from typing import Union


class CreateMassiveEnrollmentSchema(BaseModel):
    """
    Structure that controls the type of data for create a massive enrollment

    Attributes:
        student_id (int): Student ID.
        room_id (int): Room Name.
    """

    student_id: Union[int, None] = None
    room_id: int = Field(alias="Room ID")
