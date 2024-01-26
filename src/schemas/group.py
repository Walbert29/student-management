from pydantic import BaseModel, Field
from datetime import datetime


class CreateGroupSchema(BaseModel):
    """
    Schema for creating a new group.

    Attributes:
        name (str): The name of the group.
        description (str): A description of the group.
        start_time (datetime): The start time of the group (default is the current date and time).
        end_time (datetime): The end time of the group (default is the current date and time).
        course_id (int): The ID of the course to which the group belongs.
    """

    name: str = Field()
    description: str = Field()
    start_time: datetime = Field(default=datetime.now)
    end_time: datetime = Field(default=datetime.now)
    course_id: int = Field()
