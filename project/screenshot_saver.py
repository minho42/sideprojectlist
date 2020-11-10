import time

from core.utils import get_chromedriver
from django.apps import apps
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.shortcuts import get_object_or_404


class ScreenshotSaver:
    def __init__(self):
        self.driver = get_chromedriver(headless=True)

    def save(self, project_id):
        Project = apps.get_model("project", "Project")
        p = get_object_or_404(Project, id=project_id)
        self.driver.get(p.link)
        time.sleep(4)
        raw_image = self.driver.get_screenshot_as_png()
        temp = NamedTemporaryFile(delete=True)
        temp.write(raw_image)
        temp.flush()
        # This triggers infinite loop of post_save signals
        p.screenshot.save(p.slug, File(temp), save=True)

    def __del__(self):
        if self.driver:
            self.driver.quit()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        if self.driver:
            self.driver.quit()
