from allauth.socialaccount.models import SocialAccount
from core.utils import staff_check
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import UserUpdateForm
from .models import User


@login_required
def profile(request, slug):
    template = "profiles/profile.html"
    user = get_object_or_404(User, slug=slug)

    # superuser shouldn't be visible to anyone else
    superuser = get_object_or_404(User, is_superuser=True)
    if slug == superuser.slug and request.user.slug != slug:
        raise Http404

    context = {"u": user}
    return render(request, template, context)


@login_required
def delete(request, slug):
    template = "profiles/profile_confirm_delete.html"
    user = get_object_or_404(User, id=request.user.id)
    context = {"u": user}

    if request.method == "POST":
        user.delete()
        messages.success(request, f"Account deleted")
        return HttpResponseRedirect(reverse("home"))

    return render(request, template, context)


# https://simpleisbetterthancomplex.com/tips/2016/08/04/django-tip-9-password-change-form.html
@login_required
def change_password(request, slug):
    # Users with socialauth login is not supposed to change password inside app
    if request.user.is_loggedin_with_socialauth():
        provider = SocialAccount.objects.get(user_id=request.user.id).provider
        msg = f"You are not supposed to change password in this website as you are logged in with {provider}."
        raise PermissionDenied(msg)

    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed")
            return redirect(reverse("profiles:user", args=[user.slug]))
        else:
            print("Password form not valid")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "profiles/profile_change_password.html", {"form": form})


@login_required
def update(request, slug):
    if request.method == "POST":
        user = request.user
        form = UserUpdateForm(request.POST, instance=request.user)

        if form.is_valid():
            changed_list = []
            if form.has_changed():
                # messages.success(request, f'Profile updated: {form.changed_data}')
                changed_list = form.changed_data

            # msg = "Profile updated: " + ", ".join(changed_list)
            # messages.success(request, msg)
            # TODO "Profile updated" vs "Profile edited"
            messages.success(request, "Profile updated")
            try:
                form.save()
            except IntegrityError:
                messages.error(request, "Profile update failed...")
            return HttpResponseRedirect(reverse("profiles:user", args=[user.slug]))
        else:
            print("Update form not valid")

    else:
        form = UserUpdateForm(instance=request.user)

    context = {"form": form}
    template = "profiles/profile_update.html"
    return render(request, template, context)
