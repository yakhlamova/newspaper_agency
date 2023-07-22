from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

from agency.models import Redactor, Newspaper


class RedactorCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Redactor
        fields = UserCreationForm.Meta.fields + (
            "years_of_experience",
            "first_name",
            "last_name"
        )

    def clean_years_of_experience(self):
        years_of_experience = self.cleaned_data.get("years_of_experience")

        if years_of_experience:
            if years_of_experience < 0:
                raise forms.ValidationError("Years of experience cannot be less than 0.")
            elif years_of_experience > 60:
                raise forms.ValidationError("Years of experience cannot be more than 60.")

        return years_of_experience


class RedactorSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by username"})
    )


class NewspaperForm(forms.ModelForm):
    publishers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Newspaper
        fields = "__all__"
        widgets = {
            "published_date": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_published_date(self):
        published_date = self.cleaned_data.get("published_date")

        if published_date and published_date > timezone.now().date():
            raise forms.ValidationError("Published date cannot be in the future.")

        return published_date

    def clean_publishers(self):
        publishers = self.cleaned_data.get("publishers")

        if not publishers or len(publishers) > 3:
            raise forms.ValidationError("Please choose from 1 to 3 publishers.")

        return publishers


class NewspaperSearchForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by title"})
    )


class TopicSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"})
    )
