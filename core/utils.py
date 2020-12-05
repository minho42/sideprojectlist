import os
import time
from functools import wraps
from typing import List, Union

import requests
from django.conf import settings
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.http import Http404
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"


def add_q_auto_to_url(url: str) -> str:
    if not url:
        return
    return url.replace("/upload/", "/upload/q_auto/")


def save_image_from_url_to_local(url: str, filename=None) -> bool:
    headers = {"User-Agent": USER_AGENT}
    r = requests.get(url, headers=headers)

    if r.status_code != requests.codes.ok:
        return False
    if not filename:
        return False

    with open(filename, "wb") as file:
        file.write(r.content)
    return True


def save_image_from_url(field, url: str, filename=None) -> bool:
    headers = {"User-Agent": USER_AGENT}
    r = requests.get(url, headers=headers)

    if r.status_code != requests.codes.ok:
        return False

    temp = NamedTemporaryFile(delete=True)
    temp.write(r.content)
    temp.flush()

    if not filename:
        filename = os.path.basename(url)

    field.save(filename, File(temp), save=True)
    return True


def get_chromedriver(headless: bool = True) -> Union[object, None]:
    options = webdriver.ChromeOptions()
    # prefs = {"profile.managed_default_content_settings.images": 2}
    # options.add_experimental_option("prefs", prefs)
    if headless:
        options.add_argument("headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(
        "--remote-debugging-port=9222"
    )  # Trying to fix WebDriverException("unknown error: DevToolsActivePort file doesn't exist", None, None)
    # options.add_argument("--window-size=2560,5120")
    options.add_argument("window-size=2560,5120")
    # options.add_argument("--start-maximized")

    try:
        driver = webdriver.Chrome(
            os.environ.get("CHROME_DRIVER_PATH"), options=options,
        )
        driver.set_window_size(1024, 768)
        # if settings.DEBUG:
        #     driver = webdriver.Chrome(
        #         os.environ.get("CHROME_DRIVER_PATH"),
        #         options=options,
        #     )
        #     driver.set_window_size(1024, 768)
        # else:
        #     # Heroku
        #     options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

        #     driver = webdriver.Chrome(
        #         executable_path=os.environ.get("CHROME_DRIVER_PATH"),
        #         chrome_options=options,
        #     )
        #     driver.set_window_size(1024, 768)

    except WebDriverException as e:
        # TODO Needs to record/log error message somewhere so can be chased
        print("WebDriverException")
        print(str(e))
        driver = None

    return driver


def timeit(func):
    @wraps(func)
    def closure(*args, **kwargs):
        ts = time.time()
        result = func(*args, **kwargs)
        te = time.time()
        print("<%s> took %0.3fs." % (func.__name__, te - ts))
        return result

    return closure


def get_all_fields(model) -> List[str]:
    # print('---------------------------')
    # pprint.pprint(model._meta.__dict__)
    # print('---------------------------')

    r = []
    try:
        # r = [f.name for f in model._meta.__dict__["local_fields"]]
        r = [f.name for f in model._meta.local_fields]
    except KeyError:
        pass
    else:
        pass
    return r


def get_all_fields_excluding(model, exclude_list: List[str]) -> List[str]:
    if type(exclude_list) is not list:
        raise TypeError("exclude_list must be list")

    include_list = get_all_fields(model)

    for i in include_list:
        for e in exclude_list:
            e = e.strip()
            if e in include_list:
                include_list.remove(e)

    return include_list


def superuser_check(user: object) -> Union[bool, object]:
    """To be used as parameter for @user_passes_test
    View is only available for superuser otherwise raise 404"""
    if user.is_superuser:
        return True
    raise Http404()


def staff_check(user: object) -> Union[bool, object]:
    """To be used as parameter for @user_passes_test
    View is only available for staff otherwise raise 404"""
    if user.is_staff:
        return True
    raise Http404()
