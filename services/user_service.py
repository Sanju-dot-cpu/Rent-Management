from models.user_model import (
    get_user_by_username, get_user_by_id, get_all_renters,
    create_renter, update_renter, delete_renter
)
from utils.validators import is_empty


def register_renter(username, password, room_id):
    if is_empty(username) or is_empty(password):
        return {"success": False, "message": "Username and password required"}

    # ✅ Only username must be unique (login key).
    # Names in Rooms table can duplicate freely — matched by room_id.
    if get_user_by_username(username):
        return {"success": False, "message": "Username already exists"}

    rid = create_renter(username, password, room_id)
    return {"success": True, "message": "Renter created", "id": rid}


def list_renters():
    return get_all_renters()


def get_renter(renter_id):
    return get_user_by_id(renter_id)


def edit_renter(renter_id, username, password, room_id):
    if is_empty(username) or is_empty(password):
        return {"success": False, "message": "Username and password required"}
    update_renter(renter_id, username, password, room_id)
    return {"success": True, "message": "Renter updated"}


def remove_renter(renter_id):
    delete_renter(renter_id)
    return {"success": True, "message": "Renter deleted"}

def get_profile(user_id):
    return get_user_by_id(user_id)


def update_profile(user_id, username, old_password, new_password):
    user = get_user_by_id(user_id)
    if not user:
        return {"success": False, "message": "User not found"}
    if user["password"] != old_password:
        return {"success": False, "message": "Old password is incorrect"}
    if is_empty(username) or is_empty(new_password):
        return {"success": False, "message": "Username and new password required"}

    update_renter(user_id, username, new_password, user["room_id"])
    return {"success": True, "message": "Profile updated"}