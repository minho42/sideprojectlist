from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.apps import apps

from .screenshot_saver import ScreenshotSaver
from .twitter_saver import TwitterSaver


@shared_task
def save_info(project_id: int, screenshot=True, avatar=True, bio=True) -> None:
    if screenshot:
        with ScreenshotSaver() as ss:
            ss.save(project_id)

    ts = TwitterSaver()
    if bio:
        ts.save_bio(project_id)
    if avatar:
        ts.save_profile_image(project_id)

    # TODO call generate_json here for automation
    # TODO check permission or catch permission exception
    # generate_json()


@shared_task
def save_info_for_all(screenshot=True, avatar=True, bio=True) -> None:
    Project = apps.get_model("project", "Project")
    total = Project.objects.count()
    for p in Project.objects.all():
        # print(f"{index+1}/{total}")
        save_info(p.id, screenshot=True, avatar=True, bio=True)
