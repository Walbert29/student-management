from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from models.course import CourseModel
from models.group import GroupModel
from schemas.group import CreateGroupSchema

# GET
print("Hello, World!")

print("Hello, World!")


def list_groups_with_courses(db_session: Session):
    """Retrieve a list of groups with respectives courses from the database.

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
    """Retrieve a group from the database based on its ID.

    Args:
        db_session (Session): SQLAlchemy database session.
        group_id (int): The ID of the group to be retrieved.

    Returns:
        GroupModel: The group with the specified ID.
    """

    return db_session.query(GroupModel).filter(GroupModel.id == group_id).first()


def get_group_by_course_id(db_session: Session, course_id: int) -> GroupModel:
    """Retrieve a group from the database based on its course ID.

    Args:
        db_session (Session): SQLAlchemy database session.
        course_id (int): The ID of the course to be retrieved.

    Returns:
        GroupModel: The group with the specified course ID.
    """

    return (
        db_session.query(GroupModel).filter(GroupModel.course_id == course_id).first()
    )


# POST


def post_group(db_session: Session, group: CreateGroupSchema) -> GroupModel:
    """Create a new group in the database.

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


# DELETE


def delete_group(db_session: Session, group_id: int) -> GroupModel:
    """Delete a group of the database.

    Args:
        db_session (Session): SQLAlchemy database session.
        group_id (int): The ID of the group to be deleted.

    Returns:
        GroupModel: The group if it exists, otherwise None GroupModel: The group if it exists, otherwise None GroupModel: The group if it exists, otherwise None
    """

    group = db_session.query(GroupModel).filter(GroupModel.id == group_id).first()

    db_session.delete(group)
    db_session.commit()

    return group
