from flask import request, jsonify, g
import jwt
from functools import wraps
from config import SECRET_KEY
from repositories.user_repository import UserRepository

def verify_jwt(f):
    """ Middleware to verify JWT token for protected routes """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token or not token.startswith("Bearer "):
            return jsonify({"error": "Token is missing or invalid"}), 401

        token = token.split(" ")[1]  # Extract actual token
        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            g.email = decoded_token["email"]
            g.role = decoded_token["role"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated_function

def admin_required(f):
    """ Middleware to ensure only admins can access a route """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.role != "admin":
            return jsonify({"error": "Unauthorized: Admin access required"}), 403
        return f(*args, **kwargs)

    return decorated_function
