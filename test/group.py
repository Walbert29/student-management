import sys
import unittest
from fastapi.testclient import TestClient

sys.path.insert(0, "../src")

from main import app

client = TestClient(app)
class TestGroup(unittest.TestCase):
    def test_list_group_with_course(self):
        """
        Test case:
            List list list groups with their respective courses.
        Expected state:
            All existing groups and the respective courses to which it is attached should be displayed.
        """
        response = client.get("/group/list")

        self.assertEqual(response.status_code, 200)

        data_expected = {
                "Group": {
                  "end_time": "2024-01-27T17:54:24",
                  "id": 1,
                  "description": "Course Backend level: A1",
                  "start_time": "2024-01-26T17:54:20",
                  "name": "Backend A1",
                  "course_id": 1
                },
                "Course": {
                  "name": "Backend",
                  "id": 1,
                  "description": "Course about Backend"
                }
              }
        data_groups = response.json()

        self.assertEqual(data_groups[0], data_expected)

    def test_create_group_course_error(self):
        """
        Test case:
            Create group, in this case linking it to a non-existing course.
        Expected state:
            Display message alerting the group cannot be created because the associated course is not found.
        """
        course_id = 99
        data_to_create = {
              "name": "Data Sir",
              "description": "Data Full Sir",
              "start_time": "2024-01-27T18:52:22.741Z",
              "end_time": "2024-01-27T18:52:22.741Z",
              "course_id": course_id
            }
        request = client.post("/group/create", json=data_to_create)

        self.assertEqual(request.status_code, 404)
        response = request.json()
        self.assertEqual(response["message"], f"Course with ID: {course_id} not found")

    def test_create_group_successful(self):
        """
        Test case:
            Create group, in this case linking it to a non-existing course.
        Expected state:
            Display message alerting the group cannot be created because the associated course is not found.
        """
        course_id = 3
        data_to_create = {
              "name": "Data Sir",
              "description": "Data Full Sir",
              "start_time": "2024-01-27T18:52:22.741Z",
              "end_time": "2024-01-27T18:52:22.741Z",
              "course_id": course_id
            }
        request = client.post("/group/create", json=data_to_create)

        self.assertEqual(request.status_code, 201)
        response = request.json()
        self.assertEqual(response["message"], "Data created successfully")