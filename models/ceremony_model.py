from sqlalchemy import Column, Integer, String, DateTime, Text, func
from database import Base, BaseModelMixin

class CeremonyType(Base, BaseModelMixin):
    __tablename__ = "ceremony_types" # Table for different ceremony types
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=func.now())  # Timestamp for creation
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  # Timestamp for updates
    description = Column(String, nullable=True)  # Optional description field


class CeremonyPlan(Base, BaseModelMixin): 
    __tablename__ = "ceremony_plans"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # From payload
    ceremony_type = Column(String, nullable=False)               # 1. Ceremony type
    ceremony_metadata = Column(String, nullable=True)            # 2. Selected ceremony meta data (optional)
    voice_type = Column(String, nullable=False)                  # 3. Voice type
    background_sound = Column(String, nullable=False)            # 4. Background sound
    ceremonial_companion = Column(String, nullable=False)        # 5. Ceremonial companion
    ceremony_duration = Column(Integer, nullable=False)          # 6. Ceremony Duration
    meditation_duration = Column(Integer, nullable=True)         # 7. Meditation Duration (optional)
    ceremony_prompts = Column(String, nullable=False)            # 8. Ceremony personalization prompts
    meditation_prompts = Column(String, nullable=True)           # 9. Meditation personalization prompts (optional)
    ceremony_datetime = Column(String, nullable=False)           # 10. Date & time
    participants = Column(String, nullable=True)                 # 11. Participants (optional)
    email = Column(String, nullable=False)                       # 12. Email

    # Timestamps
    created_at = Column(DateTime, default=func.now())  
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

        
    # if I make participant a list
    # participant = Column(Text, nullable=True)  # Use Text for JSON string
    # def set_participant(self, participant_list):
    #     self.participant = json.dumps(participant_list)

    # def get_participant(self):
    #     return json.loads(self.participant) if self.participant else []