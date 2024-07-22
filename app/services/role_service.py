from uuid import UUID
from fastapi import Depends
from app.models.request.role import RoleCreate
from app.repository.role_repository import RoleRepository

class RoleService:
    def __init__(self, role_repository: RoleRepository = Depends(RoleRepository)):
        self.role = role_repository

    def create_role(self, role_create: RoleCreate):
        role_create.name.lower()
        return self.role.create_role(role_create)

    def update_role(self, role_id: UUID, role_update: RoleCreate):
        role_update.name.lower()
        return self.role.update_role(role_update)

    def delete_role(self, role_id: UUID):
        return self.role.delete_role(role_id)
    
    def get_role_by_id(self, role_id: UUID):
        return self.role.get_role_by_id(role_id)
    
    def get_all_roles(self):
        return self.role.get_all_roles()