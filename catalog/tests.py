from django.test import Client, TestCase
from django.urls import reverse


class CoursePortalViewTests(TestCase):
    def test_home_page_shows_course_summary(self):
        response = self.client.get(reverse("catalog:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome to DTI CoursePortal")
        self.assertContains(response, "DTI412")
        self.assertEqual(response.context["total_courses"], 3)

    def test_course_list_and_search(self):
        response = self.client.get(reverse("catalog:course_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["courses"]), 3)

        response = self.client.get(
            reverse("catalog:course_list"),
            {"q": "dti305"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [course["code"] for course in response.context["courses"]],
            ["DTI305"],
        )

    def test_course_detail_and_unknown_course(self):
        response = self.client.get(
            reverse("catalog:course_detail", args=[101])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Special Topic in Application Development")

        response = self.client.get(
            reverse("catalog:course_detail", args=[999])
        )
        self.assertEqual(response.status_code, 404)

    def test_inquiry_rejects_missing_or_invalid_fields(self):
        response = self.client.post(
            reverse("catalog:inquiry"),
            {
                "student_name": " ",
                "email": "not-an-email",
                "message": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Student Name is required.")
        self.assertContains(response, "A valid Email address is required.")
        self.assertContains(response, "Inquiry message cannot be empty.")
        self.assertIsNone(response.context["submitted_data"])

    def test_inquiry_accepts_valid_post_and_course_code(self):
        response = self.client.post(
            reverse("catalog:inquiry"),
            {
                "student_name": "Jane Doe",
                "email": "jane@example.com",
                "course_code": "DTI412",
                "message": "Could you share the course schedule?",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Inquiry Processed Successfully!")
        self.assertContains(response, "Jane Doe")
        self.assertEqual(
            response.context["submitted_data"]["course_code"],
            "DTI412",
        )

    def test_inquiry_rejects_unknown_course_code(self):
        response = self.client.post(
            reverse("catalog:inquiry"),
            {
                "student_name": "Jane Doe",
                "email": "jane@example.com",
                "course_code": "UNKNOWN",
                "message": "Question",
            },
        )

        self.assertContains(response, "Select a course from the available list.")
        self.assertIsNone(response.context["submitted_data"])

    def test_inquiry_requires_a_csrf_token(self):
        client = Client(enforce_csrf_checks=True)
        inquiry_url = reverse("catalog:inquiry")
        valid_data = {
            "student_name": "Jane Doe",
            "email": "jane@example.com",
            "course_code": "DTI412",
            "message": "Question",
        }

        rejected = client.post(inquiry_url, valid_data)
        self.assertEqual(rejected.status_code, 403)

        form_page = client.get(inquiry_url)
        self.assertEqual(form_page.status_code, 200)
        csrf_token = client.cookies["csrftoken"].value
        accepted = client.post(
            inquiry_url,
            valid_data,
            HTTP_X_CSRFTOKEN=csrf_token,
        )
        self.assertEqual(accepted.status_code, 200)
