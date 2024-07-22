from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends, status
from app.models.request.role import RoleResponse, RoleCreate
from app.services.role_service import RoleService


router = APIRouter()

@router.post("/roles", status_code=status.HTTP_201_CREATED, response_model=RoleResponse)
def create_role(data: RoleCreate, roleservice: RoleService = Depends(RoleService)):
    new_role = roleservice.create_role(data)
    return new_role

@router.get("/roles", status_code=status.HTTP_200_OK, response_model=list[RoleResponse])
def get_role(roleservice: RoleService = Depends(RoleService)):
    return roleservice.get_all_roles()


@router.put("/roles/{id}", response_model=RoleResponse)
def update_role(id: UUID, data: RoleCreate, roleservice: RoleService = Depends(RoleService)):
    return roleservice.update_role(role_id=id, role_update=data)

@router.delete("/roles/{id}")
def delete_role(id: UUID, roleservice: RoleService = Depends(RoleService)):
    roleservice.delete_role(id)
    return {"Success"}