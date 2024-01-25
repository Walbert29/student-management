import xlsxwriter
from fastapi import status, HTTPException
from fastapi.responses import FileResponse


from enums.templates import TypeTemplates


def list_available_templates():
    """
    List the templates available to use

    Returns:
    - JSON: ListTemplateSchema
    """

    list_templates = []

    for template in TypeTemplates:
        list_templates.append(
            {
                "id": template.template_id,
                "name": template.template_name,
                "description": template.template_description,
            }
        )

    return list_templates


def generate_template(template_id: int) -> FileResponse:
    """
    generate the necessary template for bulk data uploading.

    Returns:
    - File: xlsx file with the required structure

    Raises:
    """

    template_selected = None

    for template in TypeTemplates:
        if template.template_id == template_id:
            template_selected = template

    if template_selected is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template with ID {template_id} not found",
        )

    file_name = f"{template_selected.template_name}.xlsx"

    workbook = xlsxwriter.Workbook(file_name)
    worksheet = workbook.add_worksheet()

    col_position = 0

    for header in template_selected.headers:
        worksheet.write(0, col_position, header)
        col_position += 1

    workbook.close()

    return FileResponse(
        file_name,
        filename=file_name,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
