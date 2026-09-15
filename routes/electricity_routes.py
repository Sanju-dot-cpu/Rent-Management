from flask import Blueprint, request
from utils.decorators import role_required
from services.electricity_service import list_bills, add_bill, edit_bill, remove_bill, get_bill
from utils.response import success_response, error_response

from flask import send_file
from services.room_service import get_room
from services.pdf_service import electricity_pdf

electricity_bp = Blueprint("electricity", __name__)


@electricity_bp.route("/list/<int:room_id>", methods=["GET"])
@role_required("owner")
def api_list_bills(room_id):
    return success_response(list_bills(room_id))


@electricity_bp.route("/get/<int:bill_id>", methods=["GET"])
@role_required("owner")
def api_get_bill(bill_id):
    bill = get_bill(bill_id)
    if not bill:
        return error_response("Bill not found", 404)
    return success_response(bill)


@electricity_bp.route("/add", methods=["POST"])
@role_required("owner")
def api_add_bill():
    data = request.get_json() or request.form
    result = add_bill(
        data.get("room_id"),
        data.get("month"),
        data.get("start_date"),
        data.get("units"),
        data.get("amount"),
        data.get("paid_date"),
        data.get("balance_amount"),
        data.get("status")
    )
    if not result["success"]:
        return error_response(result["message"], 400)
    return success_response(result, result["message"])


@electricity_bp.route("/edit/<int:bill_id>", methods=["POST"])
@role_required("owner")
def api_edit_bill(bill_id):
    data = request.get_json() or request.form
    result = edit_bill(
        bill_id,
        data.get("month"),
        data.get("start_date"),
        data.get("units"),
        data.get("amount"),
        data.get("paid_date"),
        data.get("balance_amount"),
        data.get("status")
    )
    if not result["success"]:
        return error_response(result["message"], 400)
    return success_response(result, result["message"])


@electricity_bp.route("/delete/<int:bill_id>", methods=["POST"])
@role_required("owner")
def api_delete_bill(bill_id):
    result = remove_bill(bill_id)
    return success_response(result, result["message"])


@electricity_bp.route("/download/<int:room_id>", methods=["GET"])
@role_required("owner")
def api_download_electricity_pdf(room_id):
    room = get_room(room_id)
    if not room:
        return error_response("Room not found", 404)
    bills = list_bills(room_id)
    buf = electricity_pdf(room, bills)
    return send_file(
        buf,
        as_attachment=True,
        download_name=f"electricity_{room['room_no']}.pdf",
        mimetype="application/pdf"
    )