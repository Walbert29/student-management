from sqlalchemy.orm import Session


from crud.guardian import (
    create_massive_guardian,
    update_massive_guardian,
    get_guardian_by_email,
    get_guardian_by_id,
)
from schemas.guardian import CreateGuardianSchema, UpdateGuardianSchema


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


def update_guardian(session: Session, validated_guardian_data: UpdateGuardianSchema):
    """
    Creates or retrieves a guardian based on the provided data.

    Args:
        session (Session): SQLAlchemy session.
        validated_guardian_data (CreateGuardianSchema): Validated guardian data.

    Returns:
        int: Guardian ID.
    """
    get_guardian = get_guardian_by_id(session, validated_guardian_data.id)
    if get_guardian:
        update_guardian = update_massive_guardian(
            db_session=session,
            updated_data=validated_guardian_data,
            current_guardian=get_guardian,
        )
        return update_guardian
    return get_guardian
