from celery import Celery
from celery.schedules import timedelta
from config import CELERY_BROKER_URL

def make_celery():
    celery = Celery(
        "user_management_service",
        broker=CELERY_BROKER_URL,
        backend=CELERY_BROKER_URL,
        include=["services.notification_service"]
    )

    # Periodic Task Scheduling
    celery.conf.beat_schedule = {
        "send_pending_verifications_every_5s": {
            "task": "services.notification_service.send_pending_verifications",
            "schedule": timedelta(seconds=5),  # Run every 5 seconds
        },
    }

    celery.conf.timezone = "UTC"
    return celery

celery = make_celery()
