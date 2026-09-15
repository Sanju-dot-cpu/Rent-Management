from flask import Blueprint, render_template, request
from utils.decorators import login_required
from services.room_service import get_room
from services.audit_service import list_audits
from services.electricity_service import list_bills
from utils.response import success_response, error_response

renter_bp = Blueprint("renter", __name__)


@renter_bp.route("/view", methods=["GET"])
@login_required
def view():
    user = request.user
    if user.get("role") != "renter":
        return error_response("Access denied", 403)

    room_id = user.get("room_id")
    if not room_id:
        return error_response("No room assigned", 404)

    room = get_room(room_id)
    if not room:
        return error_response("Room not found", 404)

    return render_template("renter/view.html", room=room)


@renter_bp.route("/api/my-room", methods=["GET"])
@login_required
def api_my_room():
    user = request.user
    if user.get("role") != "renter":
        return error_response("Access denied", 403)
    room = get_room(user.get("room_id"))
    if not room:
        return error_response("Room not found", 404)
    return success_response(room)


@renter_bp.route("/api/my-audits", methods=["GET"])
@login_required
def api_my_audits():
    user = request.user
    if user.get("role") != "renter":
        return error_response("Access denied", 403)
    return success_response(list_audits(user.get("room_id")))


@renter_bp.route("/api/my-bills", methods=["GET"])
@login_required
def api_my_bills():
    user = request.user
    if user.get("role") != "renter":
        return error_response("Access denied", 403)
    return success_response(list_bills(user.get("room_id")))