from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from models.teacher import TeacherModel

from schemas.teacher import CreateTeacherSchema

# GET


def get_teacher_by_email(db_session: Session, email: str) -> TeacherModel:
    """
    Retrieve a teacher from the database based on their email address.

    Args:
        db_session (Session): SQLAlchemy database session.
        email (str): Email address of the teacher being searched.

    Returns:
        TeacherModel: Instance of the Teacher model corresponding to the provided email,
                      or None if no Teacher is found with that email.
    """

    query = db_session.query(TeacherModel).filter(TeacherModel.email == email).first()

    return query


def get_teacher_by_id(db_session: Session, teacher_id: int) -> TeacherModel:
    """
    Retrieve a teacher from the database based on its ID.

    Args:
        db_session (Session): SQLAlchemy database session.
        teacher_id (int): The ID of the teacher to be retrieved.

    Returns:
        TeacherModel: The teacher with the specified ID.
    """

    return db_session.query(TeacherModel).filter(TeacherModel.id == teacher_id).first()


# POST


def post_teacher(db_session: Session, teacher: CreateTeacherSchema) -> TeacherModel:
    """
    Create a new teacher in the database.

    Args:
        db_session (Session): SQLAlchemy database session.
        teacher (CreateTeacherSchema): Teacher data to be created, adhering to the schema.

    Returns:
        TeacherModel: The new teacher created.
    """

    map_course = jsonable_encoder(teacher)
    data_to_create = TeacherModel(**map_course)
    db_session.add(data_to_create)
    db_session.commit()
    db_session.refresh(data_to_create)

    return data_to_create
