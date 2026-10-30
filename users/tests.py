from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class AdminLoginRedirectTests(TestCase):
    def test_superuser_redirects_to_admin_dashboard(self):
        User.objects.create_user(
            email="admin@test.com",
            password="12345678",
            name="Admin User",
            phone="1234567890",
            is_staff=True,
            is_superuser=True,
        )

        response = self.client.post(
            reverse("users:login"),
            {"email": "admin@test.com", "password": "12345678"},
            follow=False,
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("users:admin.index"))

    def test_superuser_can_log_in_with_username(self):
        User.objects.create_user(
            username="ithan123",
            email="ithan123@admin.invalid",
            password="StrongTestPassword123!",
            name="Admin User",
            phone="1234567890",
            is_staff=True,
            is_superuser=True,
        )

        response = self.client.post(
            reverse("users:login"),
            {"email": "ithan123", "password": "StrongTestPassword123!"},
        )

        self.assertRedirects(response, reverse("users:admin.index"))
        self.assertEqual(
            self.client.session["_auth_user_id"],
            str(User.objects.get(username="ithan123").pk),
        )

    def test_regular_user_cannot_access_admin_dashboard(self):
        user = User.objects.create_user(
            email="customer@test.com",
            password="StrongTestPassword123!",
            name="Customer",
            phone="1234567890",
        )
        self.client.force_login(user)

        response = self.client.get(reverse("users:admin.index"))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/users/login/"))
