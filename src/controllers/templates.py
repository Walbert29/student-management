from fastapi import APIRouter, status
from fastapi.responses import FileResponse

from services.templates import (
    list_available_templates,
    generate_template,
)

template_router = APIRouter(
    prefix="/template",
    tags=["Templates"],
)


@template_router.get(
    path="/list/templates",
    status_code=status.HTTP_200_OK,
    summary="List of available templates",
)
def get_list_templates():
    """
    # Get list of available templates

    ### Returns:
    #### JSON: ListTemplateSchema

    """
    return list_available_templates()


@template_router.get(
    path="/template/{template_id}",
    status_code=status.HTTP_200_OK,
    summary="Get template to be completed by id",
)
def get_template(template_id: int) -> FileResponse:
    """
    # Get template to be completed by id

    ### Returns:
    #### File: xlsx file with the required structure

    """
    return generate_template(template_id=template_id)
