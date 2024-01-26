from sqlalchemy.orm import Session

from models.group import GroupModel
from models.course import CourseModel


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
