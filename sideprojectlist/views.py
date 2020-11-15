from datetime import timedelta

from core.utils import staff_check
from django.contrib.auth.decorators import user_passes_test
from django.db.models.functions import TruncDate
from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone
from profiles.models import User
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from project.tasks import save_info_for_all
from rest_framework.response import Response
from sideprojectlist.celery import app
from project.models import Project


def home(request):
    template = "home.html"
    context = {}
    return render(request, template, context)


def about(request):
    template = "about.html"
    return render(request, template)


class AsyncSaveInfoForAll(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return async_save_info_for_all(request)


@user_passes_test(staff_check)
def async_save_info_for_all(request):
    save_info_for_all.apply_async(
        args=(),
        link=success_callback_for_async_save_info_for_all.s(),
        link_error=None,
    )
    return Response([{"response": "OK"}])


@app.task
def success_callback_for_async_save_info_for_all(response):
    print("success_")
    pass


@user_passes_test(staff_check)
def dashboard(request):
    template = "dashboard.html"
    context = {}

    user_count = (
        User.objects.exclude(is_superuser=True).exclude(is_active=False).count()
    )
    count_maker_bio_not_saved = Project.objects.filter(
        ~Q(twitter_handle=None) & Q(maker_bio=None)
    ).count()
    count_screenshot_not_saved = Project.objects.filter(screenshot=None).count()

    context["user_count"] = user_count
    context["count_maker_bio_not_saved"] = count_maker_bio_not_saved
    context["count_screenshot_not_saved"] = count_screenshot_not_saved

    return render(request, template, context)


class ChartDataSignupCount(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        data = get_api_data_signup_count()
        return Response(data)


def get_api_data_signup_count():
    created = list(
        User.objects.annotate(date=TruncDate("date_joined"))
        .values("date")
        .distinct()
        .order_by("date")
    )

    for c in created:
        c["count"] = (
            User.objects.filter(date_joined__gte=c["date"])
            .filter(date_joined__lt=c["date"] + timedelta(days=1))
            .count()
        )
    fill_null_in_the_gap(created, "count", 0)
    created = sorted(created, key=lambda k: k["date"])
    data = {
        "dates": [c["date"] for c in created],
        "counts": [c["count"] for c in created],
    }

    return data


def _add_day(date):
    return date + timedelta(days=1)


def _is_this_date_in_list(date, list_source):
    # return set(['YES' for d in list_source if d['date'] == date])
    for d in list_source:
        if d["date"] == date:
            return True
    return False


def _get_dates_to_fill(created, first_date, last_date):
    result = []
    this_date = first_date
    while this_date <= last_date:
        this_date = _add_day(this_date)
        if not _is_this_date_in_list(this_date, created):
            result.append(this_date)
    return result


def fill_null_in_the_gap(created, label, value_to_fill=None):
    assert created

    first_date = created[0]["date"]
    last_date = timezone.now().date()
    dates = _get_dates_to_fill(created, first_date, last_date)

    if dates:
        for date in dates:
            created.append({"date": date, label: value_to_fill})
