from pydantic import BaseModel, Field
from typing import Optional


class CreateTeacherSchema(BaseModel):
    """
    This class represents the schema for creating a teacher.

    Attributes:
        first_name (str): The first name of the teacher. It is a required field.
        last_name (str): The last name of the teacher. It is a required field.
        email (str): The email of the teacher. It is a required field.
        document_type_id (Optional[int]): The ID of the teacher's identification type. It is an optional field.
        document_number (Optional[int]): The identification number of the teacher. It is an optional field.
        country_id (Optional[int]): The ID of the teacher's country. It is an optional field.
    """

    first_name: str = Field()
    last_name: str = Field()
    email: str = Field()
    document_type_id: Optional[int] = Field()
    document_number: Optional[int] = Field()
    country_id: Optional[int] = Field()
