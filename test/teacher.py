import sys
import unittest
from fastapi.testclient import TestClient

sys.path.insert(0, "../src")

from main import app

client = TestClient(app)


class TestTeacher(unittest.TestCase):
    def test_create_teacher_successful(self):
        """
        Test case:
            Create new teacher successfully
        Expected state:
            Teacher message successfully created
        """
        data_to_create = {
          "first_name": "Diego",
          "last_name": "Perez",
          "email": "diegopp@gmail.com",
          "document_type_id": 1,
          "document_number": 2020,
          "country_id": 1
        }
        request = client.post("/teacher/create", json=data_to_create)

        self.assertEqual(request.status_code, 201)
        response = request.json()
        self.assertEqual(response["message"], "Data created successfully")

    def test_create_teacher_email_exists_error(self):
        """
        Test case:
            Create a new teacher but with an existing email.
        Expected state:
             Display error message with email already exists.
        """
        data_to_create = {
            "first_name": "Diego",
            "last_name": "Perez",
            "email": "juant@gmail.com",
            "document_type_id": 1,
            "document_number": 2020,
            "country_id": 1
        }

        request = client.post("/teacher/create", json=data_to_create)

        self.assertEqual(request.status_code, 409)
        response = request.json()
        self.assertEqual(response["message"], f"Teacher with email: {data_to_create['email']} already exists")