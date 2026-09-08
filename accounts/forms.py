from allauth.account.forms import SignupForm
from django import forms


class CustomSignupForm(SignupForm):
    """
    Extends allauth's SignupForm with first/last name, so the values
    collected on the sign-up page actually get saved onto the user.
    """
    first_name = forms.CharField(max_length=150, label="First name")
    last_name = forms.CharField(max_length=150, label="Last name")

    field_order = ["first_name", "last_name", "email", "password1", "password2"]

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.save()
        return user
