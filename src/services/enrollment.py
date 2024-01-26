from fastapi import UploadFile, status, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError
from sqlalchemy.orm import Session


from database.database import create_connection

from models.enrollment import EnrollmentModel

from schemas.guardian import CreateGuardianSchema
from schemas.student import CreateMassiveStudentSchema
from schemas.enrollment import CreateMassiveEnrollmentSchema

from crud.enrollment import verify_room_exists, get_enrollment_by_ids
from services.guardian import create_guardian
from services.student import create_student

student_id_resonse_key = "Student ID"
room_id_resonse_key = "Room ID"
message_error = "Error message"
status_response_key = "Status"


def validate_data(enrollment):
    """
    Validates guardian, student, and enrollment data from a given enrollment record.

    Args:
        enrollment (dict): Enrollment record to be validated.

    Returns:
        Tuple[CreateGuardianSchema, CreateMassiveStudentSchema, CreateMassiveEnrollmentSchema]: Validated data.

    """
    validated_guardian_data = CreateGuardianSchema(**enrollment)
    validated_student_data = CreateMassiveStudentSchema(**enrollment)
    validated_enrollment_data = CreateMassiveEnrollmentSchema(**enrollment)
    return (
        validated_guardian_data,
        validated_student_data,
        validated_enrollment_data,
    )


def extract_data_from_file(file: UploadFile):
    """
    Extracts data from an Excel file uploaded through FastAPI's UploadFile.

    Args:
        file (UploadFile): Excel file containing enrollment data.

    Returns:
        List[Dict[str, Any]]: List of dictionaries representing records from the Excel file.

    Raises:
        pd.errors.EmptyDataError: If the Excel file is empty or contains no data.
    """
    df_file_enrollment = pd.read_excel(file.file)

    file_enrollment = (
        df_file_enrollment.astype(object)
        .where(pd.notnull(df_file_enrollment), None)
        .to_dict(orient="records")
    )

    return file_enrollment


def validate_enrollment(
    session: Session,
    validated_enrollment_data: CreateMassiveEnrollmentSchema,
    student_id: int,
    failed_students: list,
):
    """
    Validates enrollment data and checks for room and enrollment availability.

    Args:
        session (Session): SQLAlchemy session.
        validated_enrollment_data (CreateMassiveEnrollmentSchema): Validated enrollment data.
        student_id (int): Student ID.

    Returns:
        bool: True if validation passes.

    """
    verify_room = verify_room_exists(
        db_session=session, room_id=validated_enrollment_data.room_id
    )
    if not verify_room:
        failed_students.append(
            {
                student_id_resonse_key: student_id,
                message_error: f"Room ID: {validated_enrollment_data.room_id} does not exist",
            }
        )
        return False

    verify_available_enrollment = get_enrollment_by_ids(
        db_session=session,
        student_id=student_id,
        room_id=validated_enrollment_data.room_id,
    )

    if verify_available_enrollment:
        failed_students.append(
            {
                student_id_resonse_key: student_id,
                message_error: f"Student already enrolled in room or group: {validated_enrollment_data.room_id}",
            }
        )
        return False

    return True


def create_enrollment(
    session: Session,
    validated_enrollment_data: CreateMassiveEnrollmentSchema,
    student_id: int,
):
    """
    Creates an enrollment record.

    Args:
        session (Session): SQLAlchemy session.
        validated_enrollment_data (CreateMassiveEnrollmentSchema): Validated enrollment data.
        student_id (int): Student ID.

    Returns:
        bool: True if enrollment creation is successful.
    """
    validated_enrollment_data.student_id = student_id
    enrollment_data_to_create = jsonable_encoder(
        validated_enrollment_data, by_alias=False
    )
    create_enrollment = EnrollmentModel(**enrollment_data_to_create)
    session.add(create_enrollment)
    session.commit()
    return True


def create_enrollment_students(file: UploadFile):
    """
    Process a file containing enrollment data and create guardian, student, and enrollment records.

    Args:
        file (UploadFile): Excel file containing enrollment data.

    Returns:
        JSONResponse: Response with details of successful and failed enrollments.
    """
    if not file.filename.endswith(".xlsx"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File extension not supported",
        )

    failed_students = []
    successful_students = []

    file_enrollment = extract_data_from_file(file)

    for enrollment in file_enrollment:
        guardian_id, student_id = None, None
        try:
            (
                validated_guardian_data,
                validated_student_data,
                validated_enrollment_data,
            ) = validate_data(enrollment)
        except ValidationError as e:
            for error in e.errors():
                failed_students.append(
                    {
                        "Column Error": error.get("loc"),
                        "Error message": error.get("msg"),
                        "Value entered": error.get("input"),
                    }
                )
            continue

        session = create_connection()

        with session.begin():
            guardian_id = create_guardian(session, validated_guardian_data)
            student_id = create_student(session, validated_student_data, guardian_id)

            if validate_enrollment(
                session=session,
                validated_enrollment_data=validated_enrollment_data,
                student_id=student_id,
                failed_students=failed_students,
            ):
                create_enrollment(session, validated_enrollment_data, student_id)
                successful_students.append(
                    {
                        student_id_resonse_key: student_id,
                        room_id_resonse_key: validated_enrollment_data.room_id,
                        "status": "Successful",
                    }
                )

    return JSONResponse(
        status_code=status.HTTP_207_MULTI_STATUS,
        content={
            "Successful users": successful_students,
            "Failed users": failed_students,
        },
    )