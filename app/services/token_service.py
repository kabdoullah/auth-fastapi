from app.models.request.token import TokenCreate
from app.repository.token_repository import TokenRepository
from fastapi import Depends

class TokenService:
    def __init__(self, token_repository: TokenRepository = Depends(TokenRepository)):
        self.token = token_repository


    def store_token(self, token: TokenCreate):
        return self.token.store_token(token)
    
    def verify_token(self, token):
        return self.token.verify_token(token)
    
    def delete_token(self, token):
        return self.token.delete_token(token)