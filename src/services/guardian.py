from sqlalchemy.orm import Session


from crud.guardian import create_massive_guardian, get_guardian_by_email
from schemas.guardian import CreateGuardianSchema


def create_guardian(session: Session, validated_guardian_data: CreateGuardianSchema):
    """
    Creates or retrieves a guardian based on the provided data.

    Args:
        session (Session): SQLAlchemy session.
        validated_guardian_data (CreateGuardianSchema): Validated guardian data.

    Returns:
        int: Guardian ID.
    """
    get_guardian = get_guardian_by_email(session, validated_guardian_data.email)
    if not get_guardian:
        create_guardian = create_massive_guardian(
            db_session=session, guardian=validated_guardian_data
        )
        return create_guardian.id
    return get_guardian.id
