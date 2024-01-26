from sqlalchemy.orm import Session

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
