from repositories.ceremony_repository import CeremonyTypeRepository, CeremonyPlanRepository
from repositories.user_repository import UserRepository

class CeremonyTypeService:
    def __init__(self, db_session):
        self.repo = CeremonyTypeRepository(db_session)
    
    def get_ceremony_types(self):
        return self.repo.get_all_ceremony_types()   
    
    def add_ceremony_type(self, name: str, description: str = None):
        return self.repo.add_ceremony_type(name, description)


class CeremonyPlanService:
    def __init__(self, db_session):
        self.repo = CeremonyPlanRepository(db_session)
        self.user_repo = UserRepository(db_session)

    def user_ceremony_plans(self, email: str):
        if not self.user_repo.get_by_email(email):
            raise ValueError("User not found")  # 404 Not Found
        return self.repo.user_ceremony_plans(email)
    
    def get_ceremony_plan_by_id(self, ceremony_id: int):
        return self.repo.get_ceremony_plan_by_id(ceremony_id)
    
    def delete_ceremony_plan_by_id(self, ceremony_id: int):
        return self.repo.delete_ceremony_plan_by_id(ceremony_id)
    
    def get_all_ceremony_plan(self):
        return self.repo.get_all_ceremony_plan()   
    
    def add_ceremony_plan(self, email: str, ceremony_type: str,ceremony_metadata: str = None, voice_type: str = None,background_sound: str = None, ceremonial_companion: str = None,ceremony_duration: int = None, meditation_duration: int = None,ceremony_prompts: str = None, meditation_prompts: str = None,ceremony_datetime: str = None,participants: str = None):
        if not self.user_repo.get_by_email(email):
            raise ValueError("User not found")  # 404 Not Found
        return self.repo.add_ceremony_plan(email, ceremony_type,ceremony_metadata,
    voice_type,background_sound, ceremonial_companion,ceremony_duration, meditation_duration,ceremony_prompts, meditation_prompts,ceremony_datetime,participants)
    