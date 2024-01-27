from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from schemas.course import CreateCourseSchema

from models.course import CourseModel

# GET


def validate_exist_course(db_session: Session, course_id: int):
    """
    Validate the existence of a course in the database.

    Args:
        db_session (Session): SQLAlchemy database session.
        course_id (int): The ID of the course to be validated.

    Returns:
        CourseModel: The course if it exists, otherwise None
    """

    return db_session.query(CourseModel).filter(CourseModel.id == course_id).first()


# POST


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


# DELETE


def delete_course(db_session: Session, course_id: int) -> CourseModel:
    """
    Delete a course of the database.

    Args:
        db_session (Session): SQLAlchemy database session.
        course_id (int): The ID of the course to be deleted.

    Returns:
        CourseModel: The course if it exists, otherwise None
    """

    course = db_session.query(CourseModel).filter(CourseModel.id == course_id).first()

    if course is not None:
        db_session.delete(course)
        db_session.commit()

    return course
