from fastapi import HTTPException, UploadFile, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.orm import Session
import pandas as pd


from crud.student import (
    create_massive_student,
    update_massive_student,
    get_student_by_email,
    get_student_by_id,
    get_students_by_group_id,
    get_students_by_room_id,
)
from database.database import create_connection
from schemas.guardian import UpdateGuardianSchema
from schemas.student import CreateMassiveStudentSchema, UpdateMassiveStudentSchema
from services.guardian import update_guardian

student_id_resonse_key = "Student ID"
room_id_resonse_key = "Room ID"
message_error = "Error message"
status_response_key = "Status"


def extract_data_from_file(file: UploadFile):
    """
    Extracts data from an Excel file uploaded through FastAPI's UploadFile.

    Args:
        file (UploadFile): Excel file containing enrollment data.

    Returns:
        List[Dict[str, Any]]: List of dictionaries representing records from the Excel file.

    """
    df_file_enrollment = pd.read_excel(file.file)

    file_enrollment = (
        df_file_enrollment.astype(object)
        .where(pd.notnull(df_file_enrollment), None)
        .to_dict(orient="records")
    )

    return file_enrollment


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


def update_student(
    session: Session, validated_student_data: UpdateMassiveStudentSchema
):
    """
    Creates or retrieves a student based on the provided data.

    Args:
        session (Session): SQLAlchemy session.
        validated_student_data (UpdateMassiveStudentSchema): Validated student data.
        guardian_id (int): Guardian ID.

    Returns:
        StudentModel: Student Model.
    """
    get_student = get_student_by_id(session, validated_student_data.id)
    if get_student:
        update_student = update_massive_student(
            db_session=session,
            updated_data=validated_student_data,
            current_student=get_student,
        )
        return update_student
    return get_student


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


def validate_data_update(data_student):
    """
    Validate and transform the provided data for updating a student.

    Args:
        data_student (dict): Dictionary containing data for updating a student.

    Returns:
        tuple: A tuple containing two validated data objects - one for updating guardian information
               and another for updating student information.
    """

    validated_guardian_data = UpdateGuardianSchema(**data_student)
    validated_student_data = UpdateMassiveStudentSchema(**data_student)
    return (
        validated_guardian_data,
        validated_student_data,
    )


def update_data_students(file: UploadFile):
    """
    Update student and guardian data from an Excel file.

    Args:
        file (UploadFile): The Excel file containing data to update.

    Returns:
        JSONResponse: A JSON response containing information about successful and failed updates.
    """
    if not file.filename.endswith(".xlsx"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File extension not supported",
        )

    failed_students = []
    successful_students = []

    file_data_to_update = extract_data_from_file(file)

    for data in file_data_to_update:
        try:
            (
                validated_guardian_data,
                validated_student_data,
            ) = validate_data_update(data)
        except ValidationError as e:
            for error in e.errors():
                failed_students.append(
                    {
                        "Record": data,
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
                guardian_updated = update_guardian(session, validated_guardian_data)

                if guardian_updated is None:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Guardian with ID {validated_guardian_data.id} not found",
                    )

                student_updated = update_student(session, validated_student_data)

                if student_updated is None:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Student with ID {validated_student_data.id} not found",
                    )

                successful_students.append(
                    {
                        student_id_resonse_key: student_updated.id,
                        "message": "Data Updated",
                    }
                )
        except HTTPException as e:
            failed_students.append(
                {
                    student_id_resonse_key: validated_student_data,
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
