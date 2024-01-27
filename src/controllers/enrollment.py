from fastapi import APIRouter, File, UploadFile, status

from services.enrollment import create_enrollment_students, remove_enrollment

enrollment_router = APIRouter(
    prefix="/enrollment",
    tags=["Enrollment"],
)


@enrollment_router.post(
    path="/students",
    status_code=status.HTTP_201_CREATED,
    summary="Enrollment of a group of students",
)
def post_enrollment_students(file: UploadFile = File(...)):
    """
    # Endpoint for enrolling a group of students by processing an Excel file containing enrollment data.

    ### Args:
        file (UploadFile): Excel file containing enrollment data (required).

    ### Returns:
        JSONResponse: Response with details of successful and failed enrollments.

    """
    return create_enrollment_students(file=file)


@enrollment_router.delete(
    path="/delete/{enrollment_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete enrollment of a student",
)
def delete_enrollment_students(enrollment_id: int):
    """
    # Endpoint for deleting the enrollment of a student.

    ### Args:
        enrollment_id (int): Enrollment ID (required).

    ### Returns:
        JSONResponse: Response with details of successful deletions.

    """
    return remove_enrollment(enrollment_id)
