from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from crud.course import delete_course, post_course, validate_exist_course
from crud.group import get_group_by_course_id

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


def remove_course(course_id: int):
    """
    Removes a course record.

    Args:
        course_id (int): Course ID.

    Returns:
        CourseModel: Course Model

    """
    try:
        session = create_connection()

        course = validate_exist_course(db_session=session, course_id=course_id)
        if not course:
            return JSONResponse(
                content={"message": f"Course with ID: {course_id} not found"},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        verify_group_associated = get_group_by_course_id(
            db_session=session, course_id=course_id
        )
        if verify_group_associated:
            return JSONResponse(
                content={
                    "message": f"Course with ID: {course_id} is associated with a group"
                },
                status_code=status.HTTP_409_CONFLICT,
            )

        delete_course(db_session=session, course_id=course_id)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Data deleted successfully",
                "data": jsonable_encoder(course),
            },
        )

    finally:
        session.close()
