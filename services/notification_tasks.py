import redis
from celery import shared_task
from services.notification_service import NotificationService

# Configure Redis connection
redis_client = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)

@shared_task
def send_pending_verifications():
    """Celery task to check for pending email verifications every 5 seconds"""
    keys = redis_client.keys("user:*:email_pending")

    for key in keys:
        user_id = key.split(":")[1]
        email = redis_client.get(key)

        # Send verification email
        NotificationService.send_email_verification(user_id, email)

        # Remove key from Redis after sending
        redis_client.delete(key)

@shared_task
def send_forgot_password_email(email, reset_token):
    """Celery task to send password reset email"""
    NotificationService.send_forgot_password_email(email, reset_token)
