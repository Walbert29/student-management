from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from schemas.course import CreateCourseSchema

from models.course import CourseModel


def post_course(db_session: Session, course: CreateCourseSchema) -> CourseModel:
    """
    This function creates a new course in the database.

    Args:
        db_session (Session): SQLAlchemy database session.
        course (CreateCourseSchema): The schema representing the course to be created.

    Returns:
        CourseModel: Instance of the Course model representing the newly created course.
    """
    map_course = jsonable_encoder(course)
    data_to_create = CourseModel(**map_course)
    db_session.add(data_to_create)
    db_session.commit()
    db_session.refresh(data_to_create)

    return data_to_create
