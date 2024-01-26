from crud.room import list_rooms_with_groups
from database.database import create_connection


def list_rooms_info():
    """
    List rooms with respectives groups.

    Returns:
        List[GuardianModel]: List of room with respectives groups.
    """
    try:
        session = create_connection()
        groups = list_rooms_with_groups(db_session=session)
        list_groups = []
        for group in groups:
            list_groups.append({"Room": group[0], "Group": group[1]})

        return list_groups

    finally:
        session.close()
