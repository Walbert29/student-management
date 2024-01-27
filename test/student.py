import sys
import unittest
from fastapi.testclient import TestClient

sys.path.insert(0, "../src")

from main import app

client = TestClient(app)


class TestStudent(unittest.TestCase):
    def test_student_no_enrollment_error(self):
        """
        Test case:
            Search for student with email: pablo@gmail.com assigned to room 4 whose registration failed and therefore its creation in the DB.
        Expected state:
            No user records should be found when searching the assigned room.
        """
        email = "pablo@gmail.com"
        room = 4
        response = client.get(f"/student/room/{room}")

        self.assertEqual(response.status_code, 200)
        user_search = None
        for user in response.json():
            if user["email"] == email:
                user_search = user["email"]

        self.assertIsNone(user_search)

    def test_show_student_by_group(self):
        """
        Test case:
            List students by group
        Expected state:
            All students that the group has must be shown, for this test at least one of the 3 added in the sheets must be shown.
        """

        group_id = 2
        student_email_to_verify = "diana@gmail.com"
        response = client.get(f"/student/group/{group_id}")

        self.assertEqual(response.status_code, 200)
        user_search = None
        for user in response.json():
            if user["email"] == student_email_to_verify:
                user_search = user["email"]

        self.assertEqual(user_search, student_email_to_verify)
