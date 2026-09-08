from django import forms

from .models import Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "admission_number",
            "first_name",
            "middle_name",
            "last_name",
            "date_of_birth",
            "gender",
            "address",
            "date_of_registration",
        ]
        widgets = {
            "admission_number": forms.TextInput(attrs={"placeholder": "e.g. STU-0042"}),
            "first_name": forms.TextInput(attrs={"placeholder": "Amara"}),
            "middle_name": forms.TextInput(attrs={"placeholder": "Optional"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Okonkwo"}),
            "address": forms.TextInput(attrs={"placeholder": "Optional"}),
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
            "date_of_registration": forms.DateInput(attrs={"type": "date"}),
        }
