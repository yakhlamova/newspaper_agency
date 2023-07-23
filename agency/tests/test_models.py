from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from agency.models import Topic, Newspaper, Redactor


class ModelsTest(TestCase):
    def test_topic_str(self):
        topic = Topic.objects.create(
            name="test_name"
        )

        self.assertEquals(
            str(topic),
            f"{topic.name}"
        )

    def test_redactor_str(self):
        redactor = get_user_model().objects.create_user(
            username="test_username",
            password="test_password_qwerty123",
            first_name="test_first_name",
            last_name="test_last_name"
        )

        self.assertEquals(
            str(redactor),
            f"{redactor.username} ({redactor.first_name} {redactor.last_name})"
        )

    def test_newspaper_str(self):
        topic = Topic.objects.create(name="test_name")
        newspaper = Newspaper.objects.create(
            title="test_model",
            topic=topic,
            published_date=timezone.now()  # Set the published_date to the current date and time
        )

        self.assertEqual(str(newspaper), newspaper.title)

    def test_create_redactor_with_years_of_experience(self):
        username = "test_username"
        password = "test_password_qwerty123"
        years_of_experience = 10

        redactor = get_user_model().objects.create_user(
            username=username,
            password=password,
            years_of_experience=years_of_experience
        )

        self.assertEqual(redactor.username, username)
        self.assertTrue(redactor.check_password(password))
        self.assertEqual(redactor.years_of_experience, years_of_experience)
