from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from agency.models import Redactor


class RedactorAdminTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin1234"
        )
        self.client.force_login(self.admin_user)
        self.redactor = get_user_model().objects.create_user(
            username="redactor",
            password="redactor1234",
            years_of_experience=5
        )

    def test_redactor_years_of_experience_listed(self):
        url = reverse("admin:agency_redactor_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.redactor.years_of_experience)

    def test_redactor_detailed_years_of_experience_listed(self):
        url = reverse("admin:agency_redactor_change", args=[self.redactor.id])
        response = self.client.get(url)

        self.assertContains(response, self.redactor.years_of_experience)
