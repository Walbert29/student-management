from typing import List
from pydantic import BaseModel, Field

from utils.example_templates import schema_extra


class TemplateInfoSchema(BaseModel):
    """
    Structure that controls the type of data that lists the templates

    Attributes:
        template_id (int): Template ID.
        name (str): Template Name.
        description (str): Template Description.
    """

    template_id: int = Field()
    name: str = Field()
    description: str = Field()


class ListTemplateSchema(BaseModel):
    """
    Structure that controls the type of data for a list of templates

    Attributes:
        templates (List[TemplateInfoSchema]): List of template information.
    """

    templates: List[TemplateInfoSchema]

    class Config:
        schema_extra = schema_extra
