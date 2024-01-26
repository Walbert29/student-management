from sqlalchemy.orm import Session

from models.guardian import GuardianModel


def get_guardian_by_email(db_session: Session, email: str) -> GuardianModel:
    """
    Retrieve a guardian from the database based on their email address.

    Args:
        db_session (Session): SQLAlchemy database session.
        email (str): Email address of the guardian being searched.

    Returns:
        GuardianModel: Instance of the Guardian model corresponding to the provided email,
                      or None if no guardian is found with that email.
    """

    query = db_session.query(GuardianModel).filter(GuardianModel.email == email).first()

    return query
