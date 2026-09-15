from flask import Blueprint, render_template
from utils.decorators import role_required
from services.room_service import list_rooms, get_room
from utils.response import success_response, error_response

from flask import request, session
from services.user_service import get_profile, update_profile
from utils.response import success_response, error_response

owner_bp = Blueprint("owner", __name__)


@owner_bp.route("/dashboard", methods=["GET"])
@role_required("owner")
def dashboard():
    rooms = list_rooms()
    return render_template("owner/dashboard.html", rooms=rooms)


@owner_bp.route("/room/<int:room_id>", methods=["GET"])
@role_required("owner")
def room_detail(room_id):
    room = get_room(room_id)
    if not room:
        return error_response("Room not found", 404)
    return render_template("owner/room_detail.html", room=room)


@owner_bp.route("/manage-renters", methods=["GET"])
@role_required("owner")
def manage_renters_page():
    return render_template("owner/manage_renters.html")



@owner_bp.route("/profile", methods=["GET"])
@role_required("owner")
def profile_page():
    return render_template("owner/profile.html")


@owner_bp.route("/api/profile", methods=["GET"])
@role_required("owner")
def api_profile():
    user_id = session.get("token") and request.user.get("user_id")
    profile = get_profile(user_id)
    if not profile:
        return error_response("Profile not found", 404)
    return success_response({
        "id": profile["id"],
        "username": profile["username"],
        "role": profile["role"]
    })


@owner_bp.route("/api/profile/update", methods=["POST"])
@role_required("owner")
def api_profile_update():
    data = request.get_json() or request.form
    user_id = request.user.get("user_id")
    result = update_profile(
        user_id,
        data.get("username"),
        data.get("old_password"),
        data.get("new_password")
    )
    if not result["success"]:
        return error_response(result["message"], 400)
    return success_response(result, result["message"])