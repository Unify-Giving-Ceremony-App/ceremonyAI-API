from sqlalchemy.orm import Session
from models.role_model import Role

class RoleRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_role_by_name(self, name: str):
        return self.db.query(Role).filter(Role.name == name).first()
    
    def get_role_by_id(self, id: int):
        return self.db.query(Role).filter(Role.id == id).first()

    def create_role(self, name: str):
        role = Role(name=name)
        self.db.add(role)
        self.db.commit()
        self.db.refresh(role)
        return role
