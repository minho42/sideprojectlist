"""sideprojectlist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path("aaronisawesometoo/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("u/", include("profiles.urls")),
    path("about/", views.about, name="about"),
    path("dashboard/", views.dashboard, name="dashboard"),
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
    # path("", views.home, name="home"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns += [
    path("sentry-debug/", trigger_error),
]
