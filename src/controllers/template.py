from fastapi import APIRouter, status
from fastapi.responses import FileResponse

from services.template import (
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
    # This function is a GET endpoint that returns a list of available templates.
    ## It does not require any parameters.

    ### Returns:
        list: A list of available templates. The structure of the templates is defined by the ListTemplateSchema.
    """
    return list_available_templates()


@template_router.get(
    path="/template/{template_id}",
    status_code=status.HTTP_200_OK,
    summary="Get template to be completed by id",
)
def get_template(template_id: int) -> FileResponse:
    """
    # This function is a GET endpoint that returns a specific template based on the provided template_id.

    ### Args:
        template_id (int): The ID of the template to be retrieved.

    ### Returns:
        FileResponse: An xlsx file with the required structure.
    """
    return generate_template(template_id=template_id)
