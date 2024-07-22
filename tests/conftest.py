# from datetime import timedelta
# import pytest
# from fastapi.testclient import TestClient
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from app.main import app
# from app.configurations.database import get_db, Base
# from app.utils.util import fm
# import os
# from app.models.data.user import User
# from app.models.request.professional_user import ProfessionalUserCreate
# from app.models.request.particular_user import ParticularUserCreate
# from app.utils.util import hash_password, create_refresh_token
# from app.configurations.security import REFRESH_TOKEN_EXPIRE_MINUTES


# SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")


# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# @pytest.fixture(scope="function")
# def test_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @pytest.fixture(scope="function")
# def app_test():
#     Base.metadata.create_all(bind=engine)
#     yield app
#     Base.metadata.drop_all(bind=engine)
    

# @pytest.fixture(scope="function")
# def client(app_test, test_db):
#     def _test_db():
#         return test_db
#     app_test.dependency_overrides[get_db] = _test_db
#     fm.config.SUPPRESS_SEND = 1
#     with TestClient(app_test) as client:
#         yield client


# @pytest.fixture
# def particular_user_data():
#     return {
#         "first_name": "John",
#         "last_name": "Doe",
#         "email": "johndoe@example.com",
#         "phone": "1234567890",
#         "password": "password123",
#         "birth_day": "1990-01-01"
#     }

# @pytest.fixture
# def professional_user_data():
#     return {
#         "first_name": "Jane",
#         "last_name": "Doe",
#         "email": "janedoe@example.com",
#         "phone": "1234567890",
#         "fixed_phone": "0987654321",
#         "company": "Example Inc",
#         "country": "US",
#         "company_type": "LLC",
#         "professional_category": "Technology",
#         "sub_category": "Software",
#         "website": "http://example.com",
#         "password": "password123"
#     }

# @pytest.fixture
# def login_data():
#     return {
#         "username": "janedoe@example.com",
#         "password": "password123"
#     }

# @pytest.fixture
# def test_profesional_user(test_db):
#     user_data = ProfessionalUserCreate(
#         first_name="Jane",
#         last_name="Doe",
#         email="janedoe@example.com",
#         phone="1234567890",
#         fixed_phone="0987654321",
#         company="Example Inc",
#         country="US",
#         company_type="LLC",
#         professional_category="Technology",
#         sub_category="Software",
#         website="http://example.com",
#         password="password123"
#     )
#     hashed_password = hash_password(user_data.password)
#     user = User(
#         first_name=user_data.first_name,
#         last_name=user_data.last_name,
#         email=user_data.email,
#         phone=user_data.phone,
#         fixed_phone=user_data.fixed_phone,
#         user_type="professional",
#         company=user_data.company,
#         country=user_data.country,
#         company_type=user_data.company_type,
#         professional_category=user_data.professional_category,
#         sub_category=user_data.sub_category,
#         website=user_data.website,
#         hashed_password=hashed_password
#     )
#     test_db.add(user)
#     test_db.commit()
#     test_db.refresh(user)
#     return user

# @pytest.fixture
# def test_particular_user(test_db):
#     user_data = ParticularUserCreate(
#         first_name="Jane",
#         last_name="Doe",
#         email="janedoe@example.com",
#         phone="1234567890",
#         birth_day="1990-01-01",
#         password="password123"
#     )
#     hashed_password = hash_password(user_data.password)
#     user = User(
#         first_name=user_data.first_name,
#         last_name=user_data.last_name,
#         email=user_data.email,
#         phone=user_data.phone,
#         user_type="particular",
#         birth_day=user_data.birth_day,
#         hashed_password=hashed_password
#     )
#     test_db.add(user)
#     test_db.commit()
#     test_db.refresh(user)
#     return user

# @pytest.fixture
# def valid_pro_refresh_token(test_profesional_user):
#     refresh_token_expires = timedelta(REFRESH_TOKEN_EXPIRE_MINUTES)
#     return create_refresh_token(test_db, data={"sub": test_profesional_user.id}, expires_delta=refresh_token_expires)


# @pytest.fixture
# def valid_par_refresh_token(test_particular_user):
#     refresh_token_expires = timedelta(REFRESH_TOKEN_EXPIRE_MINUTES)
#     refresh = create_refresh_token(test_db, data={"sub": test_particular_user.id}, expires_delta=refresh_token_expires)
#     print("refres :", refresh)
#     return refresh

# @pytest.fixture
# def invalid_refresh_token():
#     non_existent_user_id = 999
#     refresh_token_expires = timedelta(REFRESH_TOKEN_EXPIRE_MINUTES)
#     non_existent_refresh_token = create_refresh_token(test_db, data={"sub": non_existent_user_id}, expires_delta=refresh_token_expires)
#     return non_existent_refresh_token