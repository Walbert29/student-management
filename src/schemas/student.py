from pydantic import BaseModel, Field
from typing import Union


class CreateMassiveStudentSchema(BaseModel):
    """
    This class represents the schema for creating a student in a massive way. It extends the BaseModel from Pydantic.

    Attributes:
        first_name (str): The first name of the student. It is a required field.
        last_name (str): The last name of the student. It is a required field.
        email (str): The email of the student. It is a required field.
        guardian_id (Optional[int]): The ID of the student's guardian. It is an optional field.
    """

    first_name: str = Field(alias="Student Frist name")
    last_name: str = Field(alias="Student Last Name")
    email: str = Field(alias="Student Email")
    guardian_id: Union[int, None] = None


class UpdateMassiveStudentSchema(CreateMassiveStudentSchema):
    """
    This class represents the schema for updating a student in a massive way. It extends the BaseModel from Pydantic.

    Attributes:
        guardian_id (int): The ID of the student's guardian. It is a required field.
    """

    id: int = Field(alias="Student ID")
    guardian_id: int = Field(alias="Guardian ID")
