from fastapi import APIRouter, status

from services.student import obtain_students_by_group, obtain_students_by_room

student_router = APIRouter(
    prefix="/student",
    tags=["Student"],
)


@student_router.get(
    path="/group/{group_id}",
    status_code=status.HTTP_200_OK,
    summary="Get students by group",
)
def get_students_by_group_id(group_id: int):
    """
    # Endpoint for retrieving a list of students based on the provided group ID.

    ### Args:
        group_id (int): Group ID.

    ### Returns:
        JSONResponse: Response with list of students.

    """
    return obtain_students_by_group(group_id=group_id)


@student_router.get(
    path="/room/{room_id}",
    status_code=status.HTTP_200_OK,
    summary="Get students by room",
)
def get_students_by_room_id(room_id: int):
    """
    # Endpoint for retrieving a list of students based on the provided Room ID.

    ### Args:
        room_id (int): Room ID.

    ### Returns:
        JSONResponse: Response with list of students.

    """
    return obtain_students_by_room(room_id=room_id)
