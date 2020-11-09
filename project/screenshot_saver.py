# class ScreenshotSaver:
#     pass

# import json
# import os
# import pickle
# import pprint
# import re
# from datetime import datetime, timedelta
# from json import JSONDecodeError
# from typing import Union
# import pytz
# import requests
# from asgiref.sync import async_to_sync
# from celery import Celery
# from channels.layers import get_channel_layer
# from cryptography.fernet import InvalidToken
# from django.contrib.auth import get_user_model
# from django.db import IntegrityError
# from django.shortcuts import get_object_or_404
# from django.utils import timezone
# from django.utils.timezone import make_aware
# from lxml import html
# from lxml.etree import ParserError
# from selenium.common.exceptions import (
#     NoSuchElementException,
#     TimeoutException,
#     WebDriverException,
# )
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait

# from core.utils import USER_AGENT, decrypt, get_chromedriver, timeit
# from district.models import District

# from .models import Roster


# class RosterScraper:
#     def __init__(
#         self, user_id: int, raw_start_date: str, raw_end_date: str, district: object,
#     ) -> None:
#         self.user_myself = get_object_or_404(get_user_model(), id=user_id)
#         print(f"User: {self.user_myself.username}")
#         assert len(raw_start_date) == len(raw_start_date) == 8, "Invalid date"
#         self.raw_start_date = raw_start_date
#         self.raw_end_date = raw_end_date
#         # start_date, end_date: YYYYMMDD -> YYYY/MM/DD
#         self.start = self._date_with_delimiter(raw_start_date, "/")
#         self.end = self._date_with_delimiter(raw_end_date, "/")

#         self.district = district
#         self.code = district.code

#         self.BASE_URL = f"https://{self.code}eol.ros.health.nsw.gov.au/"
#         self.authority = f"{self.code}eol.ros.health.nsw.gov.au"
#         self.login_url = f"{self.BASE_URL}EmployeeOnlineHealth/{self.code}/Login"
#         self.path = f"/EmployeeOnlineHealth/{self.code}/Roster/PersonalRoster"
#         self.personal_roster_url = (
#             f"{self.BASE_URL}EmployeeOnlineHealth/{self.code}/Roster/PersonalRoster"
#         )
#         self.referer = f"{self.BASE_URL}EmployeeOnlineHealth/{self.code}/Login"
#         self.approved_roster_url = f"{self.personal_roster_url}/GetApprovedRoster"
#         self.public_holidays_url = f"{self.personal_roster_url}/GetPublicHolidays"
#         self.pending_duties_url = f"{self.personal_roster_url}/GetDeclinedPendingDuties"

#         # To get <input name="__RequestVerificationToken" type="hidden" value="..." >
#         self.request_verification_token_xpath = (
#             "//input[@name='__RequestVerificationToken']/@value"
#         )
#         self.request_verification_token = None
#         self.channel_layer = get_channel_layer()
#         self.driver = get_chromedriver(headless=True)

#     @timeit
#     def _login_with_selenium(self) -> bool:
#         """Login to Employee Online (EOL)"""
#         # TODO driver is already checked for None before this method is called, but double checking for now
#         if not self.driver:
#             return False

#         # TODO make driver waiting time global variable e.g. DRIVER_WAIT_TIME_FOR_XXX
#         try:
#             self.driver.get(self.login_url)
#         except TimeoutException:
#             print("TimeoutException")
#             self.district.note = "TimeoutException: driver.get()"
#             self.district.save()
#             return False
#         eol_id = self.district.username
#         try:
#             eol_password = decrypt(self.district.password)
#         except InvalidToken:
#             # This happens when HEALTHROSTER_SECRET_KEY changes
#             error_message = (
#                 "Password decryption error. Please delete district and add again."
#             )
#             async_to_sync(self.channel_layer.group_send)(
#                 f"user_{self.user_myself.id}",
#                 {
#                     "type": "notification.message",
#                     "message": f"{self.district}: {error_message}",
#                 },
#             )
#             self.district.note = error_message
#             self.district.save()
#             print(error_message)
#             return False

#         assert len(eol_id) > 0 and len(eol_password) > 0

#         try:
#             el = WebDriverWait(self.driver, 15).until(
#                 EC.presence_of_element_located((By.ID, "btnLogin"))
#                 # EC.element_to_be_clickable((By.ID, "btnLogin"))
#             )
#         except NoSuchElementException:
#             print("NoSuchElementException: btnLogin")
#             self.district.note = "NoSuchElementException: btnLogin"
#             self.district.save()
#             return False
#         except TimeoutException:
#             print("TimeoutException: btnLogin")
#             self.district.note = "TimeoutException: btnLogin"
#             self.district.save()
#             return False

#         finally:
#             try:
#                 self.driver.find_element_by_id("Username").send_keys(eol_id)
#             except NoSuchElementException:
#                 print("NoSuchElementException: Username.send_keys")
#                 self.district.note = "NoSuchElementException: Username.send_keys"
#                 self.district.save()
#                 return False
#             except TimeoutException:
#                 print("TimeoutException: Username.send_keys")
#                 self.district.note = "TimeoutException: Username.send_keys"
#                 self.district.save()
#                 return False

#             try:
#                 self.driver.find_element_by_id("Password").send_keys(eol_password)
#             except NoSuchElementException:
#                 print("NoSuchElementException: Password.send_keys")
#                 self.district.note = "NoSuchElementException: Password.send_keys"
#                 self.district.save()
#                 return False
#             except TimeoutException:
#                 print("TimeoutException: Password.send_keys")
#                 self.district.note = "TimeoutException: Password.send_keys"
#                 self.district.save()
#                 return False

#             try:
#                 self.driver.find_element_by_id("btnLogin").click()
#             except NoSuchElementException:
#                 print("NoSuchElementException: btnLogin.click")
#                 self.district.note = "NoSuchElementException: btnLogin.click"
#                 self.district.save()
#                 return False
#             except TimeoutException:
#                 print("TimeoutException: btnLogin.click")
#                 self.district.note = "TimeoutException: btnLogin.click"
#                 self.district.save()
#                 return False

#             try:
#                 el = WebDriverWait(self.driver, 15).until(
#                     EC.presence_of_element_located((By.CLASS_NAME, "logout"))
#                 )
#             finally:
#                 if "Logout" in self.driver.page_source:
#                     print(f"Logged in with selenium")
#                     return True
#                 else:
#                     print("Login failed with selenium")

#                     if "Invalid username" in self.driver.page_source:
#                         # "Invalid username or password"
#                         error_message = "Invalid username or password"
#                         async_to_sync(self.channel_layer.group_send)(
#                             f"user_{self.user_myself.id}",
#                             {
#                                 "type": "notification.message",
#                                 "message": f"{self.district}: {error_message}",
#                             },
#                         )
#                         self.district.note = error_message
#                         self.district.is_locked = True
#                         self.district.save()
#                         print(error_message)

#                     elif (
#                         "maintain" in self.driver.page_source.lower()
#                         or "maintenance" in self.driver.page_source.lower()
#                     ):
#                         # TODO Check exact maintenance message
#                         error_message = "Under maintenance..."
#                         async_to_sync(self.channel_layer.group_send)(
#                             f"user_{self.user_myself.id}",
#                             {
#                                 "type": "notification.message",
#                                 "message": f"{self.district}: ${error_message}",
#                             },
#                         )
#                         self.district.note = error_message
#                         self.district.save()
#                         print(error_message)
#                     elif "suspended" in self.driver.page_source.lower():
#                         # "Your account has been suspended; please contact the system administrator."
#                         # TODO
#                         error_message = "Your account has been suspended. Try again later or contact the system administrator."
#                         async_to_sync(self.channel_layer.group_send)(
#                             f"user_{self.user_myself.id}",
#                             {
#                                 "type": "notification.message",
#                                 "message": f"{self.district}: ${error_message}",
#                             },
#                         )
#                         self.district.note = error_message
#                         self.district.save()
#                         print(error_message)
#                     else:
#                         # TODO What are the other reasons login could fail...
#                         error_message = "Login failed for some reason"
#                         async_to_sync(self.channel_layer.group_send)(
#                             f"user_{self.user_myself.id}",
#                             {
#                                 "type": "notification.message",
#                                 "message": f"{self.district}: ${error_message}",
#                             },
#                         )
#                         self.district.note = error_message
#                         self.district.save()
#                         print(error_message)

#                     return False

#     def _date_with_delimiter(self, date: str, delimiter: str = "/") -> str:
#         return f"{date[:4]}{delimiter}{date[4:6]}{delimiter}{date[-2:]}"

#     def _convert_date_to_australian(self, str_date: str) -> str:
#         """
#         2017/07/28 -> 28/Jul/2017 or 28/Jul
#         """
#         # TODO Make this generic so can be used elsewhere
#         datetime_date = datetime.strptime(str_date, "%Y/%m/%d")
#         current_year = datetime.now().year

#         if datetime_date.year == current_year:
#             date_format = "%d/%b"
#         else:
#             date_format = "%d/%b/%Y"

#         return datetime_date.strftime(date_format)

#     @timeit
#     def _delete_all(self) -> None:
#         """
#         In DB, dates are saved as utc.
#         Therefore, query filtering needs to be as utc

#         E.g.
#         self.raw_start_date: "20200317"
#         -> start of day as utc for 'start' field: datetime.datetime(2020, 3, 17, 2, 30, tzinfo=<UTC>)
#         -> end of day as utc for 'start' field: datetime.datetime(2020, 3, 17, 13, 0, tzinfo=<UTC>)
#         Filtering between above two dates for 'start' field.
#         """

#         Roster.objects.filter(user=self.user_myself).filter(
#             district=self.district
#         ).filter(
#             start__gte=datetime.strptime(self.raw_start_date, "%Y%m%d").astimezone(
#                 pytz.utc
#             )
#         ).filter(
#             start__lt=datetime.strptime(self.raw_end_date, "%Y%m%d").astimezone(
#                 pytz.utc
#             )
#             + timedelta(days=1)
#         ).delete()

#     @timeit
#     def _login_with_cookies(self, session) -> bool:
#         s = session
#         dis = get_object_or_404(District, id=self.district.id)
#         print(f"District: {dis.slug}")

#         if dis.last_cookies:
#             s.cookies = pickle.loads(dis.last_cookies)
#         else:
#             print(f"District has no 'last_cookies'")
#             return False
#         if len(s.cookies) < 1:
#             print("No cookies found")
#             return False
#         print("Cookies found")

#         self.request_verification_token = self._get_request_verification_token(s)
#         if not self.request_verification_token:
#             return False

#         print("Login with cookies success")
#         return True

#     def _save_cookies(self, session):
#         dis = get_object_or_404(District, id=self.district.id)
#         dis.last_cookies = pickle.dumps(session.cookies)
#         dis.save()

#     def _get_request_verification_token(self, session) -> Union[str, None]:
#         get_headers = {
#             "authority": self.authority,
#             "method": "GET",
#             "path": self.path,
#             "scheme": "https",
#             "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
#             "accept-encoding": "gzip, deflate, br",
#             "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
#             "cache-control": "max-age=0",
#             "referer": self.referer,
#             "sec-fetch-mode": "navigate",
#             "sec-fetch-site": "same-origin",
#             "sec-fetch-user": "?1",
#             "upgrade-insecure-requests": "1",
#             "user-agent": USER_AGENT,
#         }
#         r = session.get(self.personal_roster_url, headers=get_headers)
#         if not r.ok:
#             return None

#         try:
#             node = html.fromstring(r.content)
#         except ParserError:
#             return None

#         try:
#             request_verification_token = node.xpath(
#                 self.request_verification_token_xpath
#             )[0]
#         except IndexError:
#             print("No '__RequestVerificationToken' xpath found")
#             return None

#         if len(request_verification_token) < 1:
#             print("No '__RequestVerificationToken' found")
#             return None

#         return request_verification_token

#     @timeit
#     def fetch(self) -> bool:
#         s = requests.session()

#         if not self._login_with_cookies(s):
#             # print("Login with cookies failed")

#             # TODO Check where this "self.driver" check should reside in case of None
#             if not self.driver:
#                 error_message = (
#                     f"Something went wrong (driver missing). Try again later."
#                 )
#                 self.district.is_last_login_success = False
#                 self.district.note = error_message
#                 async_to_sync(self.channel_layer.group_send)(
#                     f"user_{self.user_myself.id}",
#                     {
#                         "type": "notification.message",
#                         "message": f"{self.district}: {error_message}",
#                     },
#                 )
#                 self.district.save()
#                 return False

#             if not self._login_with_selenium():
#                 self.district.is_last_login_success = False
#                 # note is filled inside _login_with_selenium
#                 # self.district.note = "Login failed for some reason."
#                 self.district.save()
#                 if self.driver:
#                     self.driver.quit()
#                 return False

#             # Needs to set cookies in requests.session before visiting 'PersonalRoster' for '__RequestVerificationToken'
#             for cookie in self.driver.get_cookies():
#                 s.cookies.set(cookie["name"], cookie["value"])

#             self.request_verification_token = self._get_request_verification_token(s)

#         self._set_fullname_if_empty(session=s)

#         # TODO is it too early to say it's successful here?
#         self.district.is_last_login_success = True
#         self.district.note = f"Last sync dates: {self._convert_date_to_australian(self.start)} - {self._convert_date_to_australian(self.end)}"
#         self.district.save()

#         self._save_cookies(s)

#         data = {
#             "start": self._date_with_delimiter(self.raw_start_date, "/"),
#             "end": self._date_with_delimiter(self.raw_end_date, "/"),
#             "showCancelledDuties": "true",
#         }

#         post_headers = {
#             "__RequestVerificationToken": self.request_verification_token,
#             "Accept": "application/json, text/javascript, */*; q=0.01",
#             "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
#             "Referer": self.personal_roster_url,
#             "Sec-Fetch-Mode": "cors",
#             "User-Agent": USER_AGENT,
#             "X-Requested-With": "XMLHttpRequest",
#         }

#         r = s.post(self.approved_roster_url, data=data, headers=post_headers)
#         if not r.ok:
#             self.district.is_last_login_success = False
#             error_message = (
#                 f"{r.status_code} error from Employee Online. Try again later."
#             )
#             self.district.note = error_message
#             self.district.save()
#             if self.driver:
#                 self.driver.quit()

#             async_to_sync(self.channel_layer.group_send)(
#                 f"user_{self.user_myself.id}",
#                 {
#                     "type": "notification.message",
#                     "message": f"{self.district}: {error_message}",
#                 },
#             )
#             return False
#         try:
#             approved_roster = json.loads(r.text)
#         except JSONDecodeError:
#             self.district.is_last_login_success = False
#             error_message = f"Something went wrong (JSONDecodeError). Try again later."
#             self.district.note = error_message
#             self.district.save()
#             if self.driver:
#                 self.driver.quit()
#             async_to_sync(self.channel_layer.group_send)(
#                 f"user_{self.user_myself.id}",
#                 {
#                     "type": "notification.message",
#                     "message": f"{self.district}: {error_message}",
#                 },
#             )
#             return False

#         print(f"start: {self.raw_start_date}, end: {self.raw_end_date}")
#         self._delete_all()

#         for duty in approved_roster["duties"]:
#             # pprint.pprint(duty)

#             start = datetime.strptime(duty["dutyStart"], "%Y-%m-%dT%H:%M:%S")
#             start = make_aware(start, is_dst=False)
#             end = datetime.strptime(duty["dutyEnd"], "%Y-%m-%dT%H:%M:%S")
#             end = make_aware(end, is_dst=False)
#             title = duty["title"]
#             hours = duty["workTime"]["TotalHours"]
#             is_incharge = duty["isInCharge"]
#             work_unit = duty["workUnit"]
#             is_detached = duty["isDetached"]
#             has_overtime = duty["hasOvertime"]
#             is_submitted = duty["isSubmitted"]
#             is_cancelled = duty["isCancelled"]

#             coworkers = []
#             for grouping in duty["assignedStaffGroupings"]:
#                 # TODO Add resourceRequirementSummary with alsoAssignedPersons as dictionary
#                 for person in grouping["alsoAssignedPersons"]:
#                     coworkers.append(person["displayName"])
#             coworkers = json.dumps(sorted(coworkers))
#             # json.decoder.JSONDecoder().decode(jsonified_string) # Decoding jsonified string back to python list
#             # print(coworkers)

#             try:
#                 Roster.objects.create(
#                     user=self.user_myself,
#                     district=get_object_or_404(District, id=self.district.id),
#                     start=start,
#                     title=title,
#                     end=end,
#                     hours=hours,
#                     is_incharge=is_incharge,
#                     work_unit=work_unit,
#                     is_detached=is_detached,
#                     has_overtime=has_overtime,
#                     is_submitted=is_submitted,
#                     is_cancelled=is_cancelled,
#                     coworkers=coworkers,
#                     modified=timezone.now(),
#                 )
#             except IntegrityError as e:
#                 # TODO Check how many has created and then decide success/fail
#                 # TODO Needs to record/log error message somewhere so can be chased
#                 pass

#         # nonEffectives e.g. leaves
#         for noneffective in approved_roster["nonEffectives"]:
#             title = noneffective["title"]
#             # hours = noneffective["duration"]["TotalHours"]

#             # Continuous leaves are combined on EOL and hours noted are the total hours combined from the continuous days of leaves
#             # e.g. 5 weeks of annual leave: 200 hours => 8 hour x 5 days/week x 5 weeks = 200
#             # This is tricky to get the average hour for each day because roster shows 7 days/week as annual leave while hours are calculated with 5 days/wweek
#             # If all the displayed leaves are counted for: hours can be calculated as below
#             # hours_for_each_day = noneffective["duration"]["TotalHours"] / (end - start).days
#             # Until this is figured out, hours won't be saved for nonEffectives for now

#             start = datetime.strptime(noneffective["start"], "%Y-%m-%dT%H:%M:%S")
#             start = make_aware(start, is_dst=False)
#             end = datetime.strptime(noneffective["end"], "%Y-%m-%dT%H:%M:%S")
#             end = make_aware(end, is_dst=False)

#             this_date = start
#             while this_date < end:
#                 try:
#                     Roster.objects.create(
#                         user=self.user_myself,
#                         district=get_object_or_404(District, id=self.district.id),
#                         start=this_date,
#                         title=title,
#                         end=this_date,
#                         # hours=hours,
#                         modified=timezone.now(),
#                     )
#                     this_date += timedelta(days=1)
#                 except IntegrityError as e:
#                     # TODO Check how many has created and then decide success/fail
#                     # TODO Needs to record/log error message somewhere so can be chased
#                     pass

#         if approved_roster and len(approved_roster) < 1:
#             print("Nothing fetched")
#         # print(approved_roster)

#         if self.driver:
#             self.driver.quit()

#         return True

#     def _set_fullname_if_empty(self, session):
#         if not self.user_myself.first_name + self.user_myself.last_name:
#             # Save name if not set; assumes last word as last_name
#             # TODO reduce this duplicate headers
#             get_headers = {
#                 "authority": self.authority,
#                 "method": "GET",
#                 "path": self.path,
#                 "scheme": "https",
#                 "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
#                 "accept-encoding": "gzip, deflate, br",
#                 "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
#                 "cache-control": "max-age=0",
#                 "referer": self.referer,
#                 "sec-fetch-mode": "navigate",
#                 "sec-fetch-site": "same-origin",
#                 "sec-fetch-user": "?1",
#                 "upgrade-insecure-requests": "1",
#                 "user-agent": USER_AGENT,
#             }
#             r = session.get(self.personal_roster_url, headers=get_headers)
#             if not r.ok:
#                 return False
#             try:
#                 node = html.fromstring(r.content)
#             except ParserError:
#                 return False
#             try:
#                 user_fullname = node.xpath("//li[@class='user']")[0].text
#                 # print(user_fullname)
#                 (
#                     self.user_myself.first_name,
#                     _,
#                     self.user_myself.last_name,
#                 ) = user_fullname.rpartition(" ")
#                 self.user_myself.save()
#             except IndexError:
#                 print("User's fullname not found")
#                 return False
#         return True

#     def __del__(self):
#         if self.driver:
#             self.driver.quit()

#     def __enter__(self):
#         return self

#     def __exit__(self, *exc):
#         if self.driver:
#             self.driver.quit()
