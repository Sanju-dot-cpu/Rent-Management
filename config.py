import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change_this_secret_key")
    JWT_SECRET = os.getenv("JWT_SECRET", "change_this_jwt_secret")
    JWT_EXP_HOURS = 8

    DB_PATH = os.getenv("DB_PATH", "rent_management.db")