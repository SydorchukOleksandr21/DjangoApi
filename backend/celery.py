import os

from celery import Celery, shared_task
from django.conf import settings
from django.core.mail import send_mail

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


@shared_task
def send_event_registration_email(
        user_email: str,
        event_title: str,
        event_date_str: str,
        event_location: str
) -> None:
    """
    Sends email to user after registration
    """
    subject = f"Registration confirmed: {event_title}"

    message = (
        f"You have successfully registered for the event: {event_title} "
        f"({event_date_str}, {event_location}). "
        f"If this was a mistake, you can cancel registration at any time."
    )

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=False
    )
