from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from config import DATABASE_URL
from sqlalchemy.exc import OperationalError
from datetime import datetime
from sqlalchemy.ext.declarative import declared_attr


# Create PostgreSQL Engine
try:
    engine = create_engine(DATABASE_URL)
    # Test connection immediately
    with engine.connect() as conn:
        print("Database connection successful.")
except OperationalError as e:
    print("Database connection failed:", e)
    raise

# Scoped session for handling database connections
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()

# Dependency Injection for session
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create a base mixin that every SQLAlchemy model inherits from
class BaseModelMixin:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def to_dict(self):
        data = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)

            # Convert datetime to ISO format
            if isinstance(value, datetime):
                value = value.isoformat()

            data[column.name] = value
        return data
    
