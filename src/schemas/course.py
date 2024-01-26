from pydantic import BaseModel, Field


class CreateCourseSchema(BaseModel):
    """
    This class represents the schema for creating a course. It extends the BaseModel from Pydantic.

    Attributes:
        name (str): The name of the course.
        description (str): The description of the course.
    """

    name: str = Field()
    description: str = Field()
