from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import or_

from models.enrollment import EnrollmentModel
from models.room import RoomModel
from models.group import GroupModel
from schemas.enrollment import CreateMassiveEnrollmentSchema

# GET


def get_enrollment_by_ids(
    db_session: Session, student_id: int, room_id: int
) -> EnrollmentModel:
    """
    This function retrieves an enrollment record from the database based on the student's ID and room ID.

    Args:
        db_session (Session): SQLAlchemy database session.
        student_id (int): ID of the student being searched.
        room_id (int): ID of the room being searched.

    Returns:
        EnrollmentModel: Instance of the Enrollment model corresponding to the provided student ID and room ID,
                         or None if no enrollment is found with those IDs.
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


def verify_room_exists(db_session: Session, room_id: int) -> EnrollmentModel:
    """
    This function verifies if a room with a given ID exists in the database.

    Args:
        db_session (Session): The session object representing the database connection.
        room_id (int): The ID of the room to be verified.

    Returns:
        EnrollmentModel: The model object representing the room if it exists, None otherwise.
    """

    query = db_session.query(RoomModel).filter(RoomModel.id == room_id).first()

    return query


# POST


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
