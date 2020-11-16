import re

from django import forms
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from allauth.account.forms import LoginForm, ResetPasswordForm, SignupForm
from allauth.account.utils import filter_users_by_email
from allauth.socialaccount.models import SocialAccount

# from crispy_forms.helper import FormHelper
# from uploads.core.models import Document
# from django.contrib.auth.forms import UserCreationForm
from .models import User

USERNAME_HELP_TEXT = "Alphanumeric characters (a-z, 0-9) and underscore (_)"


def profile_username_validation(username):
    if re.findall(r"[^a-zA-Z0-9_]", username):
        raise forms.ValidationError(f"{USERNAME_HELP_TEXT} only")


class UserCreationForm(SignupForm):
    """
    Custom class is used primarily to change username validation to limit special characters
    """

    # Copied from allauth.account.forms.py and changed
    # TODO catch exception: settings.ACCOUNT_USERNAME_MIN_LENGTH not defined
    email = forms.EmailField(
        label="Email",
        required=settings.ACCOUNT_EMAIL_REQUIRED,
        widget=forms.TextInput(
            attrs={"type": "email", "size": "30", "placeholder": "Email"}
        ),
        help_text="",
    )

    username = forms.CharField(
        label="Username",
        min_length=settings.ACCOUNT_USERNAME_MIN_LENGTH,
        widget=forms.TextInput(attrs={"placeholder": "Username"}),
        help_text="",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].label = "Email"
        self.fields["email"].placeholder = "Email"

    def clean_username(self):
        super().clean_username()
        username = self.cleaned_data.get("username")
        profile_username_validation(username)
        return username


class LoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["login"].label = "Email"
        # TODO How to change placeholder for email
        # Try to override allauth.account.forms.AddEmailForm?
        # self.fields["login"].placeholder = "Email"  # <-- not working

    def clean_login(self):
        email = self.cleaned_data["login"]
        try:
            user = User.objects.get(email=email)
            if user.is_signedup_with_socialauth():
                social = SocialAccount.objects.get(user_id=user.id)
                raise forms.ValidationError(
                    f"You are signed up with {social.provider.capitalize()}. Please use 'Log in with {social.provider.capitalize()}'"
                )
        except ObjectDoesNotExist:
            pass

        return super().clean_login()


class UserUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True
        # self.fields.keyOrder = []
        self.fields["username"].help_text = USERNAME_HELP_TEXT

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "bio", "website"]
        widgets = {"bio": forms.Textarea(attrs={"rows": 2})}

    def clean_username(self):
        username = self.cleaned_data.get("username")
        profile_username_validation(username)
        return username


class UserResetPasswordForm(ResetPasswordForm):
    def clean_email(self):

        email = self.cleaned_data["email"]
        users = filter_users_by_email(email)
        if len(users) == 1:
            try:
                social = SocialAccount.objects.get(user_id=users[0].id)
                if social:
                    raise forms.ValidationError(
                        f"You are signed up with {social.provider.capitalize()}. You are not supposed to reset password on this site."
                    )
            except ObjectDoesNotExist:
                pass

        return super().clean_email()
