import sys
import unittest
from fastapi.testclient import TestClient

sys.path.insert(0, "../src")

from main import app

client = TestClient(app)


class TestCourse(unittest.TestCase):
    def test_create_course_successful(self):
        """
        Test case:
            Create new course successfully
        Expected state:
             Show message of successfully created course
        """
        data_to_create = {
              "name": "Learn Marketing",
              "description": "Course about marketing",
            }
        request = client.post("/course/create", json=data_to_create)

        self.assertEqual(request.status_code, 201)
        response = request.json()
        self.assertEqual(response["message"], "Data created successfully")

    def test_create_course_value_no_valid(self):
        """
        Test case:
            Create a new course with an invalid name.
        Expected state:
             Display error message with description of the camo to be corrected.
        """
        data_to_create = {
              "name": 90,
              "description": "Course about marketing",
            }
        request = client.post("/course/create", json=data_to_create)

        error_detail_expected = [
            {
              "type": "string_type",
              "loc": [
                "body",
                "name"
              ],
              "msg": "Input should be a valid string",
              "input": 90,
              "url": "https://errors.pydantic.dev/2.5/v/string_type"
            }
          ]

        self.assertEqual(request.status_code, 422)
        response = request.json()
        self.assertEqual(response["detail"], error_detail_expected)