from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from models.room import RoomModel
from models.group import GroupModel

from schemas.room import CreateRoomSchema

# GET


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


def verify_room_exists(db_session: Session, room_id: int) -> RoomModel:
    """
    This function verifies if a room with a given ID exists in the database.

    Args:
        db_session (Session): The session object representing the database connection.
        room_id (int): The ID of the room to be verified.

    Returns:
        EnrollmentModel: The model object representing the room if it exists, None otherwise.
    """

    query = db_session.query(RoomModel).filter(RoomModel.id == room_id).first()

    return query


def get_room_by_group_id(db_session: Session, group_id: int) -> RoomModel:
    """
    Retrieve a room from the database based on its group ID.

    Args:
        db_session (Session): SQLAlchemy database session.
        group_id (int): The ID of the group to be retrieved.

    Returns:
        RoomModel: The room with the specified group ID.
    """

    return db_session.query(RoomModel).filter(RoomModel.group_id == group_id).first()


# POST


def post_room(db_session: Session, room: CreateRoomSchema) -> RoomModel:
    """
    Create a new room in the database.

    Args:
        db_session (Session): SQLAlchemy database session.
        room (CreateRoomSchema): Room data to be created, adhering to the schema.

    Returns:
        RoomModel: The new room created.
    """

    map_course = jsonable_encoder(room)
    data_to_create = RoomModel(**map_course)
    db_session.add(data_to_create)
    db_session.commit()
    db_session.refresh(data_to_create)

    return data_to_create


# DELETE


def delete_room(db_session: Session, room_id: int) -> RoomModel:
    """
    Delete a room in the database.

    Args:
        db_session (Session): SQLAlchemy database session.
        room_id (int): Room ID to be deleted.

    Returns:
        RoomModel: The new room created.
    """

    room = db_session.query(RoomModel).filter(RoomModel.id == room_id).first()

    if room is not None:
        db_session.delete(room)
        db_session.commit()

    return room
