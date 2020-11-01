from allauth.account.adapter import DefaultAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialAccount
from allauth.utils import email_address_exists
from django.apps import apps
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.forms import ValidationError, forms
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.text import slugify

from sideprojectlist.models import TimeStampedModel


class CustomAccountAdapter(DefaultAccountAdapter):
    error_messages = DefaultAccountAdapter.error_messages
    error_messages["username_taken"] = "This username is already taken"
    error_messages["email_taken"] = "This email is already taken"

    # def clean_username(self, username):
    #     if len(username) > settings.ACCOUNT_USERNAME_MAX_LENGTH:
    #         raise ValidationError("Username is too long")
    #     return DefaultAccountAdapter.clean_username(
    #         self, username
    #     )  # For other default validations


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    error_messages = DefaultSocialAccountAdapter.error_messages
    error_messages[
        "email_taken"
    ] = "%s: An account already exists with this email."  # <- needs "%s"

    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        user.username = user.email.split("@")[0]

        # If user tries to login with socialaccount for the first time without signing up before,
        # it will automatically signup and login the user
        # This behaviour is unexpected, and prevented here
        # TODO Below check should only be done when in login page, but not in signup page...
        # if not user.is_signedup_with_socialauth():
        #     messages.warning(request, f"You're not signed up with '{user.email}'")
        #     raise ImmediateHttpResponse(redirect("/accounts/login/"))

        return user


class User(AbstractUser):
    # TODO make sure slug length/max_length is consistent with username
    slug = models.SlugField(max_length=100, allow_unicode=True, unique=True)
    bio = models.CharField(max_length=280, null=True, blank=True)
    website = models.URLField(max_length=200)

    class Meta:
        ordering = ["-date_joined"]

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("profiles:user", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        # if not self.id:
        # Newly created
        self.slug = slugify(self.username)
        self.email = BaseUserManager.normalize_email(self.email)
        super().save(*args, **kwargs)

    @property
    def fullname(self):
        # ? Should I use strip()?
        return f"{self.first_name} {self.last_name}"

    @property
    def initial(self):
        # ? Should I use strip()?
        initial = ""
        if len(self.first_name) > 0:
            initial = self.first_name[0]
        if len(self.last_name) > 0:
            initial += self.last_name[0]

        if not (self.first_name or self.last_name):
            initial = self.username[0]
        return initial

    @property
    def firstname_or_username(self):
        if self.first_name:
            return self.first_name
        return self.username

    def all_users_except_superuser(self):
        return User.objects.exclude(is_superuser=True).order_by("-date_joined")

    def all_users_except_me(self):
        return User.objects.exclude(id=self.id)

    def is_signedup_with_socialauth(self):
        try:
            social_user_id = SocialAccount.objects.get(user_id=self.id).user_id
            if social_user_id:
                return True
            return False
        except:
            return False

    def is_loggedin_with_socialauth(self):
        return self.is_authenticated and self.is_signedup_with_socialauth()


class Follow:
    pass