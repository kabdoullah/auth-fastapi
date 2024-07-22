from app.repository.otp_repository import OTPRepository
from fastapi import Depends

class OTPService:
    def __init__(self, otp_repository: OTPRepository = Depends(OTPRepository)):
        self.otp = otp_repository

    def create_otp(self):
        return self.otp.create_otp()
    

    def verify_otp(self, otp):
        return self.otp.verify_otp(otp)
    
    def delete_otp(self, otp):
        return self.otp.delete_otp(otp)