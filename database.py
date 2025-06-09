from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from config import DATABASE_URL
from sqlalchemy.exc import OperationalError

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
