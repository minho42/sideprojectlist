from __future__ import absolute_import, unicode_literals

from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_mail_with_celery(
    subject, message, from_email, recipient_list, fail_silently=False
):
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=fail_silently,
        )
    except:
        print("send_mail_with_celery failed")
        # TODO Do some proper error handling
        pass
