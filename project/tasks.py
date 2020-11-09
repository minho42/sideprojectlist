from __future__ import absolute_import, unicode_literals

from celery import shared_task
from project.models import Project


@shared_task
def save_sreenshot():
    pass


# from celery.exceptions import MaxRetriesExceededError, SoftTimeLimitExceeded
# @shared_task(default_retry_delay=3 * 60, max_retries=3)
# @shared_task
# def get_all_roster(user_id: int, start: str, end: str):
#     for district in District.objects.filter(user__id=user_id).exclude(is_locked=True):
#         with RosterScraper(user_id, start, end, district) as RS:
#             if RS.fetch():
#                 generate_stats(user_id, district)
