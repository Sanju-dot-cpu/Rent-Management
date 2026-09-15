import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change_this_secret_key")
    JWT_SECRET = os.getenv("JWT_SECRET", "change_this_jwt_secret")
    JWT_EXP_HOURS = 8

    DB_DRIVER = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")
    DB_SERVER = os.getenv("DB_SERVER", ".")
    DB_NAME = os.getenv("DB_NAME", "RentManagementDB")
    DB_USER = os.getenv("DB_USER", "")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_TRUSTED_CONNECTION = os.getenv("DB_TRUSTED_CONNECTION", "yes")