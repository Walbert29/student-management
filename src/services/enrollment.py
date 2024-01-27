from fastapi import UploadFile, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.orm import Session


from database.database import create_connection

from schemas.guardian import CreateGuardianSchema
from schemas.student import CreateMassiveStudentSchema
from schemas.enrollment import CreateMassiveEnrollmentSchema

from crud.enrollment import (
    create_enrollment,
    get_enrollment_by_ids,
    delete_enrollment,
)
from crud.room import verify_room_exists
from services.guardian import create_guardian
from services.student import create_student, extract_data_from_file

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


def validate_enrollment(
    session: Session,
    validated_enrollment_data: CreateMassiveEnrollmentSchema,
    student_id: int,
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room ID: {validated_enrollment_data.room_id} does not exist",
        )

    verify_available_enrollment = get_enrollment_by_ids(
        db_session=session,
        student_id=student_id,
        room_id=validated_enrollment_data.room_id,
    )

    if verify_available_enrollment:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Student already enrolled in room or group: {validated_enrollment_data.room_id}",
        )

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
                        "Record": enrollment,
                        "Column Error": error.get("loc"),
                        "Error message": error.get("msg"),
                        "Value entered": error.get("input"),
                        "Status": "Failed",
                    }
                )
            continue

        try:
            session = create_connection()

            with session.begin():
                guardian_id = create_guardian(session, validated_guardian_data)
                student_id = create_student(
                    session, validated_student_data, guardian_id
                )

                if validate_enrollment(
                    session=session,
                    validated_enrollment_data=validated_enrollment_data,
                    student_id=student_id,
                ):
                    create_enrollment(session, validated_enrollment_data, student_id)
                    successful_students.append(
                        {
                            student_id_resonse_key: student_id,
                            room_id_resonse_key: validated_enrollment_data.room_id,
                            "Status": "Successful",
                        }
                    )
        except HTTPException as e:
            failed_students.append(
                {
                    student_id_resonse_key: student_id,
                    message_error: e.detail,
                    status_response_key: "Failed",
                }
            )
        except Exception as e:
            failed_students.append(
                {
                    "Student Data": jsonable_encoder(validated_student_data),
                    message_error: e.args,
                    status_response_key: "Failed",
                }
            )

    return JSONResponse(
        status_code=status.HTTP_207_MULTI_STATUS,
        content={
            "Successful users": successful_students,
            "Failed users": failed_students,
        },
    )


def remove_enrollment(enrollment_id: int):
    """
    Removes an enrollment record.

    Args:
        enrollment_id (int): Enrollment ID.

    Returns:
        EnrollmentModel: Enrollment Model

    """
    session = create_connection()

    try:
        enrollment = delete_enrollment(session, enrollment_id)
        if not enrollment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Enrollment with ID {enrollment_id} not found",
            )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Data deleted successfully",
                "data": jsonable_encoder(enrollment),
            },
        )

    finally:
        session.close()
