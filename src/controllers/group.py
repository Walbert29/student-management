from fastapi import APIRouter, status

from services.group import list_groups_info

group_router = APIRouter(
    prefix="/group",
    tags=["Group"],
)


@group_router.get(
    path="/list",
    status_code=status.HTTP_200_OK,
    summary="List groups",
)
def get_list_groups():
    """
    # Endpoint for listing all groups.

    ### Returns:
        JSONResponse: Response with list of groups.

    """
    return list_groups_info()
