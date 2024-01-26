from fastapi import APIRouter, status

from services.teacher import create_teacher

from schemas.teacher import CreateTeacherSchema

teacher_router = APIRouter(
    prefix="/teacher",
    tags=["Teacher"],
)


@teacher_router.post(
    path="/create",
    status_code=status.HTTP_201_CREATED,
    summary="Create Teacher",
)
def post_new_group(teacher: CreateTeacherSchema):
    """
    # Endpoint to create a new teacher.

    ### Args:
        teacher (CreateTeacherSchema): Teacher data to be created, adhering to the schema.

    ### Returns:
        dict: A dictionary containing information about the newly created teacher.
    """
    return create_teacher(teacher=teacher)
