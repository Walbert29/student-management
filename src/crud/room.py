from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from models.room import RoomModel
from models.group import GroupModel

from schemas.room import CreateRoomSchema


def list_rooms_with_groups(db_session: Session):
    """
    Retrieve a list of rooms with respectives groups from the database.

    Args:
        db_session (Session): SQLAlchemy database session.

    Returns:
        List: List of rooms with respectives groups.
    """

    query = (
        db_session.query(RoomModel, GroupModel)
        .join(RoomModel, RoomModel.group_id == GroupModel.id)
        .all()
    )

    return query


def post_room(db_session: Session, room: CreateRoomSchema) -> RoomModel:
    """
    Create a new room in the database.

    Args:
        db_session (Session): SQLAlchemy database session.
        room (CreateRoomSchema): Room data to be created, adhering to the schema.

    Returns:
        TeacherModel: The new room created.
    """

    map_course = jsonable_encoder(room)
    data_to_create = RoomModel(**map_course)
    db_session.add(data_to_create)
    db_session.commit()
    db_session.refresh(data_to_create)

    return data_to_create
