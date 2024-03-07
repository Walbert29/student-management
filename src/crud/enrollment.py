"""
Okay
"""
from fastapi.encoders import jsonable_encoder
from sqlalchemy import or_
from sqlalchemy.orm import Session

from models.enrollment import EnrollmentModel
from models.group import GroupModel
from models.room import RoomModel
from schemas.enrollment import CreateMassiveEnrollmentSchema

# GET


def get_enrollment_by_ids(
    db_session: Session, student_id: int, room_id: int
) -> EnrollmentModel:
    """
    This function retrieves an enrollment record from the database based
    on the student's ID and room ID.

    Args:
        db_session (Session): SQLAlchemy database session.
        student_id (int): ID of the student being searched.
        room_id (int): ID of the room being searched.

    Returns:
        EnrollmentModel: Instance of the Enrollment model corresponding to the provided student ID
        and room ID or None if no enrollment is found with those IDs.
    """

    query = (
        db_session.query(EnrollmentModel, RoomModel, GroupModel)
        .join(RoomModel, EnrollmentModel.room_id == RoomModel.id)
        .join(GroupModel, RoomModel.group_id == GroupModel.id)
        .filter(
            EnrollmentModel.student_id == student_id,
            or_(
                (EnrollmentModel.room_id == room_id),
                (
                    GroupModel.id.in_(
                        db_session.query(RoomModel.group_id)
                        .join(EnrollmentModel, EnrollmentModel.room_id == RoomModel.id)
                        .join(GroupModel, RoomModel.group_id == GroupModel.id)
                        .filter(
                            EnrollmentModel.student_id == student_id,
                            EnrollmentModel.room_id == room_id,
                        )
                    )
                ),
            ),
        )
        .first()
    )

    return query


def get_enrollment_by_room_id(room_id: int, db_session: Session) -> EnrollmentModel:
    """
    This function retrieves an enrollment record from the database based on the room ID.

    Args:
        db_session (Session): SQLAlchemy database session.
        room_id (int): ID of the room being searched.

    Returns:
        EnrollmentModel: Instance of the Enrollment model corresponding to the provided room ID,
                         or None if no enrollment is found with that ID.
    """

    query = (
        db_session.query(EnrollmentModel, RoomModel)
        .join(RoomModel, EnrollmentModel.room_id == RoomModel.id)
        .filter(EnrollmentModel.room_id == room_id)
        .first()
    )

    return query


# POST


def create_enrollment(
    session: Session,
    validated_enrollment_data: CreateMassiveEnrollmentSchema,
    student_id: int,
) -> bool:
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


# DELETE


def delete_enrollment(db_session: Session, enrollment_id: int) -> EnrollmentModel:
    """
    Delete a enrollment of the database.

    Args:
        db_session (Session): SQLAlchemy database session.
        enrollment_id (int): The ID of the enrollment to be deleted.

    Returns:
        EnrollmentModel: The enrollment if it exists, otherwise None
    """

    enrollment = (
        db_session.query(EnrollmentModel)
        .filter(EnrollmentModel.id == enrollment_id)
        .first()
    )

    if enrollment is not None:
        db_session.delete(enrollment)
        db_session.commit()

    return enrollment
