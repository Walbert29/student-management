from enum import Enum


class TypeTemplates(Enum):
    """
    Control the templates that can be downloaded
    """

    ENROLLMENT_STUDENT = (
        1,
        "Enrollment Student",
        "Template used to make or update student enrollments",
        [
            "Student Frist name",
            "Student Last Name",
            "Student Email",
            "Guardian First Name",
            "Guardian Last Name",
            "Guardian Email",
            "Guardian Identification Type (ID)",
            "Guardian Identification Number",
            "Guardian Country (Id)",
            "Room ID",
        ],
    )

    def __init__(self, template_id, name, description, headers):
        self.template_id = template_id
        self.template_name = name
        self.template_description = description
        self.headers = headers
