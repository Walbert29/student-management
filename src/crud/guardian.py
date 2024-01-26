from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from models.guardian import GuardianModel
from schemas.guardian import CreateGuardianSchema

# GET


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


# POST


def create_massive_guardian(
    db_session: Session, guardian: CreateGuardianSchema
) -> GuardianModel:
    """
    Create a new guardian in the database.

    Args:
        db_session (Session): SQLAlchemy database session.
        guardian (CreateGuardianSchema): Guadian to be created.

    Returns:
        GuardianModel: Instance of the guandiam model corresponding to the newly created guardian.
    """

    guardian_data_to_create = jsonable_encoder(guardian, by_alias=False)
    create_guardian = GuardianModel(**guardian_data_to_create)
    db_session.add(create_guardian)
    db_session.flush()

    return create_guardian
