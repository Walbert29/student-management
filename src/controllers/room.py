from fastapi import APIRouter, status

from schemas.room import CreateRoomSchema

from services.room import list_rooms_info, create_room

room_router = APIRouter(
    prefix="/room",
    tags=["Room"],
)


@room_router.get(
    path="/list",
    status_code=status.HTTP_200_OK,
    summary="List rooms",
)
def get_list_rooms():
    """
    # Endpoint for listing all rooms.

    ### Returns:
        JSONResponse: Response with list of rooms.

    """
    return list_rooms_info()


@room_router.post(
    path="/create",
    status_code=status.HTTP_201_CREATED,
    summary="Create Room",
)
def post_new_group(room: CreateRoomSchema):
    """
    # Endpoint to create a new Room.

    ### Args:
        room (CreateRoomSchema): Room data to be created, adhering to the schema.

    ### Returns:
        dict: A dictionary containing information about the newly created room.
    """
    return create_room(room=room)
