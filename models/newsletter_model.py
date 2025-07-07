from sqlalchemy import Column, Integer, String, DateTime, func
from database import Base

class NewsletterSubscriber(Base):
    __tablename__ = "newsletter_subscribers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=func.now())  # Timestamp for subscription
    # updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  #