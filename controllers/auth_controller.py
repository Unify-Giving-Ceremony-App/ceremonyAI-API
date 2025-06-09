from flask import Blueprint, request, jsonify, g,redirect,redirect
from services.user_service import UserService
from services.notification_service import NotificationService
from database import get_db_session
from utils.auth_middleware import verify_jwt, admin_required
from repositories.user_repository import UserRepository
import redis
from config import REDIS_PORT,REDIS_HOST
from sqlalchemy.exc import SQLAlchemyError
from services.google_auth_service import GoogleAuthService

auth_bp = Blueprint("auth", __name__)

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)

@auth_bp.route("/register", methods=["POST"])
def register():
    """ Handles user registration and error handling """
    data = request.get_json()
    db_session = g.db_session  # Get session from middleware

    try:
        user_service = UserService(db_session)
        user = user_service.register_user(**data)

        # Store user ID in Redis
        # redis_client.setex(f"user:{user.id}:email_pending", 300, user.email)  

        # Send verification email in background
        NotificationService.send_email_verification(user.id, user.email)

        return jsonify({"message": "User registered. Please check your email for verification"}), 201
    
    except ValueError as e:  # Invalid input (duplicate email, role not found)
        return jsonify({"error": str(e)}), 400

    except PermissionError as e:  # Email is not verified
        return jsonify({"error": str(e)}), 403

    except RuntimeError as e:  # Database issues
        return jsonify({"error": str(e)}), 500

    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500

    except Exception as e:  # Catch any unexpected errors
        return jsonify({"error": "An unexpected error occurred"}), 500

@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    """ Sends a password reset email if the user exists and is verified """
    data = request.get_json()
    email = data.get("email")

    try:
        user_service = UserService()
        user_service.forgot_password(email)
        return jsonify({"message": "Password reset link sent to your email"}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except PermissionError as e:
        return jsonify({"error": str(e)}), 403
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception:
        return jsonify({"error": "An unexpected error occurred"}), 500
    
@auth_bp.route("/reset-password/<token>", methods=["POST"])
def reset_password(token):
    """ Resets a user's password if the reset token is valid """
    data = request.get_json()
    new_password = data.get("new_password")
    confirm_password = data.get("confirm_password")

    response, status = UserService.reset_password(token, new_password, confirm_password)
    return jsonify(response), status


@auth_bp.route("/change-password", methods=["POST"])
@verify_jwt  #  Requires authentication
def change_password():
    """ Allows authenticated users to change their password """
    data = request.get_json()
    email = g.email  # Extract from JWT middleware

    try:
        user_service = UserService(g.db_session)  # Create service instance
        user_service.change_password(
            email, 
            data.get("old_password"), 
            data.get("new_password"), 
            data.get("confirm_password")
        )
        return jsonify({"message": "Password changed successfully"}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except PermissionError as e:
        return jsonify({"error": str(e)}), 403
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception:
        return jsonify({"error": "An unexpected error occurred"}), 500

@auth_bp.route("/verify-email/<token>", methods=["GET"])
def verify_email(token):
    """Verifies user email using a confirmation token"""
    db_session = g.db_session
    user_service = UserService(db_session)

    try:
        response= user_service.verify_email(token)
        
        if response:
            return jsonify({"message": "Email Verified successfully"}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred"}), 500

@auth_bp.route("/login", methods=["POST"])
def login():
    """ Handles user login """
    data = request.get_json()
    db_session = g.db_session
    user_service = UserService(db_session)

    try:
     
        token, user = user_service.authenticate_user(data["email"], data["password"])
        
        user_data = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role.name,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
        }
    
        return jsonify({
            "success": True,
            "message": "Login successful",
            "data": [{
                "token": token,
                "user": user_data
            }]
        }), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 401

    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500

    except Exception:
        return jsonify({"error": "An unexpected error occurred"}), 500





@auth_bp.route("/users", methods=["GET"])
@verify_jwt
@admin_required
def get_all_users():
        """ Admin-only: Returns all users with their role """
        session = g.db_session
        user_repo = UserRepository(session)
        try:
            users = user_repo.get_all_users()
            user_list = [
                {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "role": user.role.name,
                    "created_at": user.created_at,
                    "updated_at": user.updated_at,
                }
                for user in users
            ]
            return jsonify({"users": user_list}), 200
        except SQLAlchemyError as e:
            return jsonify({"error": "Database error: " + str(e)}), 500
        except Exception:
            return jsonify({"error": "An unexpected error occurred"}), 500

@auth_bp.route("/userdetails", methods=["GET"])
@verify_jwt
def get_user_details():
        """ Users can only access their own details """
        session = g.db_session
        user_repo = UserRepository(session)
        try:
            user = user_repo.get_by_email(g.email)
            if not user:
                raise ValueError("User not found")
            user_data = {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role.name,
                "created_at": user.created_at,
                "updated_at": user.updated_at,
            }
            return jsonify(user_data), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except SQLAlchemyError as e:
            return jsonify({"error": "Database error: " + str(e)}), 500
        except Exception:
            return jsonify({"error": "An unexpected error occurred"}), 500
        
        

@auth_bp.route("/google/login", methods=["GET"])
def google_login():
    db_session = next(get_db_session()) 
    google_auth_service = GoogleAuthService(db_session)
    return redirect(google_auth_service.get_google_auth_url())

@auth_bp.route("/google/callback", methods=["GET"])
def google_callback():
    db_session = next(get_db_session()) 
    code = request.args.get("code")
    google_auth_service = GoogleAuthService(db_session)
    token_response, user = google_auth_service.handle_google_callback(code)
    user_data = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role.name if user.role else None,
        "email_verified": user.email_verified,
        "image_url": user.image_url,
        "oauth_provider": user.oauth_provider,
        "oauth_id": user.oauth_id,
    }

    return jsonify({
        "token": token_response,
        "user": user_data
    }), 200
