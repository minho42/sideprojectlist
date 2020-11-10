from __future__ import absolute_import, unicode_literals

from celery import shared_task

from .screenshot_saver import ScreenshotSaver


@shared_task
def save_screenshot(project_id):
    with ScreenshotSaver() as SS:
        SS.save(project_id)
