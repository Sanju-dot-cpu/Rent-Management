import jwt
import datetime
from config import Config


def create_token(user_id, username, role, room_id=None):
    payload = {
        "user_id": user_id,
        "username": username,
        "role": role,
        "room_id": room_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=Config.JWT_EXP_HOURS)
    }
    return jwt.encode(payload, Config.JWT_SECRET, algorithm="HS256")


def verify_token(token):
    try:
        return jwt.decode(token, Config.JWT_SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None