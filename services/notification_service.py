import resend
import redis
import time
from celery_worker import Celery
from flask import jsonify
from services.email_service import generate_email_token
from config import RESEND_API_KEY, EMAIL_SENDER, BACKEND_URL, CELERY_BROKER_URL


# Configure Redis
redis_client = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)

# Configure Celery
celery = Celery(__name__, broker=CELERY_BROKER_URL)

# Configure Resend API
resend.api_key = RESEND_API_KEY

class NotificationService:
    @staticmethod
    def send_email(to_email, subject, html_content):
        """ Send an email using Resend API """
        try:
            resend.Emails.send({
                "from": EMAIL_SENDER,
                "to": to_email,
                "subject": subject,
                "html": html_content
            })
            print(f"Email sent to {to_email}")
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False

   
        # ✅ Periodic Celery Task (Runs every 5 seconds)
    @celery.task
    def send_pending_verifications(self):
        """ Celery task to check for pending email verifications """
        for key in redis_client.scan_iter("user:*:email_pending"):
            user_id = key.split(":")[1]
            email = redis_client.get(key)

            # Send verification email
            NotificationService.send_email_verification(user_id, email)

            # Remove key from Redis
            # redis_client.delete(key)

    @staticmethod
    def send_email_verification(user_id, email):
        """ Send email verification link to user """
        
        token = generate_email_token(user_id)
        verification_link = f"{BACKEND_URL}/api/v1/auth/verify-email/{token}"

        subject = "Verify Your Email"
        html_content = f"""
        <p>Click the link below to verify your email:</p>
        <a href="{verification_link}">Verify Email</a>
        """

        return NotificationService.send_email(email, subject, html_content)


    @staticmethod
    @celery.task
    def send_pending_reset_emails():
        """ Celery task to check for pending password reset emails every 5 seconds """
        while True:
            for key in redis_client.keys("reset_token:*"):
                user_id = key.split(":")[1]
                email_data = redis_client.get(key)

                if email_data:
                    email, reset_token = email_data.split(":")
                    NotificationService.send_forgot_password_email(email, reset_token)

                    # Remove key from Redis after sending
                    redis_client.delete(key)

            time.sleep(5)  # Check every 5 seconds
            
            
    @staticmethod
    @celery.task
    def send_forgot_password_email(email, reset_token):
        """ Celery task to send password reset email """
        reset_link = f"{BACKEND_URL}/api/v1/auth/reset-password/{reset_token}"

        subject = "Reset Your Password"
        html_content = f"""
        <p>Click the link below to reset your password:</p>
        <a href="{reset_link}">Reset Password</a>
        """

        return NotificationService.send_email(email, subject, html_content)
  