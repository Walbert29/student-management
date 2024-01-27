from fastapi import APIRouter, status

from services.group import list_groups_info, create_group, remove_group

from schemas.group import CreateGroupSchema

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


@group_router.post(
    path="/create",
    status_code=status.HTTP_201_CREATED,
    summary="Create Group",
)
def post_new_group(group: CreateGroupSchema):
    """
    # Endpoint to create a new group.

    ### Args:
        group (CreateGroupSchema): The group data to be created, adhering to the schema.

    ### Returns:
        dict: A dictionary containing information about the newly created group.
    """
    return create_group(group=group)


@group_router.delete(
    path="/delete/{group_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete Group",
)
def delete_group_by_id(group_id: int):
    """
    # Endpoint to delete a group.

    ### Args:
        group_id (int): Group ID.

    ### Returns:
        dict: A dictionary containing information about the deleted group.
    """
    return remove_group(group_id=group_id)
