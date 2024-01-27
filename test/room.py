import sys
import unittest
from fastapi.testclient import TestClient

sys.path.insert(0, "../src")

from main import app

client = TestClient(app)


class TestRoom(unittest.TestCase):
    def test_create_room_successful(self):
        """
        Test case:
            Create a new room successfully
        Expected state:
            Room message successfully created
        """
        data_to_create = {
          "name": "Room D4",
          "group_id": 1,
          "teacher_id": 1
        }
        request = client.post("/room/create", json=data_to_create)

        self.assertEqual(request.status_code, 201)
        response = request.json()
        self.assertEqual(response["message"], "Data created successfully")

    def test_create_room_successful_group_no_exists(self):
        """
        Test case:
            Create room successfully but with non-existing group id.
        Expected state:
               Group to assign message not found
        """
        data_to_create = {
            "name": "Room D4",
            "group_id": 99,
            "teacher_id": 1
        }
        request = client.post("/room/create", json=data_to_create)

        self.assertEqual(request.status_code, 404)
        response = request.json()
        self.assertEqual(response["message"], f"Group with ID: {data_to_create['group_id']} not found")

    def test_create_room_successful_teacher_no_exists(self):
        """
        Test case:
            Create room successfully but with non-existing teacher id.
        Expected state:
               Teacher to assign message not found
        """
        data_to_create = {
            "name": "Room D4",
            "group_id": 1,
            "teacher_id": 99
        }
        request = client.post("/room/create", json=data_to_create)

        self.assertEqual(request.status_code, 404)
        response = request.json()
        self.assertEqual(response["message"], f"Teacher with ID: {data_to_create['teacher_id']} not found")