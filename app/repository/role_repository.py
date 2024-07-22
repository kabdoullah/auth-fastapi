from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends
from uuid import UUID
from app.configurations.database import get_db
from app.models.request.role import RoleCreate
from app.models.data.role import Role


class RoleRepository:
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        self.db = db

    def create_role(self, role: RoleCreate):
        db_role = Role(role.name)
        self.db.add(db_role)
        self.db.commit()
        self.db.refresh(db_role)
        return db_role  

    def update_role(self, role_id: UUID, role: RoleCreate):
        db_role = self.get_role_by_id(role_id=role_id)
        if db_role:
            db_role.update(**role.dict())
        self.db.commit()
        

    def delete_role(self, role_id: UUID):
        self.db.query(Role).filter(Role.id == role_id).delete()
        self.db.commit()


    def get_role_by_id(self, role_id: UUID):
        return self.db.query(Role).filter(Role.id == role_id).first()
    
    def get_all_roles(self):
        return self.db.query(Role).all()