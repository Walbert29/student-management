from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
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
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "Data created successfully",
                "data": jsonable_encoder(
                    post_course(db_session=session, course=course)
                ),
            },
        )

    finally:
        session.close()
