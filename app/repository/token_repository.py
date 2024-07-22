from sqlalchemy.orm import Session
from fastapi import Depends
from uuid import UUID   
from app.configurations.database import get_db
from app.models.data.token import Token
from app.models.request.token import TokenCreate

class TokenRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def store_token(self, token: TokenCreate):
        token = Token(**token.dict())
        self.db.add(token)
        self.db.commit()
        self.db.refresh(token)


    def get_token(self, token: str):
        return self.db.query(Token).filter(Token.token == token).first()

    def delete_token(self, token: str):
        db_token = self.db.query(Token).filter(Token.token == token).first()
        if db_token:
            self.db.delete(db_token)
            self.db.commit()


    def get_token_by_user_id(self, user_id: UUID):
        return self.db.query(Token).filter(Token.user_id == user_id).first()
    
    def verify_token(self, token: str):
        db_token = self.get_token(token)
        if db_token:
            return db_token.is_valid()
        return False
