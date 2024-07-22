import random
import string  
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from fastapi import Depends
from app.configurations.database import get_db
from app.models.data.otp import OTP

class OTPRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create_otp(self):
        otp_code = ''.join(random.choices(string.digits, k=6))
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)
        self.db.add(otp_code)
        self.db.commit()
        self.db.refresh(otp_code)
        return otp_code, expires_at

    def get_otp(self, otp_code: str):
        return self.db.query(OTP).filter(OTP.otp_code == otp_code).first()
    
    def verify_otp(self, otp_code: str):
        db_otp = self.db.query(OTP).filter(OTP.otp_code == otp_code).first()
        if db_otp and db_otp.expires_at >= datetime.now(timezone.utc).replace(tzinfo=None):
            db_otp.used = True
            self.db.commit()
            return True
        return False

    def delete_otp(self, otp_code: str):
        db_otp = self.db.query(OTP).filter(OTP.otp_code == otp_code).first()
        if db_otp:
            self.db.delete(db_otp)
            self.db.commit()
