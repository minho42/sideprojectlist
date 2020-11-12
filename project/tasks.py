from __future__ import absolute_import, unicode_literals

from celery import shared_task

from .screenshot_saver import ScreenshotSaver
from .twitter_saver import TwitterSaver


@shared_task
def save_screenshot(project_id):
    with ScreenshotSaver() as SS:
        SS.save(project_id)

    ts = TwitterSaver()
    ts.save_bio(project_id)
    ts.save_profile_image(project_id)