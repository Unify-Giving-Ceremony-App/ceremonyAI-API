from sqlalchemy import Column, Integer, String, DateTime, Text, func
from database import Base

class CeremonyType(Base):
    __tablename__ = "ceremony_types" # Table for different ceremony types
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=func.now())  # Timestamp for creation
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  # Timestamp for updates
    description = Column(String, nullable=True)  # Optional description field


class CeremonyPlan(Base):
    __tablename__ = "ceremony_plans"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False)
    ceremony_type = Column(String, nullable=False)
    ceremony_subtype = Column(String, nullable=True)
    ceremony_title = Column(String, nullable=False)
    ceremony_date = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)
    ceremony_description = Column(String, nullable=False)
    participants = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())  # Timestamp for creation
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now()) # Timestamp for updates


        
    # if I make participant a list
    # participant = Column(Text, nullable=True)  # Use Text for JSON string
    # def set_participant(self, participant_list):
    #     self.participant = json.dumps(participant_list)

    # def get_participant(self):
    #     return json.loads(self.participant) if self.participant else []