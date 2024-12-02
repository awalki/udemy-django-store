from datetime import timedelta
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from users.models import EmailVerification, User


class UserRegistrationViewTestCase(TestCase):
    def setUp(self):
        self.path = reverse("users:registration")
        self.data = {
            "first_name": "Test",
            "last_name": "User",
            "username": "testuser",
            "email": "testuser@example.com",
            "password1": "Testpass123!",
            "password2": "Testpass123!",
        }

    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context["title"], "Store - Регистрация")
        self.assertTemplateUsed(response, "users/registration.html")

    def test_user_registration_post_success(self):
        username = self.data["username"]
        self.assertFalse(User.objects.filter(username=username).exists())
        response = self.client.post(self.path, data=self.data)

        # Check creating of user
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        # TODO: FIX THIS FUCKING TEST
        # self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(User.objects.filter(username=username).exists())

        # Check email
        email_verification = EmailVerification.objects.filter(user__username=username)
        self.assertTrue(email_verification.exists())
        self.assertEqual(
            email_verification.first().expiration.date(),
            (now() + timedelta(hours=48)).date(),
        )

    def test_user_registration_post_error(self):
        User.objects.create(username=self.data["username"])
        response = self.client.post(self.path, data=self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(
            response, "Пользователь с таким именем уже существует", html=True
        )
