from crud.course import post_course
from database.database import create_connection

from schemas.course import CreateCourseSchema


def create_course(course: CreateCourseSchema):
    """
    Create a new course in the database.

    Args:
        course (CreateCourseSchema): The course data to be created, adhering to the schema.

    Returns:
        CreateCourseSchema: JSON CreateCourseSchema

    """
    try:
        session = create_connection()
        return post_course(db_session=session, course=course)

    finally:
        session.close()
