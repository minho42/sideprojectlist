from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("u/", include("profiles.urls")),
    path("about/", views.about, name="about"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("generate-json/", views.generate_json, name="generate-json"),
    path(
        "api/save-info-for-all/",
        views.AsyncSaveInfoForAll.as_view(),
        name="save-info-for-all",
    ),
    path(
        "api/signup-count/",
        views.ChartDataSignupCount.as_view(),
        name="api_signup_count",
    ),
    path("", include("project.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# def trigger_error(request):
#     division_by_zero = 1 / 0


# urlpatterns += [
#     path("sentry-debug/", trigger_error),
# ]
