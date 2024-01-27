import sys
import unittest
from fastapi.testclient import TestClient

sys.path.insert(0, "../src")

from main import app

client = TestClient(app)


class TestEnrollment(unittest.TestCase):
    def test_create_enrollment_from_file(self):
        """
        Test case:
            Student and mentor database is clean, proceed to create a set of enrollments.
        Expected state:
            Successful enrollment of students.
        """
        file_path = "../../List Students Test.xlsx"

        with open(file_path, "rb") as file:
            response = client.post(
                "/enrollment/students",
                files={
                    "file": (
                        file_path,
                        file,
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )
                },
            )

        self.assertEqual(response.status_code, 207)

        successful_users = response.json()["Successful users"]
        for user in successful_users:
            self.assertEqual(user["Status"], "Successful")

    def test_studiants_already_created_from_file(self):
        """
        Test case:
            Attempting to enroll students created in the first iteration of the attached file.
        Expected state:
            Error message alerting the already existences of these.
        """
        file_path = "../../List Students Test.xlsx"

        with open(file_path, "rb") as file:
            response = client.post(
                "/enrollment/students",
                files={
                    "file": (
                        file_path,
                        file,
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )
                },
            )

        self.assertEqual(response.status_code, 207)

        failed_users = response.json()["Failed users"]
        self.assertEqual(
            failed_users[0]["Error message"],
            "Student already enrolled in room or group: 3",
        )

        self.assertEqual(
            failed_users[1]["Error message"],
            "Student already enrolled in room or group: 4",
        )

        self.assertEqual(
            failed_users[2]["Error message"],
            "Student already enrolled in room or group: 3",
        )

    def test_student_with_last_name_error_from_file(self):
        """
        Test case:
            Student's last name with mail: pablo@gmail.com does not meet the typography that the field requires.
        Expected state:
            The following message should be displayed: Input should be a valid string
        """
        file_path = "../../List Students Test.xlsx"

        with open(file_path, "rb") as file:
            response = client.post(
                "/enrollment/students",
                files={
                    "file": (
                        file_path,
                        file,
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )
                },
            )

        self.assertEqual(response.status_code, 207)

        failed_users = response.json()["Failed users"]
        self.assertEqual(failed_users[3]["Record"]["Student Email"], "pablo@gmail.com")
        self.assertEqual(
            failed_users[3]["Error message"], "Input should be a valid string"
        )
