from fastapi import APIRouter, UploadFile, status, File

from services.student import (
    obtain_students_by_group,
    obtain_students_by_room,
    update_data_students,
)

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


@student_router.put(
    path="/update/massive",
    status_code=status.HTTP_200_OK,
    summary="Update students massive",
)
def update_students_guardian_data(file: UploadFile = File(...)):
    """
    # Endpoint to update the information of a group of students and guardian by processing an Excel file containing enrollment data.

    ### Args:
        file (UploadFile): Excel file containing student/guardian data (required).

    ### Returns:
        JSONResponse:cResponse with details of updates made and not processed.

    """
    return update_data_students(file=file)
