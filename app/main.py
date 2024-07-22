from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.configurations.database import engine, Base
from app.api.user import router as user_router
from app.api.role import router as role_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="User Authentication Microservice")

origins = [
    "http://localhost",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix="/api/v1")
app.include_router(role_router, prefix="/api/v1")

Base.metadata.create_all(bind=engine)
