import time
from pathlib import Path

import cloudinary
from core.utils import add_q_auto_to_url, get_chromedriver
from django.apps import apps
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.shortcuts import get_object_or_404
from selenium.common.exceptions import WebDriverException


class ScreenshotSaver:
    def __init__(self):
        self.driver = get_chromedriver(headless=True)
        assert self.driver

    def save(self, project_id: int) -> None:
        Project = apps.get_model("project", "Project")
        p = get_object_or_404(Project, id=project_id)
        print(f"ScreenshotSaver.save({p.id}): {p.maker_fullname}")
        try:
            self.driver.get(p.link)
        except WebDriverException:
            print(f"WebDriverException getting [{p.maker_fullname}]: {p.link}")
            # TODO: Remove previous files on local and cloudinary
            return
        time.sleep(4)
        raw_image = self.driver.get_screenshot_as_png()
        temp = NamedTemporaryFile(delete=True)
        temp.write(raw_image)
        temp.flush()
        # This triggers infinite loop of post_save signals
        p.screenshot.save(p.slug, File(temp), save=True)

        # SIDEPROJECT_DIR = Path(__file__).resolve().parent.parent.parent
        # FRONTEND_BASE_DIR = SIDEPROJECT_DIR / "sideprojectlist-frontend"
        # FRONTEND_IMAGE_PATH = FRONTEND_BASE_DIR / ""

        # path = static(f"images/screenshots/{p.slug}.png")
        BASE_DIR = Path(__file__).resolve().parent.parent
        IMAGE_DIR = BASE_DIR / "static/images"
        path = f"{IMAGE_DIR}/screenshot_{p.slug}.png"
        # print(path)
        # self.driver.save_screenshot(path)
        self.driver.get_screenshot_as_file(path)

        # TODO catch FileNotFoundError
        cloudinary_result = cloudinary.uploader.upload(
            path,
            use_filename=True,
        )
        p.cloudinary_screenshot_url = add_q_auto_to_url(cloudinary_result["secure_url"])
        p.save()

    def __del__(self):
        if self.driver:
            self.driver.quit()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        if self.driver:
            self.driver.quit()
