from pydantic import BaseModel, Field
from typing import Optional


class CreateGuardianSchema(BaseModel):
    """
    This class represents the schema for creating a guardian.

    Attributes:
        first_name (str): The first name of the guardian. It is a required field.
        last_name (str): The last name of the guardian. It is a required field.
        email (str): The email of the guardian. It is a required field.
        document_type_id (Optional[int]): The ID of the guardian's identification type. It is an optional field.
        document_number (Optional[int]): The identification number of the guardian. It is an optional field.
        country_id (Optional[int]): The ID of the guardian's country. It is an optional field.
    """

    first_name: str = Field(alias="Guardian First Name")
    last_name: str = Field(alias="Guardian Last Name")
    email: str = Field(alias="Guardian Email")
    document_type_id: Optional[int] = Field(alias="Guardian Identification Type (ID)")
    document_number: Optional[int] = Field(alias="Guardian Identification Number")
    country_id: Optional[int] = Field(alias="Guardian Country (Id)")
