from sqlalchemy import Column, Integer, String, ForeignKey, DateTime,Boolean, func
from sqlalchemy.orm import relationship
from database import Base, SessionLocal
from utils.security import hash_password
from config import ADMIN_USERNAME, ADMIN_EMAIL, ADMIN_PASSWORD,ADMIN_NAME
from models.role_model import Role

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False,unique=True)
    password = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False, default=2)  # Default role: 'user'
    email_verified = Column(Boolean, default=False)  # New column for email verification
    created_at = Column(DateTime, default=func.now())  # Timestamp for creation
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  #  Auto-update timestamp
    
        # New fields for social auth
    oauth_provider = Column(String, nullable=True)
    oauth_id = Column(String, nullable=True, unique=True)
    image_url = Column(String, nullable=True)

    role = relationship("Role")

# Function to initialize roles and default admin
def initialize_roles_and_admin():
    session = SessionLocal()
    
    # Ensure roles exist
    admin_role = session.query(Role).filter_by(name="admin").first()
    user_role = session.query(Role).filter_by(name="user").first()

    if not admin_role:
        admin_role = Role(name="admin")
        session.add(admin_role)

    if not user_role:
        user_role = Role(name="user")
        session.add(user_role)

    session.commit()

    # Ensure default admin exists
    admin_user = session.query(User).filter_by(email=ADMIN_EMAIL).first()
    if not admin_user:
        hashed_password = hash_password(ADMIN_PASSWORD)
        admin_user = User(username=ADMIN_USERNAME, name= ADMIN_NAME, email=ADMIN_EMAIL, password=hashed_password, role_id=admin_role.id)
        session.add(admin_user)
        session.commit()

    session.close()
    
def to_dict(self):
    return {
        "id": self.id,
        "username": self.username,
        "name": self.name,
        "email": self.email,
        "role": self.role.name if self.role else None,
        "email_verified": self.email_verified,
        "image_url": self.image_url,
        "oauth_provider": self.oauth_provider,
        "oauth_id": self.oauth_id,
        "created_at": self.created_at.isoformat() if self.created_at else None,
        "updated_at": self.updated_at.isoformat() if self.updated_at else None,
    }
