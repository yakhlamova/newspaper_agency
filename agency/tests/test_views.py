from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from agency.models import Redactor, Topic, Newspaper


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin1234"
        )
        self.client.force_login(self.admin_user)

    def test_index_view(self):
        url = reverse("agency:index")
        response = self.client.get(url)

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert that the correct template is used for rendering
        self.assertTemplateUsed(response, "agency/index.html")

        self.assertEqual(response.context["num_redactors"], Redactor.objects.count())
        self.assertEqual(response.context["num_newspapers"], Newspaper.objects.count())
        self.assertEqual(response.context["num_topics"], Topic.objects.count())

        # Assert that the session variable is set and incremented correctly
        self.assertEqual(self.client.session.get("num_visits"), 1)
        response = self.client.get(url)
        self.assertEqual(self.client.session.get("num_visits"), 2)

    def test_topic_list_view(self):
        # Create some test topics
        Topic.objects.create(name="Topic 1")
        Topic.objects.create(name="Topic 2")

        url = reverse("agency:topic-list")
        response = self.client.get(url)

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert that the correct template is used for rendering
        self.assertTemplateUsed(response, "agency/topic_list.html")

        # Assert that the topics are listed in the response content
        self.assertContains(response, "Topic 1")
        self.assertContains(response, "Topic 2")

    # You can write similar tests for other views as well

    def test_redactor_create_view(self):
        url = reverse("agency:redactor-create")
        response = self.client.get(url)

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert that the correct template is used for rendering
        self.assertTemplateUsed(response, "agency/redactor_form.html")

    def test_redactor_create_submit(self):
        # Test submitting the Redactor creation form
        url = reverse("agency:redactor-create")
        data = {
            "username": "new_redactor",
            "password1": "new_password",
            "password2": "new_password",
            "years_of_experience": 5,
            # Add other required fields as needed for your form
        }
        response = self.client.post(url, data)

        # Check if the response status code is 302 (Redirect)
        self.assertEqual(response.status_code, 302)

        # Assert that the Redactor is created in the database
        redactor = Redactor.objects.get(username="new_redactor")
        self.assertEqual(redactor.years_of_experience, 5)

    # You can write similar tests for other view actions like update and delete

    def test_redactor_detail_view(self):
        redactor = Redactor.objects.create_user(
            username="test_redactor",
            password="test_password",
            years_of_experience=8,
        )

        url = reverse("agency:redactor-detail", args=[redactor.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "agency/redactor_detail.html")
        self.assertContains(response, "test_redactor")
