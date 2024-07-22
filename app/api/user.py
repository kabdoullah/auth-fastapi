from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.background import BackgroundTasks
from app.models.request.user import UserResponse, PasswordResetRequest, PasswordResetConfirm
from app.models.request.token import Token
from jwt.exceptions import InvalidTokenError
from app.configurations.security import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
from app.services.user_service import UserService
from app.services.otp_service import OTPService
from app.models.request.user import UserBase
from app.models.request.token import TokenCreate
from app.models.request.otp import OTPVerify
from app.configurations.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_access_token
from app.configurations.email import send_otp_email
from app.services.token_service import TokenService
from app.exceptions.custom_exception import InvalidCredentialsException, InvalidTokenException, UserNotFoundException


router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register_user(user_data: UserBase, background_tasks: BackgroundTasks, userservice: UserService = Depends(UserService), otpservice: OTPService = Depends(OTPService)):
    db_user = userservice.get_user_by_email(user_data.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    otp_code, _ = otpservice.create_otp()
    user_data.password = hash_password(user_data.password)
    new_user = userservice.create_user(user_data)
    await send_otp_email(new_user.email, otp_code, background_tasks)

    return new_user



@router.post("/login", response_model=Token)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],  userservice: UserService = Depends(UserService), token_service: TokenService = Depends(TokenService)):
    user = userservice.get_user_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise InvalidCredentialsException()

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    
    access_token = create_access_token(data={"sub": user.id}, expires_delta=access_token_expires)
    token_service.store_token(token=TokenCreate(token=access_token, user_id=user.id, expires_at=access_token_expires))
    refresh_token = create_refresh_token(data={"sub": user.id}, expires_delta=refresh_token_expires)

    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")

@router.post("/refresh", response_model=Token)
def refresh_token(refresh_token: str, userservice: UserService = Depends(UserService), token_service: TokenService = Depends(TokenService)):

    try:
        token_data = decode_access_token(refresh_token)
    except InvalidTokenError:
        raise InvalidTokenException()

    user = userservice.get_user_by_id(token_data.user_id)
    if not user:
        raise UserNotFoundException()

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.id}, expires_delta=access_token_expires)
    token_service.store_token(token=TokenCreate(token=access_token, user_id=user.id, expires_at=access_token_expires))

    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")

@router.post("/verify-otp")
def verify_otp_route(data: OTPVerify, otpservice: OTPService = Depends(OTPService)):
    if not otpservice.verify_otp(data.email, data.otp_code):
        raise HTTPException(status_code=400, detail="Invalid OTP or OTP expired")
    return {"message": "OTP verified"}


@router.post("/password-reset-request")
async def password_reset_request(data: PasswordResetRequest, background_tasks: BackgroundTasks, userservice: UserService = Depends(UserService), otpservice: OTPService = Depends(OTPService)):
    user = userservice.get_user_by_email(data.email)
    if not user:
        raise HTTPException(status_code=400, detail="Email not registered")
    
    otp_code, _ = otpservice.create_otp()
    await send_otp_email(user.email, otp_code, background_tasks)

    return {"message": "OTP sent to email"}

@router.post("/password-reset-confirm")
def password_reset_confirm(data: PasswordResetConfirm, otpservice: OTPService = Depends(OTPService), userservice: UserService = Depends(UserService)):
    if not otpservice.verify_otp(data.email, data.otp):
        raise HTTPException(status_code=400, detail="Invalid OTP or OTP expired")
    
    data.new_password = hash_password(data.new_password)
    user = userservice.reset_password(data.email, data.new_password)
    if not user:
        raise HTTPException(status_code=400, detail="Password reset failed")
    
    return {"message": "Password reset successfully"}


# @router.post("/change-password")
# def change_password(data: PasswordChangeRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
#     user = db.query(User).filter(User.id == current_user.id).first()

#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="User not found"
#         )

#     if not verify_password(data.current_password, user.hashed_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect current password"
#         )

#     update_password(db, user, data.new_password)

#     return {"message": "Password changed successfully"}

# @router.get("/users/me/", response_model=UserResponse)
# async def read_users_me(
#     current_user: Annotated[User, Depends(get_current_active_user)]):
#     return current_user

        
    