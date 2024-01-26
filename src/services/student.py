from sqlalchemy.orm import Session


from crud.student import (
    create_massive_student,
    get_student_by_email,
    get_students_by_group_id,
    get_students_by_room_id,
)
from database.database import create_connection
from schemas.student import CreateMassiveStudentSchema


def create_student(
    session: Session,
    validated_student_data: CreateMassiveStudentSchema,
    guardian_id: int,
):
    """
    Creates or retrieves a student based on the provided data.

    Args:
        session (Session): SQLAlchemy session.
        validated_student_data (CreateMassiveStudentSchema): Validated student data.
        guardian_id (int): Guardian ID.

    Returns:
        int: Student ID.
    """
    get_student = get_student_by_email(session, validated_student_data.email)
    if not get_student:
        validated_student_data.guardian_id = guardian_id
        create_student = create_massive_student(
            db_session=session, student=validated_student_data
        )
        return create_student.id
    return get_student.id


def obtain_students_by_group(group_id: int):
    """
    Retrieves a list of students based on the provided group ID.

    Args:
        group_id (int): Group ID.

    Returns:
        list: List of students.
    """
    try:
        session = create_connection()
        return get_students_by_group_id(db_session=session, group_id=group_id)
    finally:
        session.close()


def obtain_students_by_room(room_id: int):
    """
    Retrieves a list of students based on the provided Room ID.

    Args:
        room_id (int): Room ID.

    Returns:
        list: List of students.
    """
    try:
        session = create_connection()
        return get_students_by_room_id(db_session=session, room_id=room_id)
    finally:
        session.close()
