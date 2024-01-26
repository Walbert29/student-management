from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from models.group import GroupModel
from models.course import CourseModel

from schemas.group import CreateGroupSchema

# GET


def list_groups_with_courses(db_session: Session):
    """
    Retrieve a list of groups with respectives courses from the database.

    Args:
        db_session (Session): SQLAlchemy database session.

    Returns:
        List[GroupModel]: List of groups with respectives courses.
    """

    query = (
        db_session.query(GroupModel, CourseModel)
        .join(GroupModel, GroupModel.course_id == CourseModel.id)
        .all()
    )

    return query


def get_group_by_id(db_session: Session, group_id: int) -> GroupModel:
    """
    Retrieve a group from the database based on its ID.

    Args:
        db_session (Session): SQLAlchemy database session.
        group_id (int): The ID of the group to be retrieved.

    Returns:
        GroupModel: The group with the specified ID.
    """

    return db_session.query(GroupModel).filter(GroupModel.id == group_id).first()


# POST


def post_group(db_session: Session, group: CreateGroupSchema) -> GroupModel:
    """
    Create a new group in the database.

    Args:
        db_session (Session): SQLAlchemy database session.
        group (CreateGroupSchema): The group data to be created, adhering to the schema.

    Returns:
        GroupModel: The newly created group.
    """

    map_course = jsonable_encoder(group)
    data_to_create = GroupModel(**map_course)
    db_session.add(data_to_create)
    db_session.commit()
    db_session.refresh(data_to_create)

    return data_to_create
