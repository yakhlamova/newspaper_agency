from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from agency.forms import RedactorForm, NewspaperForm


class RedactorCreationFormTest(TestCase):
    def test_clean_years_of_experience_valid(self):
        form_data = {
            "username": "testuser",
            "password1": "testpassword123",
            "password2": "testpassword123",
            "years_of_experience": 10,
            "first_name": "John",
            "last_name": "Doe",
        }
        form = RedactorForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_clean_years_of_experience_negative(self):
        form_data = {
            "username": "testuser",
            "password1": "testpassword123",
            "password2": "testpassword123",
            "years_of_experience": -5,
            "first_name": "John",
            "last_name": "Doe",
        }
        form = RedactorForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("years_of_experience", form.errors)

    def test_clean_years_of_experience_exceed_limit(self):
        form_data = {
            "username": "testuser",
            "password1": "testpassword123",
            "password2": "testpassword123",
            "years_of_experience": 70,
            "first_name": "John",
            "last_name": "Doe",
        }
        form = RedactorForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("years_of_experience", form.errors)


class NewspaperFormTest(TestCase):
    def test_clean_published_date_future(self):
        form_data = {
            "title": "Test Newspaper",
            "published_date": timezone.now().date() + timezone.timedelta(days=1),
            "publishers": [],
        }
        form = NewspaperForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("published_date", form.errors)

    def test_clean_publishers_invalid(self):
        User = get_user_model()
        user1 = User.objects.create(username="user1")
        user2 = User.objects.create(username="user2")
        user3 = User.objects.create(username="user3")
        user4 = User.objects.create(username="user4")

        form_data = {
            "title": "Test Newspaper",
            "published_date": timezone.now().date(),
            "publishers": [user1.pk, user2.pk, user3.pk, user4.pk],
        }
        form = NewspaperForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("publishers", form.errors)
