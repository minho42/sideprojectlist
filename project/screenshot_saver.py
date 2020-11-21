import cloudinary
import time
from pathlib import Path

from core.utils import get_chromedriver
from django.apps import apps
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.shortcuts import get_object_or_404


class ScreenshotSaver:
    def __init__(self):
        self.driver = get_chromedriver(headless=True)
        assert self.driver

    def save(self, project_id: int) -> None:
        Project = apps.get_model("project", "Project")
        p = get_object_or_404(Project, id=project_id)
        print(f"ScreenshotSaver.save({p.id}): {p.maker_fullname}")
        self.driver.get(p.link)
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
        p.cloudinary_screenshot_url = cloudinary_result["secure_url"]
        p.save()

    def __del__(self):
        if self.driver:
            self.driver.quit()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        if self.driver:
            self.driver.quit()
