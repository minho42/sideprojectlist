from __future__ import absolute_import, unicode_literals

from celery import shared_task
from django.apps import apps

from .screenshot_saver import ScreenshotSaver
from .twitter_saver import TwitterSaver


@shared_task
def save_info(project_id):
    with ScreenshotSaver() as SS:
        SS.save(project_id)

    ts = TwitterSaver()
    ts.save_bio(project_id)
    ts.save_profile_image(project_id)


@shared_task
def save_info_for_all():
    Project = apps.get_model("project", "Project")
    for p in Project.objects.all():
        save_info(p.id)
