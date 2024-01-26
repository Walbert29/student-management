from fastapi import APIRouter, status

from services.student import obtain_students_by_group

student_router = APIRouter(
    prefix="/student",
    tags=["Student"],
)


@student_router.post(
    path="/group/{group_id}",
    status_code=status.HTTP_201_CREATED,
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
