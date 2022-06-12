import os
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files import File
from explorer.models import Application


class TestApplications(APITestCase):
    @classmethod
    def setUpTestData(cls):
        """Create 2 users (test_user_1 & test_user_2) and one application for each (apk1 & apk2)."""
        cls.user = [User.objects.create(username=f"test_user_{_}") for _ in range(1, 3)]
        cls.applications = [
            Application.objects.create(
                application=f"apk{_}",
                package_name=f"com.apk{_}",
                package_version_code=1.0,
                owner_id=_,
            )
            for _ in range(1, 3)
        ]

    def test_retrieve_apps(self):
        response = self.client.get("/api/applications")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(self.applications), len(response.data))

    def test_retrieve_single_app(self):
        response = self.client.get("/api/applications/1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["application"], "apk1")
        self.assertEqual(response.data["package_name"], "com.apk1")

    def test_upload_app(self):
        # Authentication
        user = User.objects.get(username="test_user_1")
        self.client.force_authenticate(user=user)

        # APK upload
        module_dir = os.path.dirname(__file__)
        filepath = os.path.join(module_dir, "apk_examples/mi_launcher.apk")
        data = File(open(filepath, "rb"))
        uploaded_file = SimpleUploadedFile(
            "apk", data.read(), content_type="multipart/form-data"
        )
        payload = {"file": uploaded_file}
        response = self.client.post("/api/applications", payload, format="multipart")
        uploaded_app = Application.objects.get(
            package_name="com.mi.android.globallauncher"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(uploaded_app.owner.username, "test_user_1")

    def test_remove_app(self):
        # Authentication
        user = User.objects.get(username="test_user_1")
        self.client.force_authenticate(user=user)

        remove_response = self.client.delete("/api/applications/1")
        app_response = self.client.get("/api/applications/1")
        self.assertEqual(remove_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(app_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cannot_remove_other_creators_app(self):
        # Authentication
        user = User.objects.get(username="test_user_2")
        self.client.force_authenticate(user=user)

        response = self.client.delete(
            "/api/applications/1"
        )  # This app belongs to test_user_1
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
