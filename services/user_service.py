from repositories.user_repository import UserRepository
import redis
from repositories.role_repository import RoleRepository
from services.notification_service import NotificationService
from utils.security import hash_password, verify_password, generate_jwt
from utils.security import generate_reset_token
from sqlalchemy.exc import SQLAlchemyError
from config import SECRET_KEY
import jwt

# redis_client = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)

class UserService:
    def __init__(self, db_session):
        self.user_repo = UserRepository(db_session)
        self.role_repo = RoleRepository(db_session)

    def register_user(self, name: str, email: str, password: str, role_name: str = "user"):
        """ Register a user and handle errors properly """
        role = self.role_repo.get_role_by_name(role_name)
        if not role:
            raise ValueError(f"Role '{role_name}' does not exist")  # Raise ValueError

        if self.user_repo.get_by_email(email):
            raise ValueError("Email already exists")  # Raise ValueError

        try:
            hashed_password = hash_password(password)
            user = self.user_repo.create_user(name, email, hashed_password, role.id)
            return user
        except SQLAlchemyError as e:
            raise RuntimeError(f"Database error: {str(e)}")  # Catch database errors

    def authenticate_user(self, email: str, password: str):
        try:
            user = self.user_repo.get_by_email(email)
            
          
             
            if not user:
                raise ValueError("Email does not exists")  # 401 Unauthorized

            if not verify_password(user.password, password):
                raise ValueError("Invalid credentials")  # 401 Unauthorized

            if not self.user_repo.is_email_verified(user.email):
                raise ValueError("Email is not verified")  # 401 Unauthorized
            
            token = generate_jwt(user.email, user.role.name)
            
           
            return token, user

        except SQLAlchemyError as e:
            raise RuntimeError(f"Database error: {str(e)}")  # Catch database errors
    
    def create_default_admin(self):
        admin_role = self.role_repo.get_role_by_name("admin")
        if not admin_role:
            admin_role = self.role_repo.create_role("admin")

        # if not self.user_repo.get_by_username("admin"):
        #     hashed_password = hash_password("Password")
        #     self.user_repo.create_user("admin", "admin@example.com", hashed_password, admin_role.id)
            
            
    def forgot_password(self, email: str):
        """ Stores forgot password request in Redis instead of sending email immediately """
        user = self.user_repo.get_by_email(email)
        if not user:
            raise ValueError("User not found")

        if not user.email_verified:
            raise PermissionError("Please verify your email before resetting your password")

        try:
            reset_token = generate_reset_token(user.id)
            
            # Store request in Redis (expires in 10 minutes)
            # redis_client.setex(f"reset_token:{user.id}", 600, f"{user.email}:{reset_token}")

        except SQLAlchemyError as e:
            raise RuntimeError(f"Database error: {str(e)}")
        except redis.RedisError as e:
            raise RuntimeError(f"Redis error: {str(e)}")
    
    # def reset_password(self, token: str, new_password: str, confirm_password: str):
    #     """Handles password reset if the token is valid"""
    #     user_id = redis_client.get(f"reset_token:{token}")
    #     if not user_id:
    #         raise ValueError("Invalid or expired reset token")

    #     if new_password != confirm_password:
    #         raise ValueError("Passwords do not match")

    #     user = self.user_repo.get_by_id(int(user_id))
    #     if not user:
    #         raise ValueError("User not found")
        
    #     try:
    #         updated_user = self.user_repo.update_password(int(user_id), hash_password(new_password))
    #         if not updated_user:
    #             raise RuntimeError("Password reset failed")
    #         redis_client.delete(f"reset_token:{token}")
    #     except SQLAlchemyError as e:
    #         raise RuntimeError(f"Database error: {str(e)}")
    
    
    def change_password(self, email: str, old_password: str, new_password: str, confirm_password: str):
        """Allows authenticated users to change their password"""
        user = self.user_repo.get_by_email(email)
        print("Inside the service - Retrieved user:", user)

        if not user:
            raise ValueError("User not found")

        if not verify_password(user.password, old_password):
            raise PermissionError("Incorrect old password")

        if new_password != confirm_password:
            raise ValueError("Passwords do not match")

        try:
            print("Inside the service - Updating password")
            updated_user = self.user_repo.update_password(email, hash_password(new_password))
            
            if not updated_user:
                raise RuntimeError("Password change failed")

        except SQLAlchemyError as e:
            raise RuntimeError(f"Database error: {str(e)}")


    def verify_email(self, token: str):
        """ Verifies email using a confirmation token """
        try:
            # user_id = redis_client.get(f"token:{token}")
             # Decode the token using SECRET_KEY
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

            user_id = payload.get("user_id")
        
            if not user_id:
                raise ValueError("Invalid or expired token")

            user = self.user_repo.get_by_id(int(user_id))
            if not user:
                raise ValueError("User not found")

            # Update email verification status
            return self.user_repo.update_email_verified(user.email)


        except ValueError as e:
            return {"error": str(e)}, 400

        except SQLAlchemyError as e:
            return {"error": f"Database error: {str(e)}"}, 500

        except Exception as e:
            return {"error": "An unexpected error occurred"}, 500