from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session


from crud.student import get_student_by_email
from models.student import StudentModel
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
        student_data_to_create = jsonable_encoder(
            validated_student_data, by_alias=False
        )
        create_student = StudentModel(**student_data_to_create)
        session.add(create_student)
        session.flush()
        return create_student.id
    return get_student.id
