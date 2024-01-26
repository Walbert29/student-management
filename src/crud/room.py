from sqlalchemy.orm import Session

from models.room import RoomModel
from models.group import GroupModel


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
