from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session


from crud.guardian import get_guardian_by_email
from models.guardian import GuardianModel
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
        guardian_data_to_create = jsonable_encoder(
            validated_guardian_data, by_alias=False
        )
        create_guardian = GuardianModel(**guardian_data_to_create)
        session.add(create_guardian)
        session.flush()
        return create_guardian.id
    return get_guardian.id
