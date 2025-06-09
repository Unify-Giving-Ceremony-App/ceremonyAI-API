import os
from dotenv import load_dotenv



# Security Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "default_fallback_secret")

# PostgreSQL Database Configuration

# Now load environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Default Admin User
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_NAME = os.getenv("ADMIN_NAME", "admin")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@example.com")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "Password")

# Redis Configuration
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", f"redis://{REDIS_HOST}:{REDIS_PORT}/0")

# Resend Email API
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")

# App URLs
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:5004")

# Google OAuth
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
FRONTEND_REDIRECT_URI = os.getenv("FRONTEND_REDIRECT_URI")
