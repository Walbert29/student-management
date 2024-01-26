from crud.group import list_groups_with_courses
from database.database import create_connection


def list_groups_info():
    """
    List groups with respectives courses.

    Returns:
        List[GuardianModel]: List of groups with respectives courses.
    """
    try:
        session = create_connection()
        groups = list_groups_with_courses(db_session=session)
        list_groups = []
        for group in groups:
            list_groups.append({"group": group[0], "course": group[1]})

        return list_groups

    finally:
        session.close()
