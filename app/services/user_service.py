from app.models.request.user import UserBase
from app.repository.user_repository import UserRepository
from app.models.data.user import User
from fastapi import Depends


class UserService:
    def __init__(self, user_repository: UserRepository = Depends(UserRepository)):
        self.user_repository = user_repository

    def create_user(self, user: UserBase):
        return self.user_repository.create_user(user)

    def get_user_by_email(self, email: str):
        return self.user_repository.get_user_by_email(email)
    
    def get_user_by_id(self, user_id: int):
        return self.user_repository.get_user_by_id(user_id)
    
    def get_all_users(self):
        return self.user_repository.get_all_users()
    
    def update_user(self, user: User):
        return self.user_repository.update_user(user)
    
    def delete_user(self, user_id: int):
        return self.user_repository.delete_user(user_id)
    
    def reset_password(self, email: str, new_password: str):
        return self.user_repository.reset_password(email=email,new_password=new_password)
    
    
    
   