from models.ceremony_model import CeremonyType, CeremonyPlan

class CeremonyTypeRepository:
    def __init__(self, db_session):
        self.db = db_session

    def get_all_ceremony_types(self):
        return self.db.query(CeremonyType).all()
    
    def add_ceremony_type(self, name: str, description: str = None):
        if self.db.query(CeremonyType).filter_by(name=name).first():
            raise ValueError("Ceremony type already exists")
        ceremony_type = CeremonyType(name=name, description=description)
        self.db.add(ceremony_type)
        self.db.commit()
        self.db.refresh(ceremony_type)
        return ceremony_type


class CeremonyPlanRepository:
    def __init__(self, db_session):
        self.db = db_session

    def user_ceremony_plans(self, email: str):
        return self.db.query(CeremonyPlan).filter(CeremonyPlan.email == email).all()
    
    def get_ceremony_plan_by_id(self, ceremony_id: int):
        return self.db.query(CeremonyPlan).filter(CeremonyPlan.id == ceremony_id).first()
    
    def delete_ceremony_plan_by_id(self, ceremony_id: int):
        plans = self.db.query(CeremonyPlan).filter(CeremonyPlan.id == ceremony_id).all()
        if not plans:
            return False
        for plan in plans:
            self.db.delete(plan)
        self.db.commit()
        return True

    def get_all_ceremony_plan(self):
        return self.db.query(CeremonyPlan).all()
    
    def add_ceremony_plan(self, email: str, ceremony_type: str, ceremony_title: str, ceremony_date: str, duration: int, ceremony_description: str, participants: str, ceremony_subtype: str = None):    
        ceremony_plan = CeremonyPlan(user_email=email,
        ceremony_type=ceremony_type,
        ceremony_subtype=ceremony_subtype,
        ceremony_title=ceremony_title,
        ceremony_date=ceremony_date,
        duration=duration,
        ceremony_description=ceremony_description,
        participants=participants)
        self.db.add(ceremony_plan)
        self.db.commit()
        self.db.refresh(ceremony_plan)
        return ceremony_plan