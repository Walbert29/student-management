from sqlalchemy.orm import Session
from models.enrollment import EnrollmentModel
from models.group import GroupModel
from models.room import RoomModel

from models.student import StudentModel


def get_student_by_email(db_sesion: Session, email: str) -> StudentModel:
    """
    Retrieve a student from the database based on their email address.

    Args:
        db_session (Session): SQLAlchemy database session.
        email (str): Email address of the student being searched.

    Returns:
        StudentModel: Instance of the Student model corresponding to the provided email,
                      or None if no student is found with that email.
    """

    query = db_sesion.query(StudentModel).filter(StudentModel.email == email).first()

    return query


def get_students_by_group_id(db_session: Session, group_id: int) -> list[StudentModel]:
    """
    Retrieve a student from the database based on their group ID assigned.

    Args:
        db_session (Session): SQLAlchemy database session.
        group_id (int): Group ID of the student being searched.

    Returns:
        List[StudentModel]: List of instances of the Student model corresponding to the provided group ID
    """

    query = (
        db_session.query(StudentModel)
        .join(EnrollmentModel, EnrollmentModel.student_id == StudentModel.id)
        .join(RoomModel, RoomModel.id == EnrollmentModel.room_id)
        .join(GroupModel, GroupModel.id == RoomModel.group_id)
        .filter(GroupModel.id == group_id)
        .all()
    )

    return query
