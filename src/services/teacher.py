from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import status

from schemas.teacher import CreateTeacherSchema

from crud.teacher import get_teacher_by_email, post_teacher
from database.database import create_connection


def create_teacher(teacher: CreateTeacherSchema):
    """
    Create a new teacher in the database.

    Args:
        teacher (CreateTeacherSchema): The teacher data to be created, adhering to the schema.

    Returns:
        Union[JSONResponse, TeacherModel]: A JSONResponse if the associated teacher is found,
        otherwise the newly created teacher.
    """
    try:
        session = create_connection()
        exist_course = get_teacher_by_email(db_session=session, email=teacher.email)
        if exist_course:
            return JSONResponse(
                content={
                    "message": f"Teacher with email: {teacher.email} already exists"
                },
                status_code=status.HTTP_409_CONFLICT,
            )
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "Data created successfully",
                "data": jsonable_encoder(
                    post_teacher(db_session=session, teacher=teacher)
                ),
            },
        )

    finally:
        session.close()
