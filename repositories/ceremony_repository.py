from models.ceremony_model import CeremonyType, CeremonyPlan

class CeremonyTypeRepository:
    def __init__(self, db_session):
        self.db = db_session

    def get_all_ceremony_types(self):
        _types = self.db.query(CeremonyType).all()
        if not _types:
            return []
        return [t.to_dict() for t in _types] # Return list of types
    
    def add_ceremony_type(self, name: str, description: str = None):
        if self.db.query(CeremonyType).filter_by(name=name).first():
            raise ValueError("Ceremony type already exists")
        ceremony_type = CeremonyType(name=name, description=description)
        self.db.add(ceremony_type)
        self.db.commit()
        self.db.refresh(ceremony_type)
        return ceremony_type.to_dict()


class CeremonyPlanRepository:
    def __init__(self, db_session):
        self.db = db_session

    def user_ceremony_plans(self, email: str):
        plans = self.db.query(CeremonyPlan).filter(CeremonyPlan.email == email).all()
        if not plans:
            return []
        return [plan.to_dict() for plan in plans] # Return list of plans
    
    def get_ceremony_plan_by_id(self, ceremony_id: int):
        plan = self.db.query(CeremonyPlan).filter(CeremonyPlan.id == ceremony_id).first()
        return plan.to_dict() if plan else None
    
    def delete_ceremony_plan_by_id(self, ceremony_id: int):
        plans = self.db.query(CeremonyPlan).filter(CeremonyPlan.id == ceremony_id).all()
        if not plans:
            return False
        for plan in plans:
            self.db.delete(plan)
        self.db.commit()
        return True

    def get_all_ceremony_plan(self):
        plans = self.db.query(CeremonyPlan).all()
        if not plans:
            return []
        return [plan.to_dict() for plan in plans] # Return list of plans
 
    def add_ceremony_plan(self, email: str, ceremony_type: str,ceremony_metadata: str = None, voice_type: str = None,background_sound: str = None, ceremonial_companion: str = None,ceremony_duration: int = None, meditation_duration: int = None,ceremony_prompts: str = None, meditation_prompts: str = None,ceremony_datetime: str = None,participants: str = None):  
        ceremony_plan = CeremonyPlan(email=email,
        ceremony_type=ceremony_type.upper(),
        ceremony_metadata=ceremony_metadata,
        voice_type=voice_type.upper(),
        background_sound=background_sound.upper(),
        ceremonial_companion=ceremonial_companion,
        ceremony_duration=ceremony_duration,
        meditation_duration=meditation_duration,
        ceremony_prompts=ceremony_prompts,
        meditation_prompts=meditation_prompts,
        ceremony_datetime=ceremony_datetime,
        participants=participants)
        self.db.add(ceremony_plan)
        self.db.commit()
        self.db.refresh(ceremony_plan)
        return ceremony_plan.to_dict()

