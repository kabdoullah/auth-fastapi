import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi.background import BackgroundTasks
from dotenv import load_dotenv



load_dotenv()

MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM")
MAIL_PORT = int(os.getenv("MAIL_PORT"))
MAIL_SERVER = os.getenv("MAIL_SERVER")
MAIL_FROM_NAME = os.getenv("MAIL_FROM_NAME")

conf = ConnectionConfig(
    MAIL_USERNAME = MAIL_USERNAME,
    MAIL_PASSWORD = MAIL_PASSWORD,
    MAIL_FROM = MAIL_FROM,
    MAIL_PORT = MAIL_PORT,
    MAIL_SERVER = MAIL_SERVER,
    MAIL_FROM_NAME=MAIL_FROM_NAME,
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

fm = FastMail(conf)

async def send_otp_email(email: str, otp: str, background_tasks: BackgroundTasks):
    html = f"""<p>Your OTP code is: {otp}</p> """

    message = MessageSchema(
        subject="Your OTP Code",
        recipients=[email],
        body=html,
        subtype=MessageType.html
    )
    
    background_tasks.add_task(fm.send_message, message)