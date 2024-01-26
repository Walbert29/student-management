from fastapi import APIRouter, File, UploadFile, status

from services.enrollment import (
    create_enrollment_students,
)

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
