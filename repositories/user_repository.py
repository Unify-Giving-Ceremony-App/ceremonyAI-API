from sqlalchemy.orm import Session
from models.user_model import User
from config import ADMIN_PASSWORD

class UserRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()
    
    def get_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def create_user(self, name: str, email: str, password: str, role_id: int):
        user = User(name=name, email=email, password=password, role_id=role_id)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_all_users(self):
        """ Fetch all users with role information """
        return self.db.query(User).all()
    
    
    # def is_email_verified(self, email: str) -> bool:
    #     """ Check if a user's email is verified """
    #     user = self.get_by_email(email)
    #     return user.email_verified if user else False
    
    def is_email_verified(self, email: str) -> bool:
        """ Check if a user's email is verified """
        user = self.get_by_email(email)
        
        if not user:
            # print(f"DEBUG: No user found with email {email}")  #  Debugging
            return False  # Return False if the user doesn't exist

        return user.email_verified

    def update_email_verified(self, email: str) -> bool:
        """ Verifies a user's email by updating the email_verified flag """
        user = self.get_by_email(email)
        if user:
            user.email_verified = True
            self.db.commit()
            return True
        return False
    
    
    def update_password(self, email: str, new_password: str):
        """ Updates a user's password """
        user = self.get_by_email(email)
        if user:
            user.password = new_password
            self.db.commit()
            return user  #  Return updated user instead of True
        return None  #  Return None if update fails
    
    
    def get_or_create_google_user(self, google_data):
        email = google_data.get("email")
        oauth_id = google_data.get("id")

        # Try to get existing user by email
        user = self.get_by_email(email)
        
        if user:
            # Update user if needed (e.g., oauth_id or provider not set yet)
            if not user.oauth_id:
                user.oauth_id = oauth_id
                user.oauth_provider = "google"
                user.image_url = google_data.get("picture")
                user.email_verified = True
                self.db.commit()
            return user

        # Create new user from Google profile
        new_user = User(
            name=google_data.get("name"),
            email=email,
            password=ADMIN_PASSWORD,  # No password for OAuth
            email_verified=True,
            oauth_provider="google",
            oauth_id=oauth_id,
            image_url=google_data.get("picture")
        )

        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user
