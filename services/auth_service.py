from models.user_model import get_user_by_username
from utils.jwt_utils import create_token


def authenticate(username, password):
    user = get_user_by_username(username)
    if not user:
        return None

    # Exact password match (any case + special chars allowed)
    if user["password"] != password:
        return None

    token = create_token(
        user_id=user["id"],
        username=user["username"],
        role=user["role"],
        room_id=user["room_id"]
    )
    return {
        "token": token,
        "user_id": user["id"],
        "username": user["username"],
        "role": user["role"],
        "room_id": user["room_id"]
    }