from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import os
from datetime import datetime, timedelta
from config import SECRET_KEY

def hash_password(password: str) -> str:
    return generate_password_hash(password, method='sha256')

def verify_password(hashed_password: str, password: str) -> bool:
    return check_password_hash(hashed_password, password)

# def generate_jwt(email: str, role: str) -> str:
#     print("inside the gnerate jwt", email, role)
#     payload = {"email": email, "role": role, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)}
#     print("jwt decoding",jwt.encode(payload, SECRET_KEY, algorithm="HS256"))
#     return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
def generate_jwt(email: str, role: str) -> str:
    
    payload = {
        "email": email,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    
    try:
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return token
    except Exception as e:
        return None


def generate_reset_token(user_id):
    """ Generate a password reset token (JWT) """
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=10)  # 10 min expiry
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def decode_reset_token(token):
    """ Decode a password reset token """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
