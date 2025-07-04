from flask import Flask, g,redirect, url_for, session, jsonify, request
from flask_cors import CORS
from flasgger import Swagger
from controllers.auth_controller import auth_bp
from controllers.notification_controller import notification_bp
from database import SessionLocal, Base, engine
from models.user_model import initialize_roles_and_admin
from services.notification_service import NotificationService

from config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI,SECRET_KEY


app = Flask(__name__)

CORS(app,origins=["http://localhost:3000"])  # Enable CORS for all routes
app.secret_key = SECRET_KEY

# ✅ Fix Swagger version
swagger = Swagger(app, template={
    "openapi": "3.0.2",
    "info": {
        "title": "User Management API",
        "description": "API for user authentication and password management",
        "version": "1.0.0"
    },
    "servers": [
        {
            "url": "http://localhost:5004",
            "description": "Local Development Server"
        }
    ]
})



app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
app.register_blueprint(notification_bp, url_prefix="/api/v1/notification")


# Create tables and initialize default roles & admin user
Base.metadata.create_all(bind=engine)
initialize_roles_and_admin()

@app.before_request
def create_session():
    g.db_session = SessionLocal()

@app.after_request
def close_session(response):
    db_session = getattr(g, "db_session", None)
    if db_session:
        db_session.close()
    return response

@app.route("/health", methods=["GET"])
def health_check():
    """Health Check
    ---
    get:
      description: Check if the User Management Service is running
      responses:
        200:
          description: Service is running
    """
    return {"status": "User Management Service is running"}, 200

if __name__ == "__main__":  
    app.run(host="0.0.0.0", port=5004)
