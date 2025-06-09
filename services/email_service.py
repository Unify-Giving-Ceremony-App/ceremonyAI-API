import os
import resend
import jwt
from datetime import datetime, timedelta
import redis
from config import SECRET_KEY, RESEND_API_KEY, EMAIL_SENDER, BACKEND_URL,REDIS_PORT,REDIS_HOST

# Configure Redis
# redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)

# Configure Resend API
resend.api_key = RESEND_API_KEY

def generate_email_token(user_id):
    """ Generate a JWT token for email verification """
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=5)  # Token expires in 5 minutes
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    # redis_client.setex(f"token:{token}", 300, user_id)  # Store token in Redis (expires in 5 min)
    return token

def send_email_verification(user_id, email):
    """ Send email verification link to user using Resend API """
    token = generate_email_token(user_id)
    verification_link = f"{BACKEND_URL}/api/v1/auth/verify-email/{token}"

    subject = "Verify Your Email"
    html_content = f"""
    <p>Click the link below to verify your email:</p>
    <a href="{verification_link}">Verify Email</a>
    """

    try:
        r = resend.Emails.send({
            "from": EMAIL_SENDER,
            "to": email,
            "subject": subject,
            "html": html_content
        })
        print(f"Verification email sent to {email}")
    except Exception as e:
        print(f"Error sending email: {e}")
