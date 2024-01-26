from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from models.enrollment import EnrollmentModel
from models.group import GroupModel
from models.room import RoomModel

from models.student import StudentModel
from schemas.student import CreateMassiveStudentSchema, UpdateMassiveStudentSchema

# GET


def get_student_by_email(db_session: Session, email: str) -> StudentModel:
    """
    Retrieve a student from the database based on their email address.

    Args:
        db_session (Session): SQLAlchemy database session.
        email (str): Email address of the student being searched.

    Returns:
        StudentModel: Instance of the Student model corresponding to the provided email,
                      or None if no student is found with that email.
    """

    query = db_session.query(StudentModel).filter(StudentModel.email == email).first()

    return query


def get_student_by_id(db_session: Session, student_id: int) -> StudentModel:
    """
    Retrieve a student from the database based on their id.

    Args:
        db_session (Session): SQLAlchemy database session.
        student_id (int): Id of the student being searched.

    Returns:
        StudentModel: Instance of the Student model corresponding to the provided id,
                      or None if no student is found with that id.
    """

    query = db_session.query(StudentModel).filter(StudentModel.id == student_id).first()

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


def get_students_by_room_id(db_session: Session, room_id: int) -> list[StudentModel]:
    """
    Retrieve a student from the database based on their room ID assigned.

    Args:
        db_session (Session): SQLAlchemy database session.
        room_id (int): Room ID of the student being searched.

    Returns:
        List[StudentModel]: List of instances of the Student model corresponding to the provided Room ID
    """

    query = (
        db_session.query(StudentModel)
        .join(EnrollmentModel, EnrollmentModel.student_id == StudentModel.id)
        .join(RoomModel, RoomModel.id == EnrollmentModel.room_id)
        .filter(RoomModel.id == room_id)
        .all()
    )

    return query


# POST


def create_massive_student(
    db_session: Session, student: CreateMassiveStudentSchema
) -> StudentModel:
    """
    Create a new student in the database.

    Args:
        db_session (Session): SQLAlchemy database session.
        student (CreateMassiveStudentSchema): Student to be created.

    Returns:
        StudentModel: Instance of the Student model corresponding to the newly created student.
    """

    student_data_to_create = jsonable_encoder(student, by_alias=False)
    create_student = StudentModel(**student_data_to_create)
    db_session.add(create_student)
    db_session.flush()

    return create_student


# PUT


def update_massive_student(
    db_session: Session,
    updated_data: UpdateMassiveStudentSchema,
    current_student: StudentModel,
) -> StudentModel:
    """
    Update student in the database.

    Args:
        db_session (Session): SQLAlchemy database session.
        student (UpdateMassiveStudentSchema): Student to be updated.

    Returns:
        StudentModel: Instance of the Student model corresponding to the newly created student.
    """

    for field, value in jsonable_encoder(updated_data, by_alias=False).items():
        setattr(current_student, field, value)

    db_session.flush()

    return current_student
