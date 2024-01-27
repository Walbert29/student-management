from fastapi import APIRouter, status

from services.course import create_course, remove_course
from schemas.course import CreateCourseSchema

course_router = APIRouter(
    prefix="/course",
    tags=["Course"],
)


@course_router.post(
    path="/create",
    status_code=status.HTTP_201_CREATED,
    summary="Create Course",
)
def post_new_course(course: CreateCourseSchema):
    """
    # Endpoint to create a new course.

    ### Args:
        course (CreateCourseSchema): The course data to be created, adhering to the schema.

    ### Returns:
        dict: A dictionary containing information about the newly created course.
    """
    return create_course(course=course)


@course_router.delete(
    path="/delete/{course_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete Course",
)
def delete_course_by_id(course_id: int):
    """
    # Endpoint to delete a course.

    ### Args:
        course_id (int): Course ID.

    ### Returns:
        dict: A dictionary containing information about the deleted course.
    """
    return remove_course(course_id=course_id)
