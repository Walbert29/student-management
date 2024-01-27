from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from database.database import create_connection

from schemas.room import CreateRoomSchema

from crud.teacher import get_teacher_by_id
from crud.group import get_group_by_id
from crud.room import list_rooms_with_groups, post_room, verify_room_exists, delete_room
from crud.enrollment import get_enrollment_by_room_id


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


def create_room(room: CreateRoomSchema):
    """
    Create a new room in the database.

    Args:
        room (CreateRoomSchema): The room data to be created, adhering to the schema.

    Returns:
        Union[JSONResponse, RoomModel]: A JSONResponse if the associated group_id or teacher_id is not found,
        otherwise the newly created room.
    """
    try:
        session = create_connection()
        exists_group = get_group_by_id(db_session=session, group_id=room.group_id)
        if not exists_group:
            return JSONResponse(
                content={"message": f"Group with ID: {room.group_id} not found"},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        exists_teacher = get_teacher_by_id(
            db_session=session, teacher_id=room.teacher_id
        )
        if not exists_teacher:
            return JSONResponse(
                content={"message": f"Teacher with ID: {room.teacher_id} not found"},
                status_code=status.HTTP_404_NOT_FOUND,
            )
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "Data created successfully",
                "data": jsonable_encoder(post_room(db_session=session, room=room)),
            },
        )

    finally:
        session.close()


def remove_room(room_id: int):
    """
    Removes a room record.

    Args:
        room_id (int): Room ID.

    Returns:
        RoomModel: Room Model

    """

    try:
        session = create_connection()

        verify_room = verify_room_exists(db_session=session, room_id=room_id)
        if not verify_room:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": f"Room with ID: {room_id} not found"},
            )

        verify_enrollment_with_room = get_enrollment_by_room_id(
            room_id=room_id, db_session=session
        )

        if verify_enrollment_with_room:
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={
                    "message": f"Room with ID: {room_id} has enrollments associated"
                },
            )

        delete_room(db_session=session, room_id=room_id)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Data deleted successfully",
                "data": jsonable_encoder(verify_room),
            },
        )

    finally:
        session.close()
