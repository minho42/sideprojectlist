from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.apps import apps

from .screenshot_saver import ScreenshotSaver
from .twitter_saver import TwitterSaver


@shared_task
def save_info(project_id: int, screenshot=True, twitter_info=True) -> None:
    if screenshot:
        with ScreenshotSaver() as ss:
            ss.save(project_id)

    ts = TwitterSaver()
    if twitter_info:
        ts.save_followers_count(project_id)
        ts.save_profile_image(project_id)

    # TODO call generate_json here for automation
    # TODO check permission or catch permission exception
    # generate_json()


@shared_task
def save_info_for_all(screenshot=True, twitter_info=True) -> None:
    Project = apps.get_model("project", "Project")
    total = Project.objects.count()
    for p in Project.objects.order_by("maker_fullname"):
        # print(f"{index+1}/{total}")
        save_info(p.id, screenshot, twitter_info)
