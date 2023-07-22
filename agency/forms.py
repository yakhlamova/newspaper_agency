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
            "published_date": forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_published_date(self):
        published_date = self.cleaned_data.get("published_date")

        if published_date and published_date > timezone.now().date():
            raise forms.ValidationError("Published date cannot be in the future.")

        return published_date
