from django import forms

from .models import SchoolClass


class SchoolClassForm(forms.ModelForm):
    class Meta:
        model = SchoolClass
        fields = ["name", "nickname", "description"]
        widgets = {
            "nickname": forms.TextInput(attrs={"placeholder": "Optional, e.g. Eagles"}),
            "description": forms.TextInput(attrs={"placeholder": "Optional"}),
        }
