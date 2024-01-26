from fastapi import APIRouter, status

from services.room import list_rooms_info

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
