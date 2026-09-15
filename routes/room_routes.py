from flask import Blueprint, request
from utils.decorators import role_required
from services.room_service import add_room, edit_room, remove_room, list_rooms
from services.user_service import register_renter, list_renters, edit_renter, remove_renter
from utils.response import success_response, error_response

room_bp = Blueprint("room", __name__)


@room_bp.route("/api/list", methods=["GET"])
@role_required("owner")
def api_list_rooms():
    return success_response(list_rooms())


@room_bp.route("/api/add", methods=["POST"])
@role_required("owner")
def api_add_room():
    data = request.get_json() or request.form
    result = add_room(
        data.get("room_no"),
        data.get("renter_name"),
        data.get("arriving_date"),
        data.get("advance_booking_amount"),
        data.get("first_reading")
    )
    if not result["success"]:
        return error_response(result["message"], 400)
    return success_response(result, result["message"])


@room_bp.route("/api/edit/<int:room_id>", methods=["POST"])
@role_required("owner")
def api_edit_room(room_id):
    data = request.get_json() or request.form
    result = edit_room(
        room_id,
        data.get("room_no"),
        data.get("renter_name"),
        data.get("arriving_date"),
        data.get("advance_booking_amount"),
        data.get("first_reading")
    )
    if not result["success"]:
        return error_response(result["message"], 400)
    return success_response(result, result["message"])


@room_bp.route("/api/delete/<int:room_id>", methods=["POST"])
@role_required("owner")
def api_delete_room(room_id):
    result = remove_room(room_id)
    return success_response(result, result["message"])


@room_bp.route("/api/renters", methods=["GET"])
@role_required("owner")
def api_list_renters():
    return success_response(list_renters())


@room_bp.route("/api/renter/add", methods=["POST"])
@role_required("owner")
def api_add_renter():
    data = request.get_json() or request.form
    result = register_renter(
        data.get("username"),
        data.get("password"),
        data.get("room_id")
    )
    if not result["success"]:
        return error_response(result["message"], 400)
    return success_response(result, result["message"])


@room_bp.route("/api/renter/edit/<int:renter_id>", methods=["POST"])
@role_required("owner")
def api_edit_renter(renter_id):
    data = request.get_json() or request.form
    result = edit_renter(
        renter_id,
        data.get("username"),
        data.get("password"),
        data.get("room_id")
    )
    if not result["success"]:
        return error_response(result["message"], 400)
    return success_response(result, result["message"])


@room_bp.route("/api/renter/delete/<int:renter_id>", methods=["POST"])
@role_required("owner")
def api_delete_renter(renter_id):
    result = remove_renter(renter_id)
    return success_response(result, result["message"])