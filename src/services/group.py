from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import status

from crud.group import (
    list_groups_with_courses,
    post_group,
    get_group_by_id,
    delete_group,
)
from crud.room import get_room_by_group_id

from database.database import create_connection

from schemas.group import CreateGroupSchema

from crud.course import validate_exist_course


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
            list_groups.append({"Group": group[0], "Course": group[1]})

        return list_groups

    finally:
        session.close()


def create_group(group: CreateGroupSchema):
    """
    Create a new group in the database.

    Args:
        group (CreateGroupSchema): The group data to be created, adhering to the schema.

    Returns:
        Union[JSONResponse, GroupModel]: A JSONResponse if the associated course is not found,
        otherwise the newly created group.
    """
    try:
        session = create_connection()
        exist_course = validate_exist_course(
            db_session=session, course_id=group.course_id
        )
        if not exist_course:
            return JSONResponse(
                content={"message": f"Course with ID: {group.course_id} not found"},
                status_code=status.HTTP_404_NOT_FOUND,
            )
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "Data created successfully",
                "data": jsonable_encoder(post_group(db_session=session, group=group)),
            },
        )

    finally:
        session.close()


def remove_group(group_id: int):
    """
    Remove a group from the database.

    Args:
        group_id (int): The ID of the group to be removed.

    Returns:
        JSONResponse: A JSONResponse if the group is not found, otherwise a JSONResponse with a message.
    """
    try:
        session = create_connection()
        group = get_group_by_id(db_session=session, group_id=group_id)
        if not group:
            return JSONResponse(
                content={"message": f"Group with ID: {group_id} not found"},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        verify_associed_room = get_room_by_group_id(
            db_session=session, group_id=group_id
        )
        if verify_associed_room:
            return JSONResponse(
                content={
                    "message": f"Group with ID: {group_id} cannot be deleted because it has associated rooms"
                },
                status_code=status.HTTP_409_CONFLICT,
            )

        delete_group(db_session=session, group_id=group_id)

        return JSONResponse(
            content={
                "message": "Data deleted successfully",
                "data": jsonable_encoder(group),
            },
            status_code=status.HTTP_200_OK,
        )

    finally:
        session.close()
