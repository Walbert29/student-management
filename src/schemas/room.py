from pydantic import BaseModel, Field


class CreateRoomSchema(BaseModel):
    """
    This class represents the schema for creating a room.

    Attributes:
        name (str): The name of the room. It is a required field.
        group_id (int): Id of the group to which you belong. It is an optional field.
        teacher_id (int): Id of the assigned teacher. It is an optional field.
    """

    name: str = Field()
    group_id: int = Field()
    teacher_id: int = Field()
